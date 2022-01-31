from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.operators import ColumnOperators
from app.db import db
from app.models.system_config import SystemConfig
from app.models.colour import Colour
from app.helpers.auth import authenticated
from app.helpers.permission import check_permission
from app.resources.utils.utils import get_url_parameters_v2
from app.services.authentication_service import AuthenticationService
from app.services.permission_service import PermissionService 

def configuration():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"configuration_show") 

    config = SystemConfig.get_config()
    col = Colour.all()
    return render_template("configuration/configuration.html",config=config, col=col)

def save_configuration():
    
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"configuration_show") 
    
    if request.form:
        parameters = get_url_parameters_v2(request.form, [ "title", "number", "colour", "criteria"])
        message = SystemConfig.update_config(parameters)
        SystemConfig.update_session_criteria(parameters["criteria"])
        Colour.update_session_colour(parameters['colour'])
        flash(message["message"], message["category"])
    return redirect(url_for("configuration"))
