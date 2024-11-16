

{
    'name': 'Estate',
    'depends': ['base', 'mail'],
    'category': 'Real Estate/Brokerage',
    'application': 'true',
    'license': 'LGPL-3',
    'data': [
        'data/mail_activity.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ]
}
