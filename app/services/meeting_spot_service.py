from app.helpers.validation_helper import validate_meetingspot_parameters
from flask import session
from app.models.meeting_spot import MeetingSpot
from app.db import db
from flask import abort
from sqlalchemy.sql import func
from sqlalchemy import asc, desc

from app.models.state import Status

class MeetingSpotService:

    @classmethod
    def get_all_meetingspots(cls):
        if bool(session["criteria"] == "ASC"):
            return MeetingSpot.query.filter_by(active=1).order_by(asc(MeetingSpot.name))
        else:
            return MeetingSpot.query.filter_by(active=1).order_by(desc(MeetingSpot.name))


    @classmethod
    def json_meetingspots(cls):
        a = db.session.query(MeetingSpot.id,MeetingSpot.name,MeetingSpot.address,MeetingSpot.latitude,MeetingSpot.longitude,MeetingSpot.email).filter(
            MeetingSpot.active==1
        )
        return [ar._asdict() for ar in a] if  a  else abort(404)
    


    @classmethod
    def get_all_meetingspots_dict(cls):
        meetingspots = MeetingSpot.query.filter_by(active=1).order_by(asc(MeetingSpot.name))
        return [meetingspot._asdict() for meetingspot in meetingspots] if meetingspots else abort;

    @classmethod
    def get_filtered_meeting_spots(cls, a_collection, a_filter):
        if a_filter is None:
            return a_collection
        else:
            both = len(a_filter.keys())
            value = list(a_filter.values())[0]
            searched = '%' + func.lower(value) + '%'
            if (both == 2):
                status = list(a_filter.values())[1]
                return a_collection.filter(((MeetingSpot.state_id) == (status)) & ((func.lower(MeetingSpot.name).like(searched)) | func.lower(MeetingSpot.address).like(searched) | func.lower(MeetingSpot.phone).like(searched) | func.lower(MeetingSpot.email).like(searched)))
            elif (list(a_filter.keys())[0] == 'search'):
                return a_collection.filter(func.lower(MeetingSpot.email).like(searched) | func.lower(MeetingSpot.name).like(searched) | func.lower(MeetingSpot.address).like(searched) | func.lower(MeetingSpot.phone).like(searched))
            else:
                status = list(a_filter.values())[0]
                return a_collection.filter((MeetingSpot.state_id) == status)

    @classmethod
    def get_meetingspot(cls, id):
        meetingspot = MeetingSpot.query.get(id)
        return meetingspot if meetingspot else abort(404)
    
    @classmethod
    def meetingspot_exist(cls, parameters):
        return True if len(list(MeetingSpot.query.filter(MeetingSpot.address == parameters['address'], MeetingSpot.name == parameters['name']))) != 0 else False
    
    @classmethod
    def add_meetingspot(cls, parameters):
        result_of_validations = validate_meetingspot_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        if cls.meetingspot_exist(parameters):
            result_of_validations['message'] = 'No es posible cargar este punto de encuentro'
            result_of_validations['category'] = 'error'
            result_of_validations['valid'] = False
            return result_of_validations
        else:
            name = parameters['name']
            phone = parameters['phone']
            email = parameters['email']
            status = parameters['status']
            latitude = parameters['latitude']
            longitude = parameters['longitude']
            address = parameters['address']
            meetingspot = MeetingSpot(name=name,address=address,  phone=phone, email=email, state_id=status, latitude=latitude, longitude=longitude)
            try:
                db.session.add(meetingspot)
                db.session.commit()
                print('se puede agregar el punto de encuentro ')
                return {'message': 'El punto de encuentro fue cargado con exito!', 'category': 'success', 'valid': True}
            except:
                return { 'message': 'El punto de encuentro no pudo ser cargado', 'category': 'error', 'valid': False }
    
    @classmethod
    def update_meetingspot(cls, parameters):
        return cls.modify_meetingspot(parameters)

    @classmethod
    def modify_meetingspot(cls, parameters):
        print('-------------parametros-----------------')
        print(parameters)
        meetingspot = cls.get_meetingspot(parameters["meetingspot_id"])
        result_of_validations = validate_meetingspot_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        meetingspot.name = parameters['name']
        meetingspot.phone = parameters['phone']
        if (parameters['email']):
            meetingspot.email = parameters['email']
        if (parameters['status']):
            meetingspot.status = parameters['status']
        meetingspot.latitude = parameters['latitude']
        meetingspot.longitude = parameters['longitude']
        meetingspot.address = parameters['address']
        db.session.commit()
        return {'message': 'El punto de encuentro fue modificado con exito!', 'category': 'success'}
    
    @classmethod
    def delete_meetingspot(cls, id):
        meetingspot = cls.get_meetingspot(id)
        meetingspot.active = 0
        db.session.commit()
        return {'message': 'El punto de encuentro fue eliminado con exito!', 'category': 'success'}

    @classmethod
    def get_states(cls):
        return Status.query.all()

    @classmethod
    def get_all(cls,id):
        query = db.session.query(MeetingSpot.id,MeetingSpot.address,
        MeetingSpot.phone, MeetingSpot.email, MeetingSpot.latitude, MeetingSpot.longitude,
        MeetingSpot.state_id, MeetingSpot.active, Status.id,
        Status.name).select_from(MeetingSpot)
        join_query= query.join(Status)
        return join_query.filter(MeetingSpot.active==1, MeetingSpot.id == id)
