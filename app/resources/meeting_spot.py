from flask import request , render_template, flash , redirect , url_for
from app.models.state import Status
from app.resources.utils.utils import get_filters, get_parameters, get_url_parameters_v2

from app.services.authentication_service import AuthenticationService
from app.services.meeting_spot_service import MeetingSpotService
from app.services.permission_service import PermissionService
from app.models.system_config import SystemConfig
from app.models.colour_map import ColourMap
from app.services.paginate_service import PaginateService


def meetingspots():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_index")
    spots_per_page = SystemConfig.get_elements_per_page()
    parameters = get_parameters(request.args)
    selected_filter = get_filters(parameters)
    page_number = parameters['page']
    spots = MeetingSpotService.get_all_meetingspots()
    filtered_collection = MeetingSpotService.get_filtered_meeting_spots(spots, selected_filter)
    paginated_collection = PaginateService.paginate_collection(
        filtered_collection, page_number, spots_per_page)
    return render_template("admin_views/meetingspots.html",meetingspots= paginated_collection, page_number=page_number, status=parameters['active'], search=parameters['search'] )

def add_meetingspot():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_new")
    states = MeetingSpotService.get_states()
    return render_template("admin_views/add_meetingspot.html", states=states)

def new_meetingspot():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_new")

    parameters = get_url_parameters_v2(request.form, ["name","email","phone","status","address","latitude","longitude"])
    message = MeetingSpotService.add_meetingspot(parameters)     
    flash(message['message'], message['category'])

    return redirect("/meetingspots", code=302)

def update_meetingspot_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_update")
    meetingspot = MeetingSpotService.get_meetingspot(id)
    states = MeetingSpotService.get_states()
    all_meetingspots = MeetingSpotService.get_all(id)
    return render_template("admin_views/update_meetingspot.html", meetingspot= meetingspot, states=states, all=all_meetingspots)

def update_meetingspot():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_update")
    if request.form:
        parameters = get_url_parameters_v2(request.form, ["meetingspot_id","name","address","email","phone","status","latitude","longitude"])
        message = MeetingSpotService.update_meetingspot(parameters)
        flash(message['message'], message['category'])
    return redirect(url_for("meetingspot_index", id=parameters["meetingspot_id"]))
    
def delete_meetingspot(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"meeting_spot_destroy")
    message = MeetingSpotService.delete_meetingspot(id)
    flash(message['message'], message['category'])
    return redirect("/meetingspots", code=302)

   