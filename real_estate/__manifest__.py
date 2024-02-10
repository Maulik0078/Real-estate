# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Real Estate',
    'version' : '1.0',
    'summary': 'Real Estate Mangament',
    'sequence': 10,
    'Description':'Real Estate Mangament Software',   
    'category': '',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
    'sale',
    'account',],
    'data': [
        'security/ir.model.access.csv',
        'data/estate_auto_mail_views.xml',
        'data/estate_mail.xml',
        'views/estate_property_views.xml',
        'views/estate_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_settings_views.xml',
        'views/estate_inherit_views.xml',
        'views/estate_menu_views.xml',
 
    ],
    'demo': [],
    'installable': True,
    'application': True,
  
}
