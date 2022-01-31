from sqlalchemy.sql.functions import user
from werkzeug.exceptions import abort
from app.helpers.validation_helper import validate_denunciation_parameters
from app.models.denunciation import Denunciation
from app.models.category import Category
from app.models.user import User
from app.models.denunciation_state import DenunciationState
from flask import session
from app.db import db
from sqlalchemy import asc, desc
from sqlalchemy.sql import func


class DenunciationService:

    @classmethod
    def get_all_states(cls):
        if bool(session["criteria"] == "ASC"):
            return DenunciationState.query.filter_by(active=1).order_by(asc(DenunciationState.name))
        else:
            return DenunciationState.query.filter_by(active=1).order_by(desc(DenunciationState.name))

    @classmethod
    def get_all(cls):
        if bool(session["criteria"] == "ASC"):
            query = db.session.query(Denunciation.id,Denunciation.title,Denunciation.first_name_d,
                Denunciation.last_name_d, Denunciation.email_d, Denunciation.phone_d, Denunciation.latitude,
                Denunciation.longitude, Denunciation.category_id, Denunciation.denunciation_state_id, Denunciation.attempts,
                Denunciation.user_id,DenunciationState.name_ds, DenunciationState.color_class).select_from(Denunciation)
            join_query = query.join(DenunciationState)
            return join_query.filter(Denunciation.active==1).order_by(asc(Denunciation.title))
            
        else:
            query = db.session.query(Denunciation.id,Denunciation.title,Denunciation.first_name_d,
                Denunciation.last_name_d, Denunciation.email_d, Denunciation.phone_d, Denunciation.latitude,
                Denunciation.longitude, Denunciation.category_id, Denunciation.denunciation_state_id, Denunciation.attempts,
                Denunciation.user_id,DenunciationState.name_ds, DenunciationState.color_class).select_from(Denunciation)
            join_query = query.join(DenunciationState)
            return join_query.filter(Denunciation.active==1).order_by(desc(Denunciation.title))

    @classmethod
    # maybe, we can use this: type(a_collection[0] , to represent the model, that we want to filter
    def execute_specific_filter(cls, a_collection, a_filter):
        both = len(a_filter.keys())
        value = list(a_filter.values())[0]
        searched = '%' + func.lower(value) + '%'
        if (both == 2):
            status = list(a_filter.values())[1]
            return a_collection.filter(((Denunciation.denunciation_state_id) == (status)) & (func.lower(Denunciation.title).like(searched)))
        elif (list(a_filter.keys())[0] == 'search'):
            return a_collection.filter(func.lower(Denunciation.title).like(searched))
        else:
            status = list(a_filter.values())[0]
            return a_collection.filter((Denunciation.denunciation_state_id) == status)


    @classmethod
    def get_filtered_denunciations(cls, a_collection, a_filter):
        if a_filter is None:
            resul = a_collection
        else:
            resul = cls.execute_specific_filter(a_collection, a_filter)
        return resul

    @classmethod
    def get_filtered_denunciations_by_date(cls, a_collection, a_filter):
        return a_collection.filter(Denunciation.created_at.between(a_filter['from_date'], a_filter['to_date']))
    
    @classmethod
    def denunciation_exist(cls, parameters):
        return True if len(list(Denunciation.query.filter(Denunciation.title == parameters['title'], Denunciation.category_id == parameters['category_id']))) != 0 else False
    
    @classmethod
    def add_denunciation(cls, parameters):
        result_of_validations = validate_denunciation_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        if cls.denunciation_exist(parameters):
            result_of_validations['message'] = 'No es posible cargar esta denuncia'
            result_of_validations['category'] = 'error'
            result_of_validations['valid'] = False
            return result_of_validations
        else:
            title = parameters['title']
            category_id = parameters['category_id']
            denunciation_state_id = parameters['denunciation_state_id']
            first_name = parameters['first_name_d']
            last_name = parameters['last_name_d']
            phone = parameters['phone_d']
            email = parameters['email_d']
            user_id = parameters['user_id']
            latitude = parameters['latitude']
            longitude = parameters['longitude']
            description = parameters['description']
                  
            denunciation = Denunciation(title=title, category_id=category_id, denunciation_state_id=denunciation_state_id, first_name_d=first_name, last_name_d=last_name, phone_d=phone, email_d=email, user_id=user_id, latitude=latitude, longitude=longitude, description=description)
            try:
                db.session.add(denunciation)
                db.session.commit()
                
                return {'message': 'La denuncia fue cargada con exito!', 'category': 'success', 'valid': True}
            except:
                return { 'message': 'La denuncia no pudo ser cargada', 'category': 'error', 'valid': False }
    
    
    def get_categories():
        return Category.query.filter(Category.active==1).all()
    
   
    def get_users():
        return User.query.filter(User.active==1).all()


    def get_states():
        return DenunciationState.query.filter(DenunciationState.active==1).all()

    @classmethod
    def get_denunciation(cls, id):
        denunciation = Denunciation.query.get(id)
        return denunciation if denunciation else abort(404)
    
    @classmethod
    def update_denunciation(cls, parameters):
        return cls.modify_denunciation(parameters)

    @classmethod
    def modify_denunciation(cls, parameters):
        print('-------------parametros-----------------')
        print(parameters['denunciation_id'])
        denunciation = cls.get_denunciation(parameters['denunciation_id'])
        result_of_validations = validate_denunciation_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        
        denunciation.title = parameters['title']
        if (parameters['category_id']):
            denunciation.category_id = parameters['category_id']
        if (parameters['denunciation_state_id']):
            denunciation.denunciation_state_id = parameters['denunciation_state_id']
        denunciation.first_name_d = parameters['first_name']
        denunciation.last_name_d = parameters['last_name']
        denunciation.phone_d = parameters['phone']
        denunciation.email_d = parameters['email']
        if (parameters['user_id']):
            denunciation.user_id = parameters['user_id']
        if (parameters['latitude']):
            denunciation.latitude = parameters['latitude']
        if (parameters['longitude']):
            denunciation.longitude = parameters['longitude']
        denunciation.description = parameters['description']
                  
        db.session.commit()
        return {'message': 'La denuncia fue modificada con exito!', 'category': 'success'}
    
    @classmethod
    def get_all_denunciations(self, id):
        query = db.session.query(Denunciation.id,Denunciation.title,Denunciation.first_name_d,
        Denunciation.last_name_d, Denunciation.email_d, Denunciation.phone_d, Denunciation.latitude,
        Denunciation.longitude, Denunciation.category_id, Denunciation.denunciation_state_id,
        Denunciation.user_id,Category.name_cat,DenunciationState.name_ds, User.first_name, User.last_name).select_from(Denunciation)
        join_query= query.join(DenunciationState).join(User).join(Category)
        return join_query.filter(Denunciation.active==1).all()

    @classmethod
    def get_all_states(cls):
        if bool(session["criteria"] == "ASC"):
            return DenunciationState.query.filter_by(active=1).order_by(asc(DenunciationState.name_ds))
        else:
            return DenunciationState.query.filter_by(active=1).order_by(desc(DenunciationState.name_ds))

  
    @classmethod
    def delete_denunciation(cls, id):
        denunciation = cls.get_denunciation(id)
        denunciation.active = 0
        db.session.commit()
        return {'message': 'La denuncia fue eliminada con exito!', 'category': 'success'}

    @classmethod
    def get_state_id(cls):
        state = DenunciationState.query.filter_by(name_ds='Cerrada').first()
        return state.id

    @classmethod
    def reg_attempt(cls, id):
        denunciation = cls.get_denunciation(id)
        if (denunciation.attempts < 3):
            denunciation.attempts = denunciation.attempts + 1
            message = {'message': 'Se registro un intento de contacto!', 'category': 'success'}
            if (denunciation.attempts == 3):
                denunciation.denunciation_state_id = cls.get_state_id()
                message ={'message': 'Se registro el tercer intento de contacto! Se procede a cerrar la denuncia', 'category': 'success'}
        elif (denunciation.attempts == 3):
            denunciation.denunciation_state_id = cls.get_state_id()
            message = {'message': 'Se registro un intento de contacto! Se cierra la denuncia, cantidad de intentos: 3', 'category': 'success'}
        db.session.commit()
        return message



    @classmethod
    def add_denunciation_api(cls, parameters):
        result_of_validations = validate_denunciation_parameters(parameters)
        if (not result_of_validations['valid']):
            return result_of_validations
        if cls.denunciation_exist(parameters):
            result_of_validations['message'] = 'No es posible cargar esta denuncia'
            result_of_validations['category'] = 'error'
            result_of_validations['valid'] = False
            return result_of_validations
        else:
            title = parameters['title']
            category_id = parameters['category_id']
            first_name = parameters['first_name_d']
            last_name = parameters['last_name_d']
            phone = parameters['phone_d']
            email = parameters['email_d']
            latitude = parameters['latitude']
            longitude = parameters['longitude']
            description = parameters['description']
                  
            denunciation = Denunciation(title=title, category_id=category_id, first_name_d=first_name, last_name_d=last_name, phone_d=phone, email_d=email, latitude=latitude, longitude=longitude, description=description)
            try:
                db.session.add(denunciation)
                db.session.commit()
                
                return {'message': 'La denuncia fue cargada con exito!', 'category': 'success', 'valid': True}
            except:
                return { 'message': 'La denuncia no pudo ser cargada', 'category': 'error', 'valid': False }
    