# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    google_gmail_client_identifier = fields.Char("Gmail Client Id")
    google_gmail_client_secret = fields.Char("Gmail Client Secret")

    @api.model
    def get_default_gmail_values(self, fields):
        ICP = self.env["ir.config_parameter"]
        return {
            "google_gmail_client_identifier": ICP.get_param("google_gmail_client_id"),
            "google_gmail_client_secret": ICP.get_param("google_gmail_client_secret"),
        }

    @api.multi
    def set_gmail_values(self):
        ICP = self.env["ir.config_parameter"]
        ICP.set_param("google_gmail_client_id", self.google_gmail_client_identifier)
        ICP.set_param("google_gmail_client_secret", self.google_gmail_client_secret)
