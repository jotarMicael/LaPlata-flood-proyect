from os import error, path, environ, urandom
import re

from flask import Flask, request, render_template, g, jsonify
from flask_session import Session
from sqlalchemy.orm import immediateload
from sqlalchemy.sql.operators import endswith_op
from app.models.category import Category
from app.models.colour import Colour
from app.models.colour_map import ColourMap
from app.models.evacuation_route_coordinate import EvacuationRouteCoordinate
from app.models.flood_zone import FloodZone
from app.models.flood_zone_coordinate import FloodZoneCoordinate
from app.services.denunciation_service import DenunciationService
from app.services.evacuation_routes_service import EvacuationRouteService
from app.services.flood_zone_service import FloodZoneService
from app.services.meeting_spot_service import MeetingSpotService
from app.services.user_service import UserService
from config import config
from app.db import db
from app.resources import evacuation as evacuation_controller
from app.resources import flood_zone as floodzone_controller
from app.resources import meeting_spot as meetingspot_controller
from app.resources import denunciation as denunciation_controller
from app.resources import denunciation_record as denunciation_record_controller
from app.resources import auth
from app.resources import user
from app.resources import configuration

from app.helpers import auth as helper_auth

from app.helpers import auth_google
from app.helpers import handler
from app.helpers.permission import check_permission
from flask_cors import CORS


