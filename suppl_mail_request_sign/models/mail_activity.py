# -*- coding: utf-8 -*-

###################################################################################
#
#    Copyright (c) SUPPLIoT GmbH.
#
#    This file is part of Request Document Sign module by SUPPLIoT
#    (see https://suppliot.eu).
#
#    See LICENSE file for full copyright and licensing details.
#
###################################################################################


from odoo import api, models, fields, _
from odoo.exceptions import UserError


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('sign_document', 'Sign Document')])

    request_sign_template_id = fields.Many2one(
        'sign.template', required=False, default=lambda self: self.env.context.get('active_id', None),
    )

    @api.onchange('category')
    def _onchange_category_request_sign(self):
        if self.category == 'sign_document':
            self.mail_template_ids = False


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    request_sign_template_id = fields.Many2one('sign.template', required=False)
    request_sign_signer_ids = fields.One2many('mail.activity.send.request.signer', 'mail_activity_send_request_id', string="Signers", required=False)
    request_sign_follower_ids = fields.Many2many('res.partner', string="Copy to", required=False)
    request_sign_filename = fields.Char("Filename", required=False)

    request_sign_request_id = fields.Many2one('sign.request', string='Requested Signatures', required=False)
    request_sign_reference = fields.Char(related="request_sign_request_id.reference")
    request_sign_item_infos = fields.Binary(related="request_sign_request_id.request_item_infos")

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        super(MailActivity, self)._onchange_activity_type_id()

        if not self.activity_type_id:
            return

        if self.activity_type_id.category == 'sign_document':
            ## todo somethin' usefull
            self.request_sign_template_id = self.activity_type_id.request_sign_template_id or False
        else:
            self.request_sign_template_id = False
            self.request_sign_signer_ids = False
            self.request_sign_follower_ids = False
            self.request_sign_filename = False

    @api.onchange('request_sign_template_id')
    def _onchange_activity_template_id(self):
        if not self.request_sign_template_id:
            self.request_sign_signer_ids = False
            return

        roles = self.request_sign_template_id.sign_item_ids.responsible_id
        self.request_sign_filename = self.request_sign_template_id.display_name
        self.summary = _("Signature Request - %(file_name)s", file_name=self.request_sign_template_id.attachment_id.name)
        self.request_sign_signer_ids = [(5, 0, 0)] + [(0, 0, {
            'role_id': role.id,
            'partner_id': False,
        }) for role in roles]


    @api.model
    def create(self, values):
        activity = super(MailActivity, self).create(values)
        activity_type = activity.activity_type_id

        if activity_type and activity_type.category == 'sign_document':
            self._create_sign_request(activity)

        return activity

    def _create_sign_request(self, activity):
        SignObj = self.env['sign.request'].sudo()

        res = SignObj.with_context({
            'default_model': activity.res_model,
            'default_res_id': activity.res_id,
        }).initialize_new(
            activity.request_sign_template_id.id,
            [{'partner_id': signer.partner_id.id, 'role': signer.role_id.id} for signer in activity.request_sign_signer_ids],
            self.request_sign_follower_ids.ids,
            activity.summary,
            activity.summary,
            activity.note,
            True,
            False)

        sign_request = SignObj.browse(res['id'])
        sign_request.toggle_favorited()
        sign_request.action_sent()
        sign_request.write({'state': 'sent', 'mail_activity_sign_request_id': activity.id})
        sign_request.request_item_ids.write({'state': 'sent'})

        activity.request_sign_request_id = res['id']

    def _action_done(self, feedback=False, attachment_ids=None):
        self = self.with_context(activity_done=True)

        if not self.request_sign_request_id:
            return super(MailActivity, self)._action_done(feedback, attachment_ids)

        request_id = self.request_sign_request_id.id
        messages, next_activities = super(MailActivity, self)._action_done(feedback, attachment_ids)

        for msg in messages:
            msg.request_sign_request_id = request_id

        return messages, next_activities

    def unlink(self):
        if self.request_sign_request_id and \
                not self.env.context.get('sign_request_cancel', False) and \
                not self.env.context.get('activity_done', False):
            self.with_context(activity_cancel=True).request_sign_request_id.action_canceled()

        return super(MailActivity, self).unlink()


class MailActivitySendRequestSigner(models.TransientModel):
    _name = "mail.activity.send.request.signer"
    _description = 'Sign send request signer for mail activity'

    role_id = fields.Many2one('sign.item.role', readonly=True, required=True)
    partner_id = fields.Many2one('res.partner', required=True, string="Contact")
    mail_activity_send_request_id = fields.Many2one('mail.activity')

    def create(self, vals_list):
        missing_roles = []
        for vals in vals_list:
            if not vals.get('partner_id'):
                role_id = vals.get('role_id')
                role = self.env['sign.item.role'].browse(role_id)
                missing_roles.append(role.name)
        if missing_roles:
            missing_roles_str = ', '.join(missing_roles)
            raise UserError(_(
                'The following roles must be set to create the signature request: %(roles)s',
                roles=missing_roles_str,
            ))
        return super().create(vals_list)
