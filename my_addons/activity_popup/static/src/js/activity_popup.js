odoo.define('activity_popup.ActivityPopup', function(require) {
    "use strict";
    
    let AbstractAction = require('web.AbstractAction');
    let rpc = require('web.rpc'); // RPC : remote procedure call -> call server-side functions
    let Dialog = require('web.Dialog'); // Dialog Widget -> creat modals(popups)

    AbstractAction.include({
        start: function() { // extend when action start
            this._super.apply(this, arguments); //preserving default behavior.

            rpc.query({
                route: '/activities_popup/get',
                params: {},
            }).then(function(result) {
                if (result.show_popup && result.activities.length > 0) {
                    let content = $('<div>', { css: { display: 'flex', flexWrap: 'wrap', gap: '15px', marginTop: '15px' } });

                    result.activities.forEach(function(activity) {
                        const res_record_url = `/web#id=${activity.res_id}&model=${activity.res_model_id}&view_type=form`;
                        let activityCard = $('<a>', {
                            href: res_record_url,
                            css: { textDecoration: 'none', color: 'inherit', flex: '1 1 calc(33.333% - 10px)' }
                        }).append(
                            $('<div>', { css: { padding: '15px', border: '1px solid #e0e0e0', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', marginBottom: '15px' } })
                                .append($('<div>', { css: { fontSize: '1.1em', fontWeight: 'bold', color: '#333', marginBottom: '5px' }, text: activity.activity_type }))
                                .append($('<div>').html(`<span style="font-weight: bold; color: #666;">Summary:</span> ${activity.summary}`))
                                .append($('<div>').html(`<span style="font-weight: bold; color: #666;">Due Date:</span> <span style="color: #0073e6;">${activity.date_deadline}</span>`))
                                .append($('<div>', { css: { color: '#555' }, html: `<span style="font-weight: bold;">Note:</span> ${activity.note}` }))
                                .append($('<div>', { css: { color: '#555' }, html: `<span style="font-weight: bold;">Create Date:</span> ${activity.create_date}` }))
                        );
                        
                        content.append(activityCard);
                    });
                    
                    const dialog = new Dialog(null, {
                        title: "Your New Activities",
                        size: 'large',
                        $content: $('<div>').html(content),
                    });
            
                    // Open the dialog and add a custom button to the header
                    dialog.opened().then(function() {
                        // Create the button and set its properties
                        const customButton = $('<button>', {
                            text: 'Go to Activities Overview',
                            class: 'btn btn-primary',
                            click: function() {
                                window.location.href = '/web#cids=1&menu_id=4&action=121&model=mail.activity&view_type=list';
                            }
                        });
                        
                        // Append the button to the dialog's header
                        dialog.$modal.find('.modal-title').append(customButton);
                    });
            
                    dialog.open();
                }
                if(result.show_popup && result.activities.length == 0){
                    new Dialog(null, {
                        title: "Your New Activities",
                        size: 'large',
                        $content:` <div style="text-align: center; padding: 20px; margin: 50px 0">
                        <h2>All Caught Up!</h2>
                        <p style="font-size: 16px; color: #777;"> Great job! You have no new activities since your last visit. </p> </div> `,
                    }).open();

                }
            });
        }
    });
});

// odoo.define('your_module.ActivityPopup', function(require) {
//     "use strict";
    
//     let AbstractAction = require('web.AbstractAction');
//     let rpc = require('web.rpc');
//     let Dialog = require('web.Dialog');
//     let core = require('web.core');
//     let QWeb = core.qweb;

//     AbstractAction.include({
//         start: function() {
//             this._super.apply(this, arguments);

//             rpc.query({
//                 route: '/activities_popup/get',
//                 params: {},
//             }).then(function(result) {
//                 if (result.show_popup && result.activities.length > 0) {
//                     let content = $('<div>').css({
//                         display: 'flex', 
//                         flexWrap: 'wrap', 
//                         gap: '15px', 
//                         marginTop: '15px'
//                     });
//                     console.log("-------------------------before render qweb");
//                     result.activities.forEach(function(activity) {
//                         let activityCardHtml = QWeb.render('activity_popup.activity_card_template', { activity: activity });
//                         content.append(activityCardHtml);
//                     });

//                     new Dialog(null, {
//                         title: "Your Activities",
//                         size: 'large',
//                         $content: content,
//                     }).open();
//                 } else if (result.show_popup && result.activities.length == 0) {
//                     new Dialog(null, {
//                         title: "Your Activities",
//                         size: 'large',
//                         $content: $("<h1>You do not have any new activities from the last time you visited</h1>"),
//                     }).open();
//                 }
//             });
//         }
//     });
// });
