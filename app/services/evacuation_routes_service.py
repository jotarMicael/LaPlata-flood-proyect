from sqlalchemy.orm import eagerload
from app.helpers.validation_helper import validate_coordinates, validate_evacuation_route_parameters, validate_meetingspot_parameters
from flask import session
from app.models.evacuation_route import EvacuationRoute
from app.models.evacuation_route_coordinate import EvacuationRouteCoordinate
from app.models.meeting_spot import MeetingSpot
from app.db import db
from flask import abort
from sqlalchemy.sql import func
from sqlalchemy import asc, desc


class EvacuationRouteService:
    
    @classmethod
    def get_all_evacuation_routes(cls):
        if bool(session["criteria"] == "ASC"):
            return EvacuationRoute.query.filter_by(active=1).order_by(asc(EvacuationRoute.name))
        else:
            return EvacuationRoute.query.filter_by(active=1).order_by(desc(EvacuationRoute.name))

    @classmethod
    def get_filtered_evacuation_routes(cls, a_collection, a_filter):
        if a_filter is None:
            return a_collection
        else:
            both = len(a_filter.keys())
            value = list(a_filter.values())[0]
            searched = '%' + func.lower(value) + '%'
            if (both == 2):
                status = list(a_filter.values())[1]
                return a_collection.filter(((EvacuationRoute.state_id) == (status)) & ((func.lower(EvacuationRoute.name).like(searched)) ))
            elif (list(a_filter.keys())[0] == 'search'):
                return a_collection.filter(func.lower(EvacuationRoute.name).like(searched) )
            else:
                status = list(a_filter.values())[0]
                return a_collection.filter((EvacuationRoute.state_id) == status)

        
    @classmethod
    def evacuationroute_exist(cls, parameters):
        return True if len(list(EvacuationRoute.query.filter(EvacuationRoute.name == parameters['name']))) != 0 else False
    

    @classmethod
    def add_evacuationroute(cls, parameters,arreglo_coordenadas):
        result_of_validations = validate_evacuation_route_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        result_of_coordinates_validations = validate_coordinates(arreglo_coordenadas)
        if (not result_of_coordinates_validations['valid']):
            return result_of_coordinates_validations
        if cls.evacuationroute_exist(parameters):
            result_of_validations['message'] = 'No es posible cargar este recorrido de evacuación'
            result_of_validations['category'] = 'error'
            result_of_validations['valid'] = False
            return result_of_validations
        else:
            name = parameters['name']
            description = parameters['description']
            status = parameters['status']
            evacuationroute = EvacuationRoute(name=name, state_id=status, description=description)
            try:
                db.session.add(evacuationroute)
                db.session.flush()
                db.session.refresh(evacuationroute)
                for i in range(0,len(arreglo_coordenadas),1):
                    latitudAux = arreglo_coordenadas[i].split(',')[0]
                    longitudAux = arreglo_coordenadas[i].split(',')[1]
                    print ('entro a for con latitud y longitud: ',latitudAux,longitudAux)
                    evacuation_route_coordinate = EvacuationRouteCoordinate(latitude=latitudAux,longitude=longitudAux,evacuation_route_id=evacuationroute.id)
                    print ('evacuation route coordinate: ',evacuation_route_coordinate)
                    db.session.add(evacuation_route_coordinate)
                db.session.commit()

                return {'message': 'El punto de encuentro fue cargado con exito!', 'category': 'success', 'valid': True}
            except:
                return { 'message': 'El punto de encuentro no pudo ser cargado', 'category': 'error', 'valid': False }

    @classmethod
    def get_evacuationroute(cls, id):
        evacuationroute = EvacuationRoute.query.get(id)
        return evacuationroute if evacuationroute else abort(404)
    
    @classmethod
    def json_get_evacuationroute(cls, id):
        a = db.session.query(EvacuationRoute.id,EvacuationRoute.name,EvacuationRoute.description).filter(
            EvacuationRoute.id==id
        )
        return [ar._asdict() for ar in a] if  a  else abort(404)

    @classmethod
    def delete_evacuationroute(cls,id):
        evacuationroute = cls.get_evacuationroute(id)
        evacuationroute.active = 0
        db.session.commit()
        return {'message': 'El recorrido de evacuacion fue eliminado con exito!', 'category': 'success'}

    @classmethod
    def update_evacuationroute(cls, parameters, arreglo_coordenadas):
        return cls.modify_evacuationroute(parameters,arreglo_coordenadas)

    @classmethod
    def modify_evacuationroute(cls, parameters, arreglo_coordenadas):
        evacuationroute = cls.get_evacuationroute(parameters["evacuation_route_id"])
        result_of_validations = validate_evacuation_route_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        result_of_coordinates_validations = validate_coordinates(arreglo_coordenadas)
        if (not result_of_coordinates_validations['valid']):
            return result_of_coordinates_validations
        evacuationroute.name = parameters['name']
        evacuationroute.description = parameters['description']
        evacuationroute.state_id = parameters['status']
        EvacuationRouteCoordinate.coordinates_deletes(parameters["evacuation_route_id"])
        for i in range(0,len(arreglo_coordenadas),1):
                    latitudAux = arreglo_coordenadas[i].split(',')[0]
                    longitudAux = arreglo_coordenadas[i].split(',')[1]
                    evacuation_route_coordinate = EvacuationRouteCoordinate(latitude=latitudAux,longitude=longitudAux,evacuation_route_id=evacuationroute.id)
                    db.session.add(evacuation_route_coordinate)
        db.session.commit()
        return {'message': 'El recorrido de evacuacion fue modificado con exito!', 'category': 'success'}
    
    @classmethod
    def get_all_evacuation_coordinates(cls,id):
        a = db.session.query(EvacuationRouteCoordinate.latitude,EvacuationRouteCoordinate.longitude).filter(
            EvacuationRouteCoordinate.evacuation_route_id==id
        )

        return [ar._asdict() for ar in a]
    
    @classmethod
    def json_evacuationroutes(cls):
        a = db.session.query(EvacuationRoute.id,EvacuationRoute.name,EvacuationRoute.description).filter(
            EvacuationRoute.active==1
        )
        return [ar._asdict() for ar in a] if  a  else abort(404)
    
    @classmethod
    def json_evacuationroute_coordinates(cls,id):
        a = db.session.query(EvacuationRouteCoordinate.latitude.label("lat"),EvacuationRouteCoordinate.longitude.label("long")).filter(
            EvacuationRouteCoordinate.evacuation_route_id==id
        )

        return [ar._asdict() for ar in a]

    
