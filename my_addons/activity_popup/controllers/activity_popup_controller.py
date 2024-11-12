# from odoo import http
# from odoo.http import request


# class ActivityPopupController(http.Controller):
#     @http.route('/activities_popup/get_activities', type='json', auth='user')
#     def get_user_activities(self):
#         current_user_id = request.env.user.id
#         activities = request.env['mail.activity'].search(
#             [('user_id', '=', current_user_id)])
#         print("ACTIVITIES::::: ", activities)
#         # Prepare activity data for the frontend
#         activity_data = []
#         for activity in activities:
#             activity_data.append({
#                 'res_model': activity.res_model,
#                 'res_id': activity.res_id,
#                 'activity_type': activity.activity_type_id.name,
#                 'summary': activity.summary,
#                 'date_deadline': activity.date_deadline,
#                 'note': activity.note,
#             })
#         return activity_data

from odoo import http
from odoo.http import request


class ActivityPopupController(http.Controller):

    @http.route('/activities_popup/get', type='json', auth='user')
    def check_popup_status(self):
        # Check if popup has already been shown in this session
        if not request.session.get('popup_shown'):
            # Get the last login date of the current user
            print("this is first time that user seee......",
                  request.env.user.log_ids[1].create_date)
            last_login_date = request.env.user.log_ids[1].create_date
            print("this is last login date: ", last_login_date)
            if last_login_date:
                # Fetch activities for the current user created after last login
                activities = request.env['mail.activity'].search([
                    ('user_id', '=', request.env.user.id),
                    ('activity_type_id', '!=', False),
                    ('create_date', '>', last_login_date),
                ])
                print("________ activities:::", activities)
                # Mark popup as shown in the session
                request.session['popup_shown'] = True

                # Prepare activity data to return to JavaScript
                activity_data = [{
                    'activity_type': activity.activity_type_id.name,
                    'summary': activity.summary,
                    'date_deadline': activity.date_deadline,
                    'note': activity.note,
                    'create_date': activity.create_date
                } for activity in activities]

                return {'show_popup': True, 'activities': activity_data}

        # If already shown, return show_popup as False
        print("already seen")
        return {'show_popup': False}
