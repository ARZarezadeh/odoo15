odoo.define('your_module.ActivityPopup', function(require) {
    "use strict";
    
    let AbstractAction = require('web.AbstractAction');
    let rpc = require('web.rpc');
    let Dialog = require('web.Dialog');

    AbstractAction.include({
        start: function() {
            this._super.apply(this, arguments);

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
                        // Generate the link to the activity record
                        const activityUrl = `/web#id=${activity.id}&menu_id=4&action=121&model=mail.activity&view_type=form`;

                        content += `
                            <a href="${activityUrl}" style="text-decoration: none; color: inherit; flex: 1 1 calc(33.333% - 10px);">
                                <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 15px; box-sizing: border-box;">
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
                                        <span style="font-weight: bold;">Create Date:</span> ${activity.create_date}
                                    </div>
                                </div>
                            </a>
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
