#Inherit the Old API for 
import openerp
from openerp.osv import osv, fields

class im_chat_session(osv.Model):
    _inherit = "im_chat.session"


    def session_get(self, cr, uid, user_to, context=None):
        """ returns the canonical session between 2 users, create it if needed """
        session_id = False
        if user_to:
            sids = self.search(cr, uid, [('user_ids','in', user_to),('user_ids', 'in', [uid])], context=context, limit=1)
            #raise Warning(sids)
            for sess in self.browse(cr, openerp.SUPERUSER_ID, sids, context=context):
                #Added here to Check for Tom
                #raise Warning(sess.id)
                #raise Warning(sess.user_ids)

                if len(sess.user_ids) == 2 and sess.is_private():
                    session_id = sess.id
                    break
            else:
                session_id = self.create(cr, uid, { 'user_ids': [(6,0, (user_to, uid))] }, context=context)

        return self.session_info(cr, uid, [session_id], context=context)