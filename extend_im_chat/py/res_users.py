#Inherit the Old API for 
import openerp
from openerp.osv import osv, fields

class res_users(osv.Model):
    _inherit = "res.users"

    _columns = {
        'is_user_allow_portal_im' : fields.boolean('Can be View by Seafarers'),
    }


    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.extend(['is_user_allow_portal_im'])
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.extend(['is_user_allow_portal_im'])
        return init_res


    def im_search(self, cr, uid, name, limit=20, context=None):
    	result = []

    	result = super(res_users, self).im_search(cr, uid, name, limit, context)

    	# To Check if User is belong to the Portal Group if 
    	# user belong to the Portal Group then all User Chat must all be Belong to Employee Group and if its tag as Allow in Portal Chat
    	group_portal = self.pool['ir.model.data'].get_object_reference(cr, 1, 'base', 'group_portal')[1]
        group_employee = self.pool['ir.model.data'].get_object_reference(cr, 1, 'base', 'group_user')[1]

    	#raise Warning(uid)
    	model_res_groups = self.pool['res.groups']

    	search_user = model_res_groups.search(cr,1, [('users', '=', uid), ('id', '=', group_portal)],context=context)
    	if search_user:
    		if len(search_user) > 0:

    			result = []
		        where_clause_base = " U.active = 't' "
		        query_params = ()
		        if name:
		            where_clause_base += " AND P.name ILIKE %s "
		            query_params = query_params + ('%'+name+'%',)

		        # first query to find online employee
		        cr.execute('''SELECT U.id as id, P.name as name, COALESCE(S.status, 'offline') as im_status
		                FROM im_chat_presence S
		                    JOIN res_users U ON S.user_id = U.id
		                    JOIN res_partner P ON P.id = U.partner_id
		                WHERE   '''+where_clause_base+'''
		                        AND U.id != %s
		                        AND EXISTS (SELECT 1 FROM res_groups_users_rel G WHERE G.gid = %s AND G.uid = U.id)
		                        AND is_user_allow_portal_im = (1::BOOLEAN)
		                ORDER BY P.name
		                LIMIT %s
		        ''', query_params + (uid, group_employee, limit))
		        result = result + cr.dictfetchall()
        #raise Warning(result)
        #AND S.status = 'online'
        return result   

		