from app.models.user import User
from app.db import db

class PaginateService:
    
    def paginate_collection(a_collection, page, page_size):
        return a_collection.paginate(int(page), int(page_size))