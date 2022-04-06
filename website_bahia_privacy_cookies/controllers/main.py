# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)


class website_bahia_privacy_cookies(http.Controller):
    @http.route('/page/privacy_policy', type='http', auth="public", website=True)
    def privacy_policy(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_privacy_cookies.cookies_privacy_policy_page", {
        	'no_button':1
        	})

    @http.route('/page/privacy_policy2', type='http', auth="public", website=True)
    def privacy_policy2(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_privacy_cookies.cookies_privacy_policy_page", {
        	'no_button':0


        	})

# vim :et:
