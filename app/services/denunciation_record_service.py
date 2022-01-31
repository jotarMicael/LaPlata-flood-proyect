from flask import session
from sqlalchemy.orm import query
from app.db import db
from app.models.category import Category
from app.models.denunciation import Denunciation
from app.models.denunciation_record import DenunciationRecord
from app.models.denunciation_state import DenunciationState
from app.models.user import User
from app.services.denunciation_service import DenunciationService

class DenunciationRecordService:

    @classmethod
    def get_user_name(cls,id):
        query = User.query.get(id)
        name = query.first_name + ' ' + query.last_name
        return name

    @classmethod
    def get_state_name(cls,id):
        query = DenunciationState.query.get(id)
        name = query.name_ds
        return name

    @classmethod
    def get_records_by_id(cls, id):
        query = db.session.query(
            DenunciationRecord.id,
            DenunciationRecord.detail,
            DenunciationRecord.user_assign,
            DenunciationRecord.actual_state,
            DenunciationRecord.created_at_r,
            DenunciationRecord.denunciation_id,
            Denunciation.denunciation_state_id,
            DenunciationState.name_ds
        ).select_from(DenunciationRecord)
        join_query = query.join(Denunciation).join(DenunciationState)
        return join_query.filter(DenunciationRecord.denunciation_id==id).order_by(DenunciationRecord.created_at_r)

    @classmethod
    def add_denunciation_record(cls, parameters, id):
        detail = parameters['title']
        user_assign = parameters['user_id']
        actual_state = parameters['denunciation_state_id']
        user_name = cls.get_user_name(user_assign)
        state_name = cls.get_state_name(actual_state)
        denunciation_record = DenunciationRecord(detail=detail, user_assign=user_name, denunciation_id=id, actual_state=state_name)
        denunciation = DenunciationService.get_denunciation(id)
        denunciation.denunciation_state_id = actual_state
        try:
            db.session.add(denunciation_record)
            db.session.commit()
            return {'message': 'El seguimiento fue cargado con exito!', 'category': 'success', 'valid': True}
        except:
            return { 'message': 'El seguimiento no pudo ser cargado', 'category': 'error', 'valid': False }

    @classmethod
    def delete_denunciation_record(cls, id):
        toDelete = DenunciationRecord.query.get(id)
        try:
            db.session.delete(toDelete)
            db.session.commit()
            return {'message': 'El seguimiento fue borrado con exito!', 'category': 'success', 'valid': True}
        except:
            return { 'message': 'El seguimiento no pudo ser borrado', 'category': 'error', 'valid': False }


    @classmethod
    def get_denunciation_and_record(cls, id):
        query = db.session.query(Denunciation.id,Denunciation.title,Denunciation.first_name_d,
        Denunciation.last_name_d, Denunciation.email_d, Denunciation.phone_d, Denunciation.latitude,
        Denunciation.longitude, Denunciation.category_id, Denunciation.denunciation_state_id,
        Denunciation.user_id,Category.name_cat,DenunciationState.name_ds, User.first_name,
        User.last_name).select_from(Denunciation)
        join_query= query.join(DenunciationState).join(User).join(Category)
        return join_query.filter(Denunciation.active==1, Denunciation.id==id)