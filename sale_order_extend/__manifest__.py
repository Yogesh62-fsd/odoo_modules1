{
    'name': 'Sale Order Extended Module',
    'version': '1.3',
    'description': 'This is sale order extended module designed for demonstartion purpose.',
    'author': 'Yogesh Pandey',
    'website': "https://www.emiprotechnologies.com/",
    'depends': ['sale_crm','sales_team','sale','purchase'],
    'data': ['security/ir.model.access.csv',
             'views/sale_order_ept_view.xml',
             'data/crm_lead_demo.xml',
             'data/product_product_data.xml',
             'views/product_extd.xml',
             'views/purchase_order_line_extd_view.xml',
             'wizard/merger_sale_order_wizard_view.xml']

}
