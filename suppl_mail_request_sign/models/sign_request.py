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


class SignRequest(models.Model):
    _inherit = "sign.request"

    mail_activity_sign_request_id = fields.Many2one('mail.activity',  string="Source activity")
    mail_activity_res_model = fields.Char(related='mail_activity_sign_request_id.res_model')
    mail_activity_res_id = fields.Many2oneReference(related='mail_activity_sign_request_id.res_id')

    def action_signed(self):
        for request in self:
            if not request.mail_activity_sign_request_id:
                continue

            request.mail_activity_sign_request_id.action_feedback(feedback=_('Document signed by all parties.'))

        super(SignRequest, self).action_signed()

    def action_canceled(self):
        if self.mail_activity_sign_request_id:
            res = self.env[self.mail_activity_res_model].sudo().browse(self.mail_activity_res_id)
            if res:
                res.message_post(body=_('Document sign request cancelled for: <a href=# data-oe-model=sign.request data-oe-id=%d>%s</a>.') % (self.id, self.template_id.name))

            if not self.env.context.get('activity_cancel', False):
                self.with_context(sign_request_cancel=True).mail_activity_sign_request_id.unlink()

        return super(SignRequest, self).action_canceled()


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def action_completed(self):
        for sign in self.mapped('sign_request_id'):
            if not sign.mail_activity_sign_request_id:
                continue

            res = self.env[sign.mail_activity_res_model].sudo().browse(sign.mail_activity_res_id)
            if not res:
                continue

            res.message_post(body=_('%s signed on document: %s.') % (self.partner_id.name, sign.template_id.name))

        super(SignRequestItem, self).action_completed()


