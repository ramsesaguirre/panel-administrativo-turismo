from sqlalchemy.exc import SQLAlchemyError
from .models import db_service, Post, Category
from datetime import datetime

class CategoryRepository:
    @staticmethod
    def create_category(name):
        session = db_service.get_session()
        try:
            category = Category(name=name)
            session.add(category)
            session.commit()
            return category.to_dict()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_categories():
        session = db_service.get_session()
        try:
            categories = session.query(Category).order_by(Category.name).all()
            return [category.to_dict() for category in categories]
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_category_by_id(category_id):
        session = db_service.get_session()
        try:
            category = session.query(Category).filter_by(id=category_id).first()
            return category.to_dict() if category else None
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def update_category(category_id, name):
        session = db_service.get_session()
        try:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                return None
                
            category.name = name
            session.commit()
            return category.to_dict()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_category(category_id):
        session = db_service.get_session()
        try:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                return False
                
            session.delete(category)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

# ... (PostRepository permanece igual pero actualizado para manejar category_id)
