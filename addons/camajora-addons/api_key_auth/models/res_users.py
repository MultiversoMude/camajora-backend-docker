                  # Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models, _
from odoo.addons.auth_signup.models.res_partner import now

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    password_reset_url = fields.Char(
        string=_("Password reset url"),
        compute="_compute_password_reset_url"
    )

    def _send_partner_password_reset(self):
        expiration = now(days=+90)
        self.partner_id.signup_prepare(signup_type="reset", expiration=expiration)

        template = self.env.ref("api_key_auth.user_password_reset_email")

        assert template._name == "mail.template"

        template_values = {
            "email_to": self.partner_id.email,
            "email_cc": False,
            "auto_delete": False,
            "partner_to": False,
            "scheduled_date": False,
        }

        _logger.error("[USER PASSWORD RESET] SENDING EMAIL")
        _logger.error(template_values)

        template.write(template_values)
        template.with_context(lang=self.lang).send_mail(
            self.id, force_send=True,
            # raise_exception=False
        )

    def _compute_password_reset_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.app.url')

        for record in self:
            if record.partner_id.signup_token:
                record.password_reset_url = '{}/password_reset/{}'.format(
                    base_url,
                    record.partner_id.signup_token
                )
            else:
                record.password_reset_url = False
