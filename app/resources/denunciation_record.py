from app.services.authentication_service import AuthenticationService
from app.services.permission_service import PermissionService
from app.models.system_config import SystemConfig
from app.resources.utils import utils
from flask import request, render_template, flash, redirect
from app.services.denunciation_record_service import DenunciationRecordService
from app.services.paginate_service import PaginateService
from app.services.denunciation_service import DenunciationService
from app.resources.utils.utils import get_url_parameters_v2

def index(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_index")
    records_per_page = SystemConfig.get_elements_per_page()
    parameters = utils.get_parameters(request.args)
    page_number = parameters['page']
    records = DenunciationRecordService.get_records_by_id(id)
    paginated_collection = PaginateService.paginate_collection(
        records, page_number, records_per_page)
    return render_template("/admin_views/denunciations_record.html", records=paginated_collection, page_number=page_number, id=id)


def new_record(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_new")
    users = DenunciationService.get_users()
    denunciation = DenunciationRecordService.get_denunciation_and_record(id)
    denunciation_states = DenunciationService.get_states()
    return render_template("admin_views/add_denunciation_record.html", users=users, id=id, den=denunciation, denunciation_states=denunciation_states)

def add_denunciation_record(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_new")

    parameters = get_url_parameters_v2(request.form, ["title", "user_id", "denunciation_state_id"])
    message = DenunciationRecordService.add_denunciation_record(parameters, id)     
    flash(message['message'], message['category'])
    return index(id)

def delete_denunciation_record(id, idD):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"denunciation_destroy")
    message = DenunciationRecordService.delete_denunciation_record(id)
    flash(message['message'], message['category'])
    return index(idD)