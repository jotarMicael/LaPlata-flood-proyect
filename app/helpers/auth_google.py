from flask import redirect, request, url_for, session, flash
from os import environ
from app.models.system_config import SystemConfig
import requests
from app.db import db
from oauthlib.oauth2 import WebApplicationClient
from app.models.user import User

from app.models.system_config import SystemConfig
from app.models.colour import Colour
from app.services.user_service import UserService
import json
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Micael Configuration
GOOGLE_CLIENT_ID = "989274173980-ucahllq38fcd0qq9002pt7pch5skbmt8.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def login():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/login/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

def register():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/register/callback_r",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


def callback():

    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "El mail del usuario no está disponible o no está verificado por Google.", 400

    user = User(
        first_name=users_name, email=users_email, active=0
    )

    print(userinfo_response.json())

    if not UserService.find_by_email(users_email):
        flash("Este email NO se encuentra registrado en el sistema")
        return redirect(url_for("auth_login"))

    if UserService.get_active(users_email):

        user = User.query.filter(
            User.email == users_email
        ).first()
        session["user"] = user.email

        config = SystemConfig.query.filter_by(active=1).first()
        colour_hexa = Colour.get_hexa(config.colour_id)
        session["hexa"] = colour_hexa
        session["criteria"] = config.criteria

        user.active_role = 'operator'
        db.session.commit()
        roles = {role.id: role.name for role in user.roles}
        session["roles"] = roles

        session["actual_role"] = 'operator'

        flash("La sesión se inició correctamente.")
        return redirect(url_for("panel"))

    flash("Su cuenta se encuentra en pendiente de aprobación")
    return redirect(url_for("auth_login"))


def callback_r():

    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "El mail del usuario no está disponible o no está verificado por Google.", 400

    user = User(
        first_name=users_name, email=users_email, active=0
    )

    print(userinfo_response.json())

    if  UserService.find_by_email(users_email):  
         flash("Este email ya se encuentra registrado en el sistema")
         return redirect(url_for("auth_login"))

    UserService.create(users_name, users_email)

    flash("¡Registro Exitoso, para iniciar sesion deberá esperar que su cuenta sea habilitada!")
    return redirect(url_for("auth_login"))
