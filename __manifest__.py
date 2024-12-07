{
    'name': 'IoT Production Integration',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Integrasi perangkat IoT dengan Odoo untuk produksi',
    'description': """
        Modul untuk mengintegrasikan perangkat IoT dalam pemantauan dan pengelolaan produksi.
    """,
    'author': 'Your Name',
    'depends': ['base', 'web', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/iot_menu.xml',
        'views/iot_device_views.xml',
    ],
    'installable': True,
    'application': True,
}
