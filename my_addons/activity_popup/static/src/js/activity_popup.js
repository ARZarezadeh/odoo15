// odoo.define('your_module.ActivityPopup', function(require) {
//     "use strict";
    
//     let AbstractAction = require('web.AbstractAction');
//     let session = require('web.session');
//     let rpc = require('web.rpc');
//     let Dialog = require('web.Dialog');

//     AbstractAction.include({
//         start: function() {
//             this._super.apply(this, arguments);

//             // Only trigger on first load when user logs in
//             console.log("---------------activity_popup_shown", localStorage.getItem("activity_popup_shown"));
//             if (session.is_bound && session.uid && !localStorage.getItem("activity_popup_shown")) {
//                 this._showActivitiesPopup();
//                 localStorage.setItem("activity_popup_shown", "true");  // Set flag to avoid repeat popups
//             }
//         },

//         _showActivitiesPopup: function() {
//             rpc.query({
//                 route: '/activities_popup/get_activities',
//                 params: {},
//             }).then(function(activities) {
//                 if (activities.length > 0) {
//                     let content = "<ul>";
//                     activities.forEach(function(activity) {
//                         content += `<li><strong>Type:</strong> ${activity.activity_type}<br>`;
//                         content += `<strong>Summary:</strong> ${activity.summary}<br>`;
//                         content += `<strong>Due Date:</strong> ${activity.date_deadline}<br>`;
//                         content += `<strong>Note:</strong> ${activity.note}<br><br></li>`;
//                     });
//                     content += "</ul>";

//                     new Dialog(null, {
//                         title: "Your Activities",
//                         size: 'large',
//                         $content: $('<div>').html(content),
//                     }).open();
//                 }
//             });
//         },
//     });
// });

// // Define WebClient modification separately
// odoo.define('your_module.WebClientLogout', function(require) {
//     "use strict";
    
//     let WebClient = require('web.WebClient');

//     WebClient.include({
//         logout: function() {
//             localStorage.removeItem("activity_popup_shown");  // Clear flag on logout
//             return this._super.apply(this, arguments);
//         }
//     });
// });

odoo.define('your_module.ActivityPopup', function(require) {
    "use strict";
    
    let AbstractAction = require('web.AbstractAction');
    let rpc = require('web.rpc');
    let Dialog = require('web.Dialog');

    AbstractAction.include({
        start: function() {
            this._super.apply(this, arguments);

            // Query the backend to check if the popup should be shown
            rpc.query({
                route: '/activities_popup/get',
                params: {},
            }).then(function(result) {
                if (result.show_popup && result.activities.length > 0) {
                    let content =  ``
                    content += `
                    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
                    `;
                result.activities.forEach(function(activity) {
                    content += `
                        <div style="flex: 1 1 calc(33.333% - 10px); padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 15px; box-sizing: border-box;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #333; margin-bottom: 5px;">
                                ${activity.activity_type}
                            </div>
                            <div style="margin: 5px 0;">
                                <span style="font-weight: bold; color: #666;">Summary:</span> ${activity.summary}
                            </div>
                            <div style="margin: 5px 0;">
                                <span style="font-weight: bold; color: #666;">Due Date:</span> 
                                <span style="color: #0073e6;">${activity.date_deadline}</span>
                            </div>
                            <div style="margin: 5px 0; color: #555;">
                                <span style="font-weight: bold;">Note:</span> ${activity.note}
                            </div>
                            <div style="margin: 5px 0; color: #555;">
                                <span style="font-weight: bold;">Note:</span> ${activity.create_date}
                            </div>
                        </div>
                    `;
                });
                content += `</div>`;                    
                    new Dialog(null, {
                        title: "Your Activities",
                        size: 'large',
                        $content: $('<div>').html(content),
                    }).open();
                }
                if(result.show_popup && result.activities.length == 0){
                    new Dialog(null, {
                        title: "Your Activities",
                        size: 'large',
                        $content: "<h1>You Do not have any new activities from last time you visit</h1>",
                    }).open();

                }
            });
        }
    });
});
