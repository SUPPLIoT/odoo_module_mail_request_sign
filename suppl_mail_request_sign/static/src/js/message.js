odoo.define('suppl_mail_request_sign/static/src/message.js', function (require) {
    'use strict';

    const {registerClassPatchModel, registerFieldPatchModel} = require('mail/static/src/model/model_core.js');

    const {attr} = require('mail/static/src/model/model_field.js');

    registerFieldPatchModel('mail.message', 'suppl_mail_request_sign/static/src/message.js', {
        request_sign_completed_document: attr(),
        request_sign_item_infos: attr(),
        request_sign_reference: attr(),
        request_sign_request_id: attr()
    });

    registerClassPatchModel('mail.message', 'suppl_mail_request_sign/static/src/activity.js', {
        //----------------------------------------------------------------------
        // Public
        //----------------------------------------------------------------------

        /**
         * @override
         */
        convertData(data) {
            const data2 = this._super(data);

            if ('request_sign_completed_document' in data) {
                data2.request_sign_completed_document = data.request_sign_completed_document;
            }
            if ('request_sign_item_infos' in data) {
                data2.request_sign_item_infos = data.request_sign_item_infos;
            }
            if ('request_sign_reference' in data) {
                data2.request_sign_reference = data.request_sign_reference;
            }
            if ('request_sign_request_id' in data) {
                data2.request_sign_request_id = data.request_sign_request_id;
            }

            return data2;
        },
    });

});
