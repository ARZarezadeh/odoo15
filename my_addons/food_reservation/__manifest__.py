{
    "name": "Food Reservation",
    "depends": ["base", "mail", "many2many_binary_widget_file_size"],
    "category": "Food/Reservation",
    "application": "True",
    "license": "LGPL-3",
    "data": [
        "security/food_security.xml",
        "security/ir.model.access.csv",
        "data/food_base_automation.xml",
        "views/food_week_views.xml",
        "views/food_order_views.xml",
        "views/food_day_views.xml",
        "views/food_product_views.xml",
        "views/food_reservation_menus.xml",
        "views/food_crons.xml"
    ],
}
