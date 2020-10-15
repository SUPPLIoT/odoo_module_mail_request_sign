# -*- coding: utf-8 -*-

###################################################################################
#
#    Copyright (c) SUPPLIoT GmbH.
#
#    This file is part of SUPPLIoT Request Document Sign module
#    (see https://suppliot.eu).
#
#    See LICENSE file for full copyright and licensing details.
#
###################################################################################

{
    'name': 'Request Document Sign',
    'version': '1.0',
    'category': 'Sales/Sign',
    'summary': '',
    'description': "",
    'author': "SUPPLIoT GmbH",
    'website': 'https://www.suppliot.eu',
    'license': 'LGPL-3',
    'depends': ['mail', 'sign'],
    'data': [
        'views/assets.xml',
        'views/activity_views.xml',
        #
        'security/ir.model.access.csv'
    ],
    'qweb': [
        'static/src/xml/activity.xml',
        'static/src/xml/message.xml'
    ],
    'installable': True,
    'application': False
}
