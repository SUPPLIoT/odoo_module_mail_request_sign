# -*- coding: utf-8 -*-

###################################################################################
#
#    Original work Copyright (c) 2004-2015 Odoo S.A.
#    Modified work Copyright (c) SUPPLIoT GmbH.
#
#    This file is part of Request Document Sign module by SUPPLIoT
#    (see https://suppliot.eu).
#
#    See LICENSE file for full copyright and licensing details.
#
###################################################################################


from odoo import api, models, fields, _
from odoo.exceptions import UserError


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
