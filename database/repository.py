from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .models import db_service, Post, Category
from datetime import datetime
from werkzeug.security import safe_join
import re
import uuid

class PostRepository:
    @staticmethod
    def sanitize_input(input_str):
        """Elimina caracteres potencialmente peligrosos"""
        if not input_str:
            return input_str
        return re.sub(r'[^\w\s\-.,áéíóúÁÉÍÓÚñÑ]', '', str(input_str))

    @staticmethod
    def create_post(title, description, category_id=None, map_url=None, images=None):
        session = db_service.get_session()
        try:
            if not title or not description:
                raise ValueError("Title and description are required")
                
            title = PostRepository.sanitize_input(title)
            description = PostRepository.sanitize_input(description)
            
            if category_id is not None:
                try:
                    category_id = int(category_id)
                except ValueError:
                    raise ValueError("Invalid category ID")
                    
            if map_url and not map_url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format")

            post = Post(
                title=title,
                description=description,
                category_id=category_id,
                map_url=map_url,
                images=images or []
            )
            session.add(post)
            session.commit()
            return post.to_dict()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_posts():
        session = db_service.get_session()
        try:
            posts = session.execute(
                text("""
                SELECT p.*, c.name as category_name 
                FROM posts p
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.created_at DESC
                """)
            ).mappings().all()
            return [dict(post) for post in posts]
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_post_by_id(post_id):
        session = db_service.get_session()
        try:
            post = session.execute(
                text("""
                SELECT p.*, c.name as category_name 
                FROM posts p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = :post_id
                """),
                {'post_id': post_id}
            ).mappings().first()
            return dict(post) if post else None
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()
