# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    microsoft_outlook_client_identifier = fields.Char("Outlook Client Id")
    microsoft_outlook_client_secret = fields.Char("Outlook Client Secret")

    @api.model
    def get_default_microsoft_values(self, fields):
        ICP = self.env["ir.config_parameter"]
        return {
            "microsoft_outlook_client_identifier": ICP.get_param(
                "microsoft_outlook_client_id"
            ),
            "microsoft_outlook_client_secret": ICP.get_param(
                "microsoft_outlook_client_secret"
            ),
        }

    @api.multi
    def set_microsoft_values(self):
        ICP = self.env["ir.config_parameter"]
        ICP.set_param(
            "microsoft_outlook_client_id", self.microsoft_outlook_client_identifier
        )
        ICP.set_param(
            "microsoft_outlook_client_secret", self.microsoft_outlook_client_secret
        )
