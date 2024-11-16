from odoo import http
from odoo.http import request


class ActivityPopupController(http.Controller):

    @http.route('/activities_popup/get', type='json', auth='user')
    def check_popup_status(self):
        # popup_shown Flag for checking if it is first time seeing popup after login or not
        if not request.session.get('popup_shown'):

            # index zero is the current time(login just now), then first index is for previous login
            last_login_date = request.env.user.log_ids[1].create_date
            if last_login_date:
                activities = request.env['mail.activity'].search([
                    ('user_id', '=', request.env.user.id),
                    ('activity_type_id', '!=', False),
                    ('create_date', '>', last_login_date),
                ])

                request.session['popup_shown'] = True

                activity_data = [{
                    'activity_type': activity.activity_type_id.name,
                    'summary': activity.summary,
                    'date_deadline': activity.date_deadline,
                    'note': activity.note,
                    'create_date': activity.create_date,
                    'id': activity.id,
                    'res_model_id': activity.res_model_id.model,
                    'res_id': activity.res_id
                } for activity in activities]

                return {'show_popup': True, 'activities': activity_data}

        print("already seen")
        return {'show_popup': False}
