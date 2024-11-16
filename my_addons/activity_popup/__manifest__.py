{
    "name": "New Activities",
    'depends': ['base', 'mail', 'web'],
    "category": "Settings/Custom",
    "license": "LGPL-3",
    "data": [
        "data/activity_popup.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "activity_popup/static/src/js/activity_popup.js",
            # "activity_popup/static/src/xml/activity_popup.xml"
        ],
        'web.assets_qweb': [
            # "activity_popup/static/src/xml/activity_popup.xml"
        ],

    },
}
