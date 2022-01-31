from flask import redirect, render_template, request, url_for, abort, session, flash
from app.db import db 
from app.models.user import User
from app.models.system_config import SystemConfig
from app.models.colour import Colour
from app.resources.utils.utils import get_url_parameters_v2
from app.services.authentication_service import AuthenticationService
from app.services.user_service import UserService


def login():
    return render_template("auth/login.html")


def authenticate():
    
    params = request.form

    user = UserService.find_by_email_and_pass(params["email"],params["password"])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
   
    if user.active == 0:
        flash("Su cuenta se encuentra bloqueada")
        return redirect(url_for("auth_login"))

    user = User.query.filter(
        User.email == params["email"] and User.password == params["password"] and User.active
    ).first()

    session["user"] = user.email
    
    config= SystemConfig.query.filter_by(active = 1).first()
    colour_hexa= Colour.get_hexa(config.colour_id)
    session["hexa"] = colour_hexa
    session["criteria"] = config.criteria
    
    roles = {role.id: role.name for role in user.roles}
    session["roles"]= roles
    print("los roles je", roles)

    actual_role = next(iter(roles))
    actual_role_aux = (user.active_role)
    session["actual_role"] = {actual_role:actual_role_aux}
    print("el rol actual", session.get("actual_role"))

    
    flash("La sesión se inició correctamente.")

    return redirect(url_for("panel"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))


def update_active_role():
    user_email = AuthenticationService.check_authentication()
    if request.form:
        parameters = get_url_parameters_v2(request.form, ["active_role"])
        message = AuthenticationService.update_active_role(parameters,user_email)
    return redirect("/panel")