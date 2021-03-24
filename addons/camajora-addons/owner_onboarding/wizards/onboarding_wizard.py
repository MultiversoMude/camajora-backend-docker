# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import email_split


_logger = logging.getLogger(__name__)


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ""


class OwnerWizard(models.TransientModel):
    _name = "owner.onboarding.wizard"
    _description = _("Grant Owner Access")

    def _default_user_ids(self):
        """
        For each partner, determine corresponding owner.onboarding.wizard.user records
        """
        partner_ids = self.env.context.get("active_ids", [])
        contact_ids = set()
        user_changes = []

        for partner in self.env["res.partner"].sudo().browse(partner_ids):
            # make sure that each contact appears at most once in the list
            if partner.id in contact_ids:
                continue

            contact_ids.add(partner.id)

            is_owner = partner.user_ids and (
                self.env.ref("rental.group_rental_owner")
                in partner.user_ids[0].groups_id
            )

            user = {
                "partner_id": partner.id,
                "email": partner.email,
                "is_owner": is_owner,
            }

            user_changes.append((0, 0, user))

        return user_changes

    user_ids = fields.One2many(
        comodel_name="owner.onboarding.wizard.user",
        inverse_name="wizard_id",
        string=_("Users"),
        default=_default_user_ids,
    )

    welcome_message = fields.Text(
        string=_("Invitation Message"),
        help=_("This text is included in the email sent to new owners."),
    )

    @api.multi
    def action_apply(self):
        self.ensure_one()
        self.user_ids.action_apply()
        return {"type": "ir.actions.act_window_close"}


class OwnerWizardUser(models.TransientModel):
    _name = "owner.onboarding.wizard.user"
    _description = _("Owner User Config")

    wizard_id = fields.Many2one(
        comodel_name="owner.onboarding.wizard",
        string=_("Wizard"),
        required=True,
        ondelete="cascade",
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string=_("Contact"),
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    email = fields.Char(_("Email"))
    user_id = fields.Many2one(comodel_name="res.users", string=_("Login User"))

    @api.multi
    def action_apply(self):
        """
        From selected partners, add corresponding users to owner group.
        """
        self.env["res.partner"].check_access_rights("write")
        group_owner = self.env.ref("rental.group_rental_owner")
        """
        error_msg = self.get_error_messages()
        if error_msg:
            raise UserError("\n\n".join(error_msg))
        """

        for wizard_user in self.sudo().with_context(active_test=False):
            # checking if the partner has a linked user
            user = (
                wizard_user.partner_id.user_ids[0]
                if wizard_user.partner_id.user_ids
                else None
            )

            # update partner email, if a new one was introduced
            if wizard_user.partner_id.email != wizard_user.email:
                wizard_user.partner_id.write({"email": wizard_user.email})

            # add owner group to relative user of selected partners
            user_owner = None
            # create a user if necessary, and make sure it is in the portal group
            if not user:
                if wizard_user.partner_id.company_id:
                    company_id = wizard_user.partner_id.company_id.id
                else:
                    company_id = (
                        self.env["res.company"]._company_default_get("res.users").id
                    )
                user_owner = (
                    wizard_user.sudo()
                    .with_context(company_id=company_id)
                    ._create_user()
                )
            else:
                user_owner = user

            wizard_user.write({"user_id": user_owner.id})

            if group_owner not in wizard_user.user_id.groups_id:
                wizard_user.user_id.write(
                    {"active": True, "groups_id": [(6, 0, [group_owner.id])]}
                )
                # prepare for the signup process
                wizard_user.user_id.partner_id.signup_prepare()

            # wizard_user.with_context(active_test=True)._send_email()
            wizard_user.refresh()

    @api.multi
    def _create_user(self):
        """ create a new user for wizard_user.partner_id
            :returns record of res.users
        """
        company_id = self.env.context.get("company_id")
        return (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            ._create_user_from_template(
                {
                    "email": extract_email(self.email),
                    "login": extract_email(self.email),
                    "partner_id": self.partner_id.id,
                    "company_id": company_id,
                    "company_ids": [(6, 0, [company_id])],
                }
            )
        )

    @api.multi
    def _send_email(self):
        """ send notification email to a new portal user """
        if not self.env.user.email:
            raise UserError(
                _(
                    "You must have an email address in your User Preferences to send emails."
                )
            )

        # determine subject and body in the portal user's language
        template = self.env.ref("portal.mail_template_data_portal_welcome")
        for wizard_line in self:
            lang = wizard_line.user_id.lang
            partner = wizard_line.user_id.partner_id

            portal_url = partner.with_context(
                signup_force_type_in_url="", lang=lang
            )._get_signup_url_for_action()[partner.id]
            partner.signup_prepare()

            if template:
                template.with_context(
                    dbname=self._cr.dbname, portal_url=portal_url, lang=lang
                ).send_mail(wizard_line.user_id.id, force_send=True)
            else:
                _logger.warning(
                    "No email template found for sending email to the portal user"
                )

        return True
