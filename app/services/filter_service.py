from app.models.user import User
from sqlalchemy.sql import func


class FilterService:

    @classmethod
    # maybe, we can use this: type(a_collection[0] , to represent the model, that we want to filter
    def execute_specific_filter(cls, a_collection, a_filter):
        both = len(a_filter.keys())
        value = list(a_filter.values())[0]
        searched = '%' + func.lower(value) + '%'
        if (both == 2):
            status = list(a_filter.values())[1]
            return a_collection.filter(((User.active) == (status)) & ((func.lower(User.email).like(searched)) | func.lower(User.first_name).like(searched) | func.lower(User.last_name).like(searched) | func.lower(User.username).like(searched)))
        elif (list(a_filter.keys())[0] == 'search'):
            return a_collection.filter(func.lower(User.email).like(searched) | func.lower(User.first_name).like(searched) | func.lower(User.last_name).like(searched) | func.lower(User.username).like(searched))
        else:
            status = list(a_filter.values())[0]
            return a_collection.filter((User.active) == bool(status))

    @classmethod
    def apply_filter(cls, a_collection, a_filter):
        if a_filter is None:
            resul = a_collection
        else:
            resul = cls.execute_specific_filter(a_collection, a_filter)
        return resul
