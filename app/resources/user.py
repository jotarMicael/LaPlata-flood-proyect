from flask import redirect, render_template, request, url_for, session, abort, flash 

from app.db import db
from app.models.user import User
from app.models.system_config import SystemConfig
from app.helpers.auth import authenticated
from app.services.authentication_service import AuthenticationService
from app.services.paginate_service import PaginateService
from app.services.filter_service import FilterService
from app.helpers.permission import check_permission
from app.models.role import Role
from app.models.user_role import UserRole
from app.resources.utils.utils import get_url_parameters_v2, get_parameters, get_filters
from app.services.permission_service import PermissionService 
from app.services.user_service import UserService


def index():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_index") 

    parameters = get_parameters(request.args)
    selected_filter = get_filters(parameters)
    users = UserService.get_users()
    filtered_collection = FilterService.apply_filter(users, selected_filter)
    users_per_page = SystemConfig.get_elements_per_page()
    page_number = parameters['page']
    paginated_collection = PaginateService.paginate_collection(
        filtered_collection, page_number, users_per_page)
    return render_template("admin_views/user_list.html", users=paginated_collection, page_number=page_number, search=parameters['search'], active=parameters['active'])


def new():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_new") 

    roles = Role.query.filter(Role.active==1).all()

    return render_template("admin_views/add_user.html", roles=roles)


def create():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_new") 

    params = request.form
    user = User.query.filter(
        User.email == params.get("email")
    ).first()

    if user:
        flash("El usuario ya se encuentra cargado.")
        return redirect(url_for("user_new"))

    roles = params.getlist('role')

    if params.get("active") == '1':
        user = User(first_name=params.get("first_name"), last_name=params.get("last_name"),
        password=params.get("password"), email=params.get("email"), username=params.get("username") , active=True
        )
    else:
        user = User(first_name=params.get("first_name"), last_name=params.get("last_name"),
        password=params.get("password"), email=params.get("email"), username=params.get("username") , active=False
        )

    db.session.add(user)
    db.session.commit()
    db.session.flush()
    for role in roles:
        db.session.add(UserRole(role_id=role, user_id=user.id))
        db.session.commit()
    flash("¡Usuario agregado exitosamente!")
    return redirect(url_for("user_index"))


def update_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_update") 
 
    user = UserService.get_user(id)
    roles = Role.query.filter(Role.active==1).all()
    return render_template("admin_views/update_user.html", user=user,roles=roles)


def update():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_update") 
    if request.form:
       
        parameters = get_url_parameters_v2(request.form, ["user_id", "password"])
       
        roles= request.form.getlist("role")
        
        message = UserService.update_user(parameters,roles)
        flash(message["message"], message["category"])

        
    return redirect(url_for("user_index"))


def destroy(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_destroy") 

    message = UserService.destroy_user(id)
    flash(message['message'], message['category'])
    return redirect(url_for("user_index"))


def reactivate(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"user_destroy") 

    message = UserService.reactivate_user(id)
    flash(message['message'], message['category'])
    return redirect(url_for("user_index"))
