from flask import request , render_template, flash , redirect , url_for
from sqlalchemy.sql.expression import null

from app.services.authentication_service import AuthenticationService
from app.services.denunciation_service import DenunciationService
from app.services.permission_service import PermissionService
from app.models.system_config import SystemConfig
from app.services.paginate_service import PaginateService
from app.resources.utils.utils import get_parameters, get_filters, get_dates_parameters, get_url_parameters_v2

def index():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_index")
    denunciation_per_page = SystemConfig.get_elements_per_page()
    parameters = get_parameters(request.args)
    selected_filter = get_filters(parameters)
    filter_dates = get_dates_parameters(request.args)
    page_number = parameters['page']
    denunciations = DenunciationService.get_all()
    denunciations_states = DenunciationService.get_all_states()
    filtered_collection = DenunciationService.get_filtered_denunciations(denunciations, selected_filter)
    print("fechas", filter_dates['from_date'])
    print("tipo fechas", type(filter_dates['from_date']))
    if (filter_dates['from_date'] != ''):
        if(type(filter_dates['from_date']) is not type(None)):
            filtered_collection = DenunciationService.get_filtered_denunciations_by_date(denunciations, filter_dates)
    paginated_collection = PaginateService.paginate_collection(
        filtered_collection, page_number, denunciation_per_page)
    print(paginated_collection, "paginated")    
    return render_template("/admin_views/denunciations.html",denunciations=paginated_collection, page_number=page_number, active=parameters['active'], search=parameters['search'], denunciations_states=denunciations_states, from_date=filter_dates['from_date'], to_date=filter_dates['to_date'] )

def add_denunciation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_new")

    categories = DenunciationService.get_categories() 
    users = DenunciationService.get_users()
    denunciation_states = DenunciationService.get_states()

    return render_template("admin_views/add_denunciation.html", categories=categories, users=users, denunciation_states=denunciation_states)

def new_denunciation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_new")

    parameters = get_url_parameters_v2(request.form, ["title","category_id","denunciation_state_id","first_name_d","last_name_d","phone_d","email_d","user_id","latitude","longitude","description"])
    message = DenunciationService.add_denunciation(parameters)     
    flash(message['message'], message['category'])

    return redirect("/denunciations?page=1&active=nope&search=&to_date=&from_date=")


def update_denunciation_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_update")
    denunciation = DenunciationService.get_denunciation(id)
    allden = DenunciationService.get_all_denunciations(id)
    denunciation_states = DenunciationService.get_states()
    categories = DenunciationService.get_categories()
    users = DenunciationService.get_users()
    return render_template("admin_views/update_denunciation.html", denunciation=denunciation, allden=allden, denunciation_states=denunciation_states, categories=categories, users=users)


def update_denunciation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_update")
    if request.form:
        parameters = get_url_parameters_v2(request.form, ["denunciation_id","title","category_id","denunciation_state_id","first_name","last_name","phone","email","user_id","latitude","longitude","description"])
        message = DenunciationService.update_denunciation(parameters)
        flash(message['message'], message['category'])
    return redirect("/denunciations?page=1&active=nope&search=&to_date=&from_date=")

def delete_denunciation(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_destroy")
    message = DenunciationService.delete_denunciation(id)
    flash(message['message'], message['category'])
    return redirect("/denunciations?page=1&active=nope&search=&to_date=&from_date=", code=302)

def register_attempt(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_index")
    message = DenunciationService.reg_attempt(id)
    flash(message['message'], message['category'])
    return redirect("/denunciations?page=1&active=nope&search=&to_date=&from_date=", code=302)