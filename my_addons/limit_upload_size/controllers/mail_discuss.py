from odoo import http, _
from odoo.http import request
from odoo.addons.mail.controllers.discuss import DiscussController
from odoo.exceptions import AccessError, UserError
import json


class CustomDiscussController(DiscussController):

    @http.route('/mail/attachment/upload', methods=['POST'], type='http', auth='public')
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        channel_partner = request.env['mail.channel.partner']
        if thread_model == 'mail.channel':
            channel_partner = request.env['mail.channel.partner']._get_as_sudo_from_request_or_raise(
                request=request, channel_id=int(thread_id))
        vals = {
            'name': ufile.filename,
            'raw': ufile.read(),
            'res_id': int(thread_id),
            'res_model': thread_model,
        }
        if is_pending and is_pending != 'false':
            # Add this point, the message related to the uploaded file does
            # not exist yet, so we use those placeholder values instead.
            vals.update({
                'res_id': 0,
                'res_model': 'mail.compose.message',
            })
        if channel_partner.env.user.share:
            # Only generate the access token if absolutely necessary (= not for internal user).
            vals['access_token'] = channel_partner.env['ir.attachment']._generate_access_token()
        try:
            file_size = len(vals['raw'])
            ResConfig = request.env['res.config.settings']
            default_values = ResConfig.default_get(['max_attachment_size'])
            max_attachment_size = default_values.get(
                'max_attachment_size', 0)
            max_file_size = max_attachment_size * 1024 * 1024  # Convert MB to bytes

            if file_size > max_file_size:
                # Raise UserError to jump to except block
                raise UserError(_("The raw file exceeds the maximum size limit of %s MB.") % (
                    max_attachment_size))

            attachment = channel_partner.env['ir.attachment'].create(vals)
            attachment._post_add_create()
            attachmentData = {
                'filename': ufile.filename,
                'id': attachment.id,
                'mimetype': attachment.mimetype,
                'name': attachment.name,
                'size': attachment.file_size
            }
            if attachment.access_token:
                attachmentData['accessToken'] = attachment.access_token

        except AccessError:
            attachmentData = {'error': _(
                "You are not allowed to upload an attachment here.")}
        except UserError as e:
            # Capture the error message from UserError
            attachmentData = {'error': str(e)}

        return request.make_response(
            data=json.dumps(attachmentData),
            headers=[('Content-Type', 'application/json')]
        )

    # @http.route('/mail/attachment/upload', methods=['POST'], type='http', auth='public')
    # def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
    #     raw_data = ufile.read()
    #     file_size = len(raw_data)
    #     print("...................THIS IS FILE SIZE::::::::: ", file_size)

    #     ResConfig = request.env['res.config.settings']
    #     default_values = ResConfig.default_get(['max_attachment_size'])
    #     max_attachment_size = default_values.get(
    #         'max_attachment_size', 0)
    #     max_file_size = max_attachment_size * 1024 * 1024  # Convert MB to bytes

    #     if file_size > max_file_size:
    #         attachmentData = {'error': _(f"The raw file exceeds the maximum size limit of {
    #                                      max_file_size / (1024 * 1024)} MB.")}
    #         return request.make_response(
    #             data=json.dumps(attachmentData),
    #             headers=[('Content-Type', 'application/json')]
    #         )
    #     # Call the original `mail_attachment_upload` method to process the upload
    #     response = super(DiscussController, self).mail_attachment_upload(
    #         ufile, thread_id, thread_model, is_pending=is_pending, **kwargs)

    #     # Debugging response from super
    #     print("Super response:", response)
    #     return response