import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, resources={r"*":{"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'


    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)

    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    conf = app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        conf["DB_USER"]+":"+conf["DB_PASS"]+"@" + \
        conf["DB_HOST"]+"/"+conf["DB_NAME"]
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

    # Creacion BD SQLAlchemy
    with app.app_context():
        from app.models import user as userModel
        from app.models import user_role as userRole
        from app.models import role as role
        from app.models import role_permission as rolePermission
        from app.models import permission as permission
        from app.models import meeting_spot as meetingSpot
        from app.models import state as state
        from app.models import system_config as systemConfig
        from app.models import colour as colour
        from app.models import colour_map as colour_map
        from app.models import flood_zone as floodZone
        from app.models import denunciation as denunciation
        from app.models import denunciation_state as denunciationState
        from app.models import category as denunciationCategory
        from app.models import evacuation_route as evacuationRoute
        from app.models import denunciation_record as denunciationRecord
        from app.models import flood_zone_coordinate as floodZoneCoordinate
        from app.models import evacuation_route_coordinate as evacutationRouteCoordinate

        db.create_all()

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=check_permission)

    # Autenticación
    app.add_url_rule("/login", "auth_login", auth.login)
    app.add_url_rule("/logout", "auth_logout", auth.logout)
    app.add_url_rule("/autenticacion", "auth_authenticate",
                     auth.authenticate, methods=["POST"])
    app.add_url_rule("/update_active_role", "update_active_role",
                     auth.update_active_role, methods=["POST"])

    app.add_url_rule("/login/google", "auth_login_google", auth_google.login)
    app.add_url_rule("/register/google", "register_google", auth_google.register)
    app.add_url_rule(
        "/login/callback", "auth_callback", auth_google.callback, methods=["GET"]
    )
    app.add_url_rule(
        "/register/callback_r", "register_callback", auth_google.callback_r, methods=["GET"]
    )

    # Rutas de Configuración
    app.add_url_rule("/configuration", "configuration",
                     configuration.configuration)
    app.add_url_rule("/configuration", "save_configuration",
                     configuration.save_configuration, methods=["POST"])

    # Rutas de Usuarios
    app.add_url_rule("/users", "user_index", user.index)
    app.add_url_rule("/users/new", "user_new", user.new)
    app.add_url_rule("/users/add", "user_create",
                     user.create, methods=["POST"])
    app.add_url_rule("/users/<id>/update",
                     "user_update_view", user.update_view)
    app.add_url_rule("/users/update", "user_update",
                     user.update, methods=['POST'])
    app.add_url_rule("/users/<id>/delete", "user_destroy", user.destroy)
    app.add_url_rule("/users/<id>/reactivate",
                     "user_reactivate", user.reactivate)

    # Rutas de puntos de encuentro
    app.add_url_rule("/meetingspots", "meetingspot_index",
                     meetingspot_controller.meetingspots)
    app.add_url_rule("/meetingspots/new", "meetingspot_new",
                     meetingspot_controller.add_meetingspot)
    app.add_url_rule("/meetingspots/add", "meetingspot_add",
                     meetingspot_controller.new_meetingspot, methods=['POST'])
    app.add_url_rule("/meetingspots/<id>/update", "meetingspot_update_view",
                     meetingspot_controller.update_meetingspot_view)
    app.add_url_rule("/meetingspots/update", "meetingspot_update",
                     meetingspot_controller.update_meetingspot, methods=['POST'])
    app.add_url_rule("/meetingspots/<id>/delete", "meetingspot_destroy",
                     meetingspot_controller.delete_meetingspot)

    # Rutas de zonas de inundacion
    app.add_url_rule("/floodzones", "floodzone_index",
                     floodzone_controller.flood_zones)
    app.add_url_rule("/floodzones/add", "floodzone_add",
                     floodzone_controller.new_flood_zones, methods=['POST'])
    app.add_url_rule("/floodzones/<id>/update", "floodzone_update_view",
                     floodzone_controller.update_floodzone_view)
    app.add_url_rule("/floodzones/<id>/<name>/<colour_id>/coordinates",
                     "floodzone_coordinates_view", floodzone_controller.flood_zone_coordinates_view)
    app.add_url_rule("/floodzones/update", "floodzone_update",
                     floodzone_controller.update_floodzone, methods=['POST'])
    app.add_url_rule("/floodzones/<id>/delete", "floodzone_destroy",
                     floodzone_controller.delete_floodzone)

    # Denuncias
    app.add_url_rule("/denunciations", "denunciation_index",
                     denunciation_controller.index)
    app.add_url_rule("/denunciations/new", "denunciation_new",
                     denunciation_controller.add_denunciation)
    app.add_url_rule("/denunciations/add", "denunciation_add",
                     denunciation_controller.new_denunciation, methods=['POST'])
    app.add_url_rule("/denunciations/<id>/update", "denunciation_update_view",
                     denunciation_controller.update_denunciation_view)
    app.add_url_rule("/denunciations/update", "denunciation_update",
                     denunciation_controller.update_denunciation, methods=['POST'])
    app.add_url_rule("/denunciations/<id>/delete", "denunciation_destroy",
                     denunciation_controller.delete_denunciation)
    app.add_url_rule("/denunciation_records/<id>",
                     "denunciation_record_index", denunciation_record_controller.index)
    app.add_url_rule("/denunciations_record/new/<id>",
                     "denunciation_record_new", denunciation_record_controller.new_record)
    app.add_url_rule("/denunciations_record/add/<id>", "denunciation_record_add",
                     denunciation_record_controller.add_denunciation_record, methods=['POST'])
    app.add_url_rule("/denunciations_record/<id>/<idD>/delete", "denunciation_record_destroy",
                     denunciation_record_controller.delete_denunciation_record)
    app.add_url_rule("/denunciations/<id>/attempt",
                     "denunciation_attempt", denunciation_controller.register_attempt)

    # Recorridos de evacuacion
    app.add_url_rule("/evacuations", "evacuation_index",
                     evacuation_controller.evacuations)
    app.add_url_rule("/evacuations/new", "evacuation_new",
                     evacuation_controller.add_evacuation)
    app.add_url_rule("/evacuations/add", "evacuation_add",
                     evacuation_controller.new_evacuation, methods=['POST'])
    app.add_url_rule("/evacuations/<id>/delete", "evacuations_destroy",
                     evacuation_controller.delete_evacuation)
    app.add_url_rule("/evacuations/<id>/update", "evacuations_update_view",
                     evacuation_controller.update_evacuation_view)
    app.add_url_rule("/evacuations/update", "evacuations_update",
                     evacuation_controller.update_evacuation, methods=['POST'])
    app.add_url_rule("/evacuations/<id>/view", "evacuations_view",
                     evacuation_controller.evacuation_view)

    # Ruta para el Home (usando decorator)

    @app.route("/")
    def home():
        return render_template("home.html")

    # Ruta para el Panel del Admin (usando decorator)

    @app.route("/panel")
    def panel():
        return render_template("admin-panel/panel.html")

    # Rutas de API-REST (usando Blueprints)
    # api = Blueprint("api", __name__, url_prefix="/api")
    # api.register_blueprint(issue_api)

    # app.register_blueprint(api)

    @app.route('/api/zonas-inundables/<int:id_zone>')
    def flood_zone(id_zone):
        FloodZoneService.get_floodzone(id_zone)
        try:
            flood_zone = FloodZoneService.json_flood_zones(id_zone)
            coordinates = FloodZoneService.get_all_flood_zone_coordinates_2(
                id_zone)
            colour = ColourMap.get_colour_json(flood_zone[0]['colour_map_id'])

            atributos = {
                "id": flood_zone[0]['id'],
                "nombre": flood_zone[0]['nombre'],
                "coordenadas": coordinates,
                "color": colour[0]['color']
            }

            return jsonify(
                {"atributos": atributos}

            )
        except:
            return (500)

    @app.route('/api/zonas-inundables')
    def flood_zones():

        flood_zones = FloodZoneService.json_flood_zones_all()
        try:
            for x in flood_zones:
                coordinates = FloodZoneService.get_all_flood_zone_coordinates_2(
                    x["id"])
                colour = ColourMap.get_colour_json(x["colour_map_id"])
                x.pop('colour_map_id', None)
                x["coordenadas"] = coordinates
                x["color"] = colour[0]['color']
            atr = {
                "zonas": flood_zones,
                "total": len(flood_zones)
            }
            return jsonify(
                atr,
            )
        except:
            return (500)

    def category_exists(id_):
        categories = Category.get_all_categories()
        for c in categories:
            if (int(id_) == c.id):
                return True
        return False

    @app.route('/api/denuncias', methods=['POST'])
    def add_denunciation_api():
  
        json_title = request.json['title']     
        json_category_id = request.json['category_id']         
        json_first_name = request.json['first_name_d']             
        json_last_name = request.json['last_name_d']  
        json_phone = request.json['phone_d']   
        json_email = request.json['email_d'] 
        json_latitude = request.json['latitude'] 
        json_longitude = request.json['longitude']      
        json_description = request.json['description'] 
        
        denuncia = dict({
            'title': json_title,
            'category_id': json_category_id,
            'first_name_d': json_first_name,
            'last_name_d': json_last_name,
            'phone_d': json_phone,
            'email_d': json_email,
            'latitude': json_latitude,
            'longitude': json_longitude,
            'description': json_description
        })

        if (category_exists(json_category_id) == False):
            return 'BAD REQUEST: ID de Categoria no valido!', 400
        message = DenunciationService.add_denunciation_api(denuncia) 
        if (message['category'] == 'error'):
            return 400
        else:
            return jsonify(denuncia)

    @app.route('/api/puntos-encuentro/')
    def puntos_de_encuentro():

        meeting_spots = MeetingSpotService.json_meetingspots()

        try:
            atr = {
                "puntos_encuentro": meeting_spots,
                "total": len(meeting_spots)
            }
            return jsonify(
                atr,
            )
        except:
            return (500)

    @app.route('/api/recorridos-evacuacion/')
    def recorridos_de_evacuacion():

        evacuation_routes = EvacuationRouteService.json_evacuationroutes()

        try:
            for x in evacuation_routes:
                coordinates = EvacuationRouteService.json_evacuationroute_coordinates(
                    x["id"])

                x["coordenadas"] = coordinates
            atr = {
                "recorridos": evacuation_routes,
                "total": len(evacuation_routes)
            }
            return jsonify(
                
                atr,
            )
        except:
            return (500)
    


    @app.route('/api/recorrido-evacuacion/<int:id>')
    def evacuation_route(id):
        try:
            evacuation_route = EvacuationRouteService.json_get_evacuationroute(id)
            print('EVACUATIONNNNNNNNNNN: ',evacuation_route)
            coordinates = EvacuationRouteService.json_evacuationroute_coordinates(id)
            print('COORDINATEEEEEEE: ',coordinates)

            atributos = {
                "id": evacuation_route[0]['id'],
                "name": evacuation_route[0]['name'],
                "coordenadas": coordinates,
                "description": evacuation_route[0]['description']
            }

            return jsonify(
                atributos
            )
        except:
            return (500)


    @app.route('/api/category-types/')
    def category_types():
        category_types = Category.json_categories()

        try:
            atr = {
                "categories": category_types
            }
            return jsonify(
                atr,
            )
        except:
            return (500)


    @app.route('/api/users/')
    def users():
        users = UserService.json_users()

        try:
            atr = {
                "users": users
            }
            return jsonify(
                atr,
            )
        except:
            return (500)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
