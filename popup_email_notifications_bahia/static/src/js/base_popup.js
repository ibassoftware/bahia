openerp.popup_email_notifications_bahia = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

instance.web.WebClient = instance.web.WebClient.extend({

    check_popup_notifications: function () {
        var self = this;
        this.rpc('/popup_email_notifications_bahia/notify')
        .done(
            function (notifications) {
                _.each(notifications,  function(notif) {
                    setTimeout(function() {
                        if ($('.ui-notify-message p#p_id').filter(function () {
                            return $(this).html() == notif.id;
                        }).length) {
                            return;
                        } // prevent displaying same notifications
                        notif.title = QWeb.render('popup_title', {'title': notif.title, 'id': notif.id});

                        notif.message += QWeb.render('popup_footer');

                        notif_elem = self.do_notify(notif.title, notif.message, true);

                        notif_elem.element.find(".link2showed").on('click',function() {
                            self.get_notif_box(this).find('.ui-notify-close').trigger("click");
                            self.rpc("/popup_email_notifications_bahia/notify_ack", {'notif_id': notif.id});
                        });

                        notif_elem.element.find(".link2viewall").on('click',function() {
                            act_call = (new instance.web.Model('popup.notification').call('action_view_allchanges',[false,notif.user_id])).then(function(result) {
                                var action = result;
                                console.log(instance);
                                instance.client.action_manager.do_action(action);
                            });
                            self.get_notif_box(this).find('.ui-notify-close').trigger("click");                        
                            //alert('1');
                        });
                        
                        notif_elem.element.find(".link2view").on('click',function() {
                            console.log(notif.user_id);
                            act_call = (new instance.web.Model('popup.notification').call('action_view_allchanges',[notif.id,notif.user_id])).then(function(result) {
                                var action = result;
                                console.log(instance);
                                instance.client.action_manager.do_action(action);
                            });
                            self.get_notif_box(this).find('.ui-notify-close').trigger("click");                        
                            //alert('1');
                        });


                    }, 1000); // #TODO check original module
                });
            }
        )
        .fail(function (err, ev) {
            if (err.code === -32098) {
                // Prevent the CrashManager to display an error
                // in case of an xhr error not due to a server error
                //console.log('Error')
                ev.preventDefault();
            }
        });
    },

    start: function (parent) {
        var self = this;
        self._super(parent);
        //console.log('qweqwe');
        $(document).ready(function () {
            self.check_popup_notifications();
            setInterval( function() {
                //console.log('Working!');
                self.check_popup_notifications();
            }, 30 * 1000);
        });
    },

})};
