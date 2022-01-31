from flask import request , render_template, flash , redirect , url_for

from werkzeug.utils import secure_filename
import os
from app.resources.utils.utils import get_filters, get_parameters, get_url_parameters_v2
from app.services.authentication_service import AuthenticationService
from app.services.flood_zone_service import FloodZoneService
from app.services.permission_service import PermissionService
from app.models.system_config import SystemConfig
from app.models.colour_map import ColourMap
from app.services.paginate_service import PaginateService


def flood_zones():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_index")
    zone_per_page = SystemConfig.get_elements_per_page()
    parameters = get_parameters(request.args)
    selected_filter = get_filters(parameters)
    page_number = parameters['page']
    flood_zones = FloodZoneService.get_all_flood_zones()
    filtered_collection = FloodZoneService.get_filtered_flood_zones(flood_zones, selected_filter)
    paginated_collection = PaginateService.paginate_collection(
        filtered_collection, page_number, zone_per_page)
    return render_template("admin_views/flood_zones.html",flood_zones= paginated_collection, page_number=page_number, status=parameters['active'], search=parameters['search'] )

def new_flood_zones():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_new") 
    f = request.files['csv']
    basepath = os.path.dirname(__file__) # La ruta donde se encuentra el archivo actual
    upload_path = os.path.join(basepath, '../static/uploads', secure_filename (f.filename)) #Nota: Si no hay una carpeta, debe crearla primero, de lo contrario se le preguntará que no existe tal ruta
    f.save(upload_path)
    message = FloodZoneService.add_flood_zones(upload_path)     
    flash(message['message'], message['category'])
    return redirect("/floodzones")

def delete_floodzone(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_destroy")
    message = FloodZoneService.delete_floodzone(id)
    flash(message['message'], message['category'])
    return redirect("/floodzones")

def update_floodzone():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_update")
    if request.form:
        parameters = get_url_parameters_v2(request.form, ["floodzone_id","status","colour"])
        message = FloodZoneService.update_floodzone(parameters)
        flash(message['message'], message['category'])       
    return redirect(url_for("floodzone_index", id=parameters["floodzone_id"]))

def update_floodzone_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_update")
    floodzone = FloodZoneService.get_floodzone(id)   
    colours_map = ColourMap.all()
    set_colour = ColourMap.get_colour(floodzone.colour_map_id)  
    return render_template("admin_views/update_floodzone.html", floodzone= floodzone, colours_map=colours_map,set_colour=set_colour)

def flood_zone_coordinates_view(id,name,colour_id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_show")
    floodzone_coordinates = FloodZoneService.get_all_flood_zone_coordinates(id)
    colour1 = ColourMap.get_colour(colour_id)
    return render_template("admin_views/flood_zones_coordinates.html",  floodzone_coordinates=floodzone_coordinates, name=name, colour=colour1)
      
def update_floodzone_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"flood_zone_update")
    floodzone = FloodZoneService.get_floodzone(id)   
    colours_map = ColourMap.all()
    set_colour = ColourMap.get_colour(floodzone.colour_map_id)  
    return render_template("admin_views/update_floodzone.html", floodzone= floodzone, colours_map=colours_map,set_colour=set_colour)
