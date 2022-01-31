from flask import request , render_template, flash , redirect , url_for

from werkzeug.utils import secure_filename
import os
from app.models.evacuation_route import EvacuationRoute
from app.resources.utils.utils import get_filters, get_parameters, get_url_parameters_v2

from app.services.authentication_service import AuthenticationService
from app.services.evacuation_routes_service import EvacuationRouteService
from app.services.permission_service import PermissionService
from app.models.system_config import SystemConfig
from app.models.colour_map import ColourMap
from app.services.paginate_service import PaginateService


def get_array_coordenadas (latitudes,longitudes):
    array_coordenadas = []
    for i in range(0,len(latitudes),1):
        coordenada_aux = latitudes[i]+","+longitudes[i]
        array_coordenadas.append(coordenada_aux)
    return array_coordenadas

def evacuations():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_show")
    routes_per_page = SystemConfig.get_elements_per_page()
    parameters = get_parameters(request.args)
    selected_filter = get_filters(parameters)
    page_number = parameters['page']
    routes = EvacuationRouteService.get_all_evacuation_routes()
    filtered_collection = EvacuationRouteService.get_filtered_evacuation_routes(routes, selected_filter)
    paginated_collection = PaginateService.paginate_collection(
    filtered_collection, page_number, routes_per_page)
    print('__________________paginated collection_______________: ',paginated_collection.items)
    return render_template("admin_views/evacuation_routes.html",evacuation_routes= paginated_collection, page_number=page_number, status=parameters['active'], search=parameters['search'] )

def add_evacuation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_new")
    return render_template("admin_views/add_evacuation_route.html")

def new_evacuation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_new")
    parameters = get_url_parameters_v2(request.form, ["name","latitude","longitude","status","description","latitudesTotal","longitudesTotal"])
    latitudesTotal = parameters.get('latitudesTotal')
    longitudesTotal = parameters.get('longitudesTotal')
    arregloLatitudes = latitudesTotal.split('|')
    arregloLongitudes = longitudesTotal.split('|')
    arregloCoordenadas = get_array_coordenadas(arregloLatitudes,arregloLongitudes)
    message = EvacuationRouteService.add_evacuationroute(parameters,arregloCoordenadas)     
    flash(message['message'], message['category'])
    return redirect("/evacuations")

def delete_evacuation(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_destroy")
    message = EvacuationRouteService.delete_evacuationroute(id)
    flash(message['message'], message['category'])
    return redirect("/evacuations")

def update_evacuation_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_update")
    evacuationroute = EvacuationRouteService.get_evacuationroute(id)
    return render_template("admin_views/update_evacuationroute.html", evacuation_route= evacuationroute)

def update_evacuation():
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_update")
    if request.form:
        parameters = get_url_parameters_v2(request.form, ["evacuation_route_id","name","latitude","longitude","status","description","latitudesTotal","longitudesTotal"])
        latitudesTotal = parameters.get('latitudesTotal')
        longitudesTotal = parameters.get('longitudesTotal')
        arregloLatitudes = latitudesTotal.split('|')
        arregloLongitudes = longitudesTotal.split('|')
        arregloCoordenadas = get_array_coordenadas(arregloLatitudes,arregloLongitudes)
        message = EvacuationRouteService.modify_evacuationroute(parameters,arregloCoordenadas)    
        flash(message['message'], message['category'])
    return redirect("/evacuations")

def evacuation_view(id):
    user_email = AuthenticationService.check_authentication()
    PermissionService.check_permission(user_email,"evacuation_show")
    evacuation_coordinates = EvacuationRouteService.get_all_evacuation_coordinates(id)
    evacuation_route = EvacuationRouteService.get_evacuationroute(id);
    name = evacuation_route.name
    # colour1 = ColourMap.get_colour(colour_id)
    # falta mandar el color en la renderizacion
    return render_template("admin_views/evacuation_route_view.html",  evacuation_coordinates=evacuation_coordinates, name=name)
      
    