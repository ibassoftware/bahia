    # -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)

class website_bahia_pages_services(http.Controller):

    @http.route('/page/services', type='http', auth="public", website=True)
    def services(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages_services.services", {})