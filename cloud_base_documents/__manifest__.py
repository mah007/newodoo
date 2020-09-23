# -*- coding: utf-8 -*-
{
    "name": "Cloud Sync for Enterprise Documents",
    "version": "13.0.1.0.1",
    "category": "Document Management",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/13.0/cloud-sync-for-enterprise-documents-431",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "cloud_base",
        "documents"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/documents_document.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The technical extension to sync Odoo Enterprise Documents with cloud clients",
    "description": """
    This is the extension for the cloud storage clients to synchronize Odoo Enterprise Documents. This module is a technical extension and is not of use without a real client app. Please select a desired one below:

    The documents hierarchy is reflected within the folder 'Odoo / Odoo Docs'
    Each Odoo folder has a linked cloud folder
    All files are synced with the same logic as usual attachments
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "44.0",
    "currency": "EUR",
}