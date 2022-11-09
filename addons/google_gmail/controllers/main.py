# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import passlib.utils
import werkzeug
from itertools import izip

from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_encode

from openerp import _, http
from openerp.exceptions import Warning as UserError
from openerp.http import request

_logger = logging.getLogger(__name__)


def _consteq(str1, str2):
    """ Constant-time string comparison. Suitable to compare bytestrings of fixed,
        known length only, because length difference is optimized. """
    return len(str1) == len(str2) and sum(ord(x)^ord(y) for x, y in izip(str1, str2)) == 0

consteq = getattr(passlib.utils, 'consteq', _consteq)


class GoogleGmailController(http.Controller):
    @http.route('/google_gmail/confirm', type='http', auth='user')
    def google_gmail_callback(self, code=None, state=None, error=None, **kwargs):
        """Callback URL during the OAuth process.

        Gmail redirects the user browser to this endpoint with the authorization code.
        We will fetch the refresh token and the access token thanks to this authorization
        code and save those values on the given mail server.
        """
        if not request.env.user.has_group('base.group_system'):
            _logger.error('Google Gmail: non-system user trying to link an Gmail account.')
            raise Forbidden()

        if error:
            return _('An error occur during the authentication process: %s.') % error

        try:
            state = json.loads(state)
            model_name = state['model']
            rec_id = state['id']
            csrf_token = u"{}".format(state['csrf_token'])
        except Exception:
            _logger.error('Google Gmail: Wrong state value %r.', state)
            raise Forbidden()

        model = request.env[model_name]

        if not 'google.gmail.mixin' in model._inherit:
            # The model must inherits from the "google.gmail.mixin" mixin
            raise Forbidden()

        record = model.browse(rec_id).exists()
        if not record:
            raise Forbidden()

        outlook_csrf_token = u"{}".format(record._get_gmail_csrf_token())
        if not csrf_token or not consteq(csrf_token, outlook_csrf_token):
            _logger.error('Google Gmail: Wrong CSRF token during Gmail authentication.')
            raise Forbidden()

        try:
            refresh_token, access_token, expiration = record._fetch_gmail_refresh_token(code)
        except UserError as e:
            return _('An error occur during the authentication process: %s.') % str(e.name)

        record.write({
            'google_gmail_access_token': access_token,
            'google_gmail_access_token_expiration': expiration,
            'google_gmail_authorization_code': code,
            'google_gmail_refresh_token': refresh_token,
        })

        url_params = {
            'id': rec_id,
            'model': model_name,
            'view_type': 'form'
        }
        url = '/web?#' + url_encode(url_params)
        return werkzeug.utils.redirect(url, 303)
