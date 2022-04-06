import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)

class website_crewlist_active_on_board(http.Controller):


    @http.route('/web?<model("hr.personnel.withrmks.menu")>', type='http', auth="private", website=False)
    def route_1(self, job):	
    	raise 
