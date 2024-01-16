from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False )
    post = Column(String, nullable= False)
    content = Column(String, nullable=False)
    is_published =Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    