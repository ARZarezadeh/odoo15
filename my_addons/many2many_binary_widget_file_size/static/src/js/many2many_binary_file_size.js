odoo.define('many2many_binary_widget_file_size.Many2ManyBinaryWithFileSize', function (require) {
    'use strict';
    console.log("Custom many2many_binary widget loaded");
    const FieldMany2ManyBinaryMultiFiles = require('web.relational_fields').FieldMany2ManyBinaryMultiFiles;
    const rpc = require('web.rpc');

    const Many2ManyBinaryWithFileSize = FieldMany2ManyBinaryMultiFiles.extend({
        _render: function () {
            this._super.apply(this, arguments);

            // Delay the appending process to ensure rendering is complete
            setTimeout(() => {
                if (this.value) {
                    this.value.data.forEach((attachmentData, index) => {
                        const attachmentId = attachmentData.data.id;
                        
                        // Fetch the attachment record with the file size
                        rpc.query({
                            model: 'ir.attachment',
                            method: 'read',
                            args: [[attachmentId], ['file_size']],
                        }).then(result => {
                            const attachment = result[0];
                            if (attachment && attachment.file_size) {
                                const sizeInKB = (attachment.file_size / 1024).toFixed(2);
                                const sizeDisplay = `${sizeInKB} KB`;
                                console.log("size display: ", sizeDisplay)
                                // Append file size to each attachment display
                                this.$('.o_attachment_wrap').eq(index).append(
                                    `<span class="o_attachment_file_size caption small"> (${sizeDisplay})</span>`
                                );
                            }
                        }).catch(err => {
                            console.error("Failed to fetch file size for attachment:", err);
                        });
                    });
                }
            }, 0); // Set a minimal delay to let the DOM render first
        },
    });

    // Register the new widget
    const registry = require('web.field_registry');
    registry.add('many2many_binary_file_size', Many2ManyBinaryWithFileSize);

    return Many2ManyBinaryWithFileSize;
});
