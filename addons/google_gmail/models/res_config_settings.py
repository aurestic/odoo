# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    google_gmail_client_identifier = fields.Char("Gmail Client Id")
    google_gmail_client_secret = fields.Char("Gmail Client Secret")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICP = self.env["ir.config_parameter"]
        res.update(
            google_gmail_client_identifier=ICP.get_param("google_gmail_client_id"),
            google_gmail_client_secret=ICP.get_param("google_gmail_client_secret"),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env["ir.config_parameter"]
        ICP.set_param("google_gmail_client_id", self.google_gmail_client_identifier)
        ICP.set_param("google_gmail_client_secret", self.google_gmail_client_secret)
