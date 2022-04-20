odoo.define('ibas_bahia_website.main', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var sPopup = require('website.s_popup');
    var rpc = require('web.rpc')
    var _t = core._t;

    publicWidget.registry.popupPolicy = publicWidget.Widget.extend({
        selector: '#sPopup1647114881651',
        events: {
            'keyup': '_onCheckKey',
            //'click.js_close_popup': '_clickAccept',
        },        
        init: function () {
            this._super.apply(this, arguments);
        },

        start: async function () {
            var self = this;
        },

        _onCheckKey: function (ev) {
            console.log(ev.keyCode);  
            if(ev.keyCode === 27){ // Key code for ESC key
                //ev.preventDefault();
                //return false
                console.log(1);
            }          
        },
        _clickAccept: function (ev) {
            ev.stopPropagation();
            //this.onTargetHide();
            this.$target.modal('hide');
            //this.trigger_up('snippet_option_visibility_update', {show: false}); 
        },
        onTargetHide: async function () {
        return new Promise(resolve => {
            const timeoutID = setTimeout(() => {
                this.$target.off('hidden.bs.modal.popup_on_target_hide');
                resolve();
            }, 500);
            this.$target.one('hidden.bs.modal.popup_on_target_hide', () => {
                clearTimeout(timeoutID);
                resolve();
            });
            this.$target.modal('hide');
        });
    },                
    });

    //EXTEND POPUP
    // publicWidget.registry.exsPopup = publicWidget.registry.popup.extend({
    //     /**
    //      * @override
    //      */
    //     start: function () {

    //         console.log('OVERR');

    //         return this._super(...arguments);
    //     },

    // });

});




window.addEventListener('load', checkJSLoaded)
function checkJSLoaded() {
    // create the script element
    console.log('app.js file has been loaded');
}