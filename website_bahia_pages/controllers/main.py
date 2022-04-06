# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)


class website_bahia_pages(http.Controller):
    @http.route('/page/principals', type='http', auth="public", website=True)
    def principal(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.principal", {})

    @http.route('/aboutus', type='http', auth="public", website=True)
    def aboutus(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.aboutus", {})


    @http.route('/contactus', type='http', auth="public", website=True)
    def contactus(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.contactus", {})



    @http.route('/page/faqs', type='http', auth="public", website=True)
    def faqs(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.faqs", {})


    @http.route('/page/generalguidelines', type='http', auth="public", website=True)
    def generalguidelines(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.generalguidelines", {})


    @http.route('/page/announcements', type='http', auth="public", website=True)
    def announcements(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.announcements", {})


    @http.route('/page/gallery', type='http', auth="public", website=True)
    def gallery(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.gallery", {})        


    @http.route('/page/governmentlinks', type='http', auth="public", website=True)
    def governmentlinks(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.governmentlinks", {})     


    #Overriding Homepage
    @http.route('/page/homepage', type='http', auth="public", website=True)
    def homepage(self):
        #env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        # Render page
        return request.website.render("website_bahia_pages.homepage", {})




# vim :et:
