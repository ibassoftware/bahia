{
    "name" : "Database Auto-Backup & Backup Auto-Transfer to FTP server",
    "version" : "6.1",
    "author" : "Emipro Technologies",
    "website" : "http://www.emiprotechnologies.com",
    "category" : "Generic Modules",
    "description": """
    
        Key feature of this module includes,
        
        -- Automatic database backup based on scheduler
        -- Manual database backup
        -- Database backup log
        -- FTP server configuration & Automatic transfer of database backup to remote location
        -- Email Notification of database notification to fix email address or Users of ERP system
        -- Email Alert to particular person when someone has manually taken database backup
        
        For feedback and support, please contact us on info@emiprotechnologies.com
                
        For more modules of OpenERP developments, please visit on following link,
        
        http://www.emiprotechnologies.com/OpenERP/Module6/
        http://www.emiprotechnologies.com/OpenERP/Module7/
                
        For our video's of OpenERP please visit following link,
        
        http://www.emiprotechnologies.com/OpenERP/Video
        
    """,
    "data" : ["view/bkp_conf_view.xml",
                    "security/db_backup_security.xml",
                    "security/backup_data.xml",
                    "security/ir.config_parameter.csv",
                    "wizard/manual_db_backup_view.xml",
                    "view/ftp_view.xml",
                    "security/ir.model.access.csv"
                    ],
    "active": False,
    "installable": True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: