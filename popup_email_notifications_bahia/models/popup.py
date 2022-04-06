# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

from openerp.osv import fields as f1, osv
from openerp.tools.translate import _

class popup_notification(models.Model):
    _name = "popup.notification"

    title = fields.Char()
    message = fields.Text()
    status = fields.Selection([('shown', 'Check'), ('draft', 'Uncheck')], defaul='draft')
    partner_ids = fields.Many2many('res.users')
    employee_id = fields.Many2one('hr.employee')
    description = fields.Text()
    #changes_license = fields.Text('License Changes')
    #changes_documents = fields.Text('Document Changes')
    #changes_medical = fields.Text('Medical Changes')

    @api.multi
    def get_notifications(self):
        result = []
        for obj in self:
            result.append({
                'title': obj.title,
                'message': obj.message,
                'status': obj.status,
                'id': obj.id,
                'user_id': self._uid,
            })
        return result

    @api.one
    def set_recdone(self):
        notif_obj = self.env['popup.notification'].sudo().browse([self.id])
        user_id = self._uid
        if notif_obj:
            if not notif_obj.partner_ids:
                notif_obj.status = 'shown'
            else:
                notif_obj.partner_ids = [(3, user_id)]
                if not notif_obj.partner_ids:
                    notif_obj.status = 'shown'
        return True



class popup_notification2(osv.osv):
    _inherit = "popup.notification"


    def open_employee_info(self, cr, uid,ids, context={}):
        hr_employee = self.pool.get('hr.employee')
        model_data = self.pool.get('ir.model.data')
        act_window = self.pool.get('ir.actions.act_window')

        for notification in self.browse(cr, uid, ids, context=context):
            emp_id = notification.employee_id.id

        action_model, action_id = model_data.get_object_reference(cr, uid, 'hr', 'open_view_employee_list')
        dict_act_window = act_window.read(cr, uid, [action_id], [])[0]
        if emp_id:
            dict_act_window['res_id'] = emp_id
            #domain.append(('id','=', notify_id))
        dict_act_window['view_mode'] = 'form,tree'
        dict_act_window['target'] = 'current'
        dict_act_window['nodestroy'] = True
        return dict_act_window
    

    def action_view_allchanges(self, cr, uid,notify_id=False,user_id=False, context={}):
        model_data = self.pool.get('ir.model.data')
        act_window = self.pool.get('ir.actions.act_window')
        #raise Warning(user_id)
        #notif_id=False,
#        domain=[]

        #raise Warning(notify_id)
        domain = [('partner_ids', 'in', user_id),
                  ('status', '=', 'draft')]
        #if notif_id:
        #    domain.append(('id','=', notif_id))

        action_model, action_id = model_data.get_object_reference(cr,1,'popup_email_notifications_bahia', 'open_popup_notification_tree')
        dict_act_window = act_window.read(cr, 1, [action_id], [])[0]
        #if emp_id:
        #    dict_act_window['res_id'] = emp_id
        #dict_act_window['view_mode'] = 'form,tree'
        #raise Warning(dict_act_window)
        if notify_id:
            dict_act_window['res_id'] = notify_id
            domain.append(('id','=', notify_id))
        dict_act_window['view_mode'] = 'tree,form'
        dict_act_window['target'] = 'current'
        dict_act_window['flags'] = {                            
                 'pager': True,
                 'views_switcher': True, 
                 'search_view':True,
                 }
        dict_act_window['nodestroy'] = True
        #dict_act_window['flags'] = {
        #    'pager': True,
        #    'views_switcher': True, 
        #    'search_view':True,        
        #}
        #raise Warning(dict_act_window)
        return dict_act_window

        #tuple_return_action = {
        #   'name': _('Employee Changes'),
        #   'view_type': 'form',
        #   'view_mode' : 'tree',
        #   'res_model': 'popup.notification',
        #   'type': 'ir.actions.act_window',
        #  'context': {},
        #   'domain': domain,
        #  'target':'current',
        #   'views': [[False, 'form']],
        #    'nodestroy': True,
        #    #'flags' : {
        #    #     'pager': True,
        #    #     'views_switcher': True, 
        #     #    'search_view':True,
        #    #     }
        #} 
        #return  tuple_return_action