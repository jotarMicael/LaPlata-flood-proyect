from flask import session, jsonify
from app.models.colour_map import ColourMap
from app.models.flood_zone import FloodZone
from app.models.flood_zone_coordinate import FloodZoneCoordinate
from app.db import db

from flask import abort
from sqlalchemy.sql import func
from sqlalchemy import asc, desc
import csv

class FloodZoneService:

    @classmethod
    def get_all_flood_zones(cls):
        if bool(session["criteria"] == "ASC"):
            return FloodZone.query.filter_by(active=1).order_by(asc(FloodZone.name))
        else:
            return FloodZone.query.filter_by(active=1).order_by(desc(FloodZone.name))

    @classmethod
    def json_flood_zones(cls,id):
        a = db.session.query(FloodZone.id,FloodZone.name.label("nombre"),FloodZone.colour_map_id.label("colour_map_id")).filter(FloodZone.id==id)
        return [ar._asdict() for ar in a]
    
    @classmethod
    def json_flood_zones_all(cls):
        a = db.session.query(FloodZone.id,FloodZone.name.label("nombre"),FloodZone.colour_map_id.label("colour_map_id"))
        return [ar._asdict() for ar in a] if  a  else abort(404)
    

    @classmethod
    def get_all_flood_zone_coordinates(cls,id):
        a = db.session.query(FloodZoneCoordinate.latitude,FloodZoneCoordinate.longitude).filter(
            FloodZoneCoordinate.flood_zone_id==id
        )

        return [ar._asdict() for ar in a]

    @classmethod
    def get_all_flood_zone_coordinates_2(cls,id):
        a = db.session.query(FloodZoneCoordinate.latitude.label("lat"),FloodZoneCoordinate.longitude.label("long")).filter(
            FloodZoneCoordinate.flood_zone_id==id
        )

        return [ar._asdict() for ar in a]
    
    
    @classmethod
    def get_filtered_flood_zones(cls, a_collection, a_filter):
        if a_filter is None:
            return a_collection
        else:
            both = len(a_filter.keys())
            value = list(a_filter.values())[0]
            searched = '%' + func.lower(value) + '%'
            if (both == 2):
                status = list(a_filter.values())[1]
                return a_collection.filter(((FloodZone.state_id) == (status)) & ((func.lower(FloodZone.name).like(searched))  ))
            elif (list(a_filter.keys())[0] == 'search'):
                return a_collection.filter(func.lower(FloodZone.name).like(searched)   )
            else:
                status = list(a_filter.values())[0]
                return a_collection.filter((FloodZone.state_id) == status)
    @classmethod
    def get_floodzone(cls, id):
        floodzone = FloodZone.query.get(id)
        return  floodzone if  floodzone else abort(404)
    

    @classmethod
    def add_flood_zones(cls, file):
        
        if not file:
            return None
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            try:
                for row in reader:                
                    array = row['area'].split(']')
                    floodzone = FloodZone(name=row['name'] ,active=1, state_id=1,colour_map_id = 1)
                    db.session.add(floodzone) 
                    db.session.flush()
                    cant = 0   
                    for arr in array:
                        arr2 = (arr.strip(',[')).split(sep=',')                            
                        if  arr2[0]:
                            cant = cant + 1
                            floodzone_coordinate = FloodZoneCoordinate(latitude=arr2[0], longitude=arr2[1], active=1,flood_zone_id = floodzone.id )
                            db.session.add(floodzone_coordinate) 
                    floodzonedb = FloodZoneService.get_floodzone(floodzone.id)
                    floodzonedb.points_count = cant
                    db.session.flush()
                db.session.commit()                
                return {'message': 'Agregados con exito!', 'category': 'success'}
            except:
                return { 'message': 'Archivo con formato inválido', 'category': 'error', 'valid': False }   
                     
    @classmethod
    def update_floodzone(cls, parameters):
        return cls.modify_floodzone(parameters)

    @classmethod
    def modify_floodzone(cls, parameters):
        
        floodzone = cls.get_floodzone(parameters["floodzone_id"])
           
        floodzone.colour_map_id= parameters['colour']   
        floodzone.state_id = parameters['status']
        
        db.session.commit()
        return {'message': 'La zona de inundacion con exito!', 'category': 'success'}
                
    @classmethod
    def delete_floodzone(cls, id):
        floodzone = cls.get_floodzone(id)
        FloodZoneCoordinate.coordinates_deletes(id)
        floodzone.active = 0
        db.session.commit()
        return {'message': 'La Zona de inundación fue eliminada con exito!', 'category': 'success'}
