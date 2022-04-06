# -*- coding: utf-8 -*-
{
    "name": "Email and Pop Up Notifications",
    #"version": "8.0.1.0.1",
    "category": "Extra Tools",
    "author": "Excode Innovation Solutions",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "base","mail",
        "hr",
        "bahia_personnel_management",
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/popup_notifications.xml",
        "views/mail_group.xml"
    ],
    "qweb": [
        "static/xml/base_popup.xml"
    ],
    #"js": [],
    #"demo": [],
    #"external_dependencies": {},

    "summary": "Use popup notification to develop your modules",
    "description": """
    Uses the Code for Pop Up Notification
        https://odootools.com/apps/8.0/popup-notifications-165
    """
}