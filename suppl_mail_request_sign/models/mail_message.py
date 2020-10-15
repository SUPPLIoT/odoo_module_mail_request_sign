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


class Message(models.Model):
    _inherit = 'mail.message'

    request_sign_request_id = fields.Many2one('sign.request', string='Requested Signatures', required=False)

    request_sign_reference = fields.Char(related="request_sign_request_id.reference")
    request_sign_item_infos = fields.Binary(related="request_sign_request_id.request_item_infos")
    request_sign_completed_document = fields.Binary(related="request_sign_request_id.completed_document")

    def _get_message_format_fields(self):
        return super(Message, self)._get_message_format_fields() + [
            'request_sign_request_id',
            'request_sign_reference',
            'request_sign_item_infos',
            'request_sign_completed_document'
        ]