# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    microsoft_outlook_client_identifier = fields.Char("Outlook Client Id")
    microsoft_outlook_client_secret = fields.Char("Outlook Client Secret")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICP = self.env["ir.config_parameter"]
        res.update(
            microsoft_outlook_client_identifier=ICP.get_param(
                "microsoft_outlook_client_id"
            ),
            microsoft_outlook_client_secret=ICP.get_param(
                "microsoft_outlook_client_secret"
            ),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env["ir.config_parameter"]
        ICP.set_param(
            "microsoft_outlook_client_id", self.microsoft_outlook_client_identifier
        )
        ICP.set_param(
            "microsoft_outlook_client_secret", self.microsoft_outlook_client_secret
        )
