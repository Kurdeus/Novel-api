from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Enum, DateTime, String, Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.constants import GenderChoices
from app.utils.fields import Password
from app import Base


association_table_followers = Table(
    "association_table_followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user_table.id")),
    Column("followed_id", Integer, ForeignKey("user_table.id")),

)




class UserItemModel(Base):
    __tablename__ = 'user_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    password: Mapped[str] = mapped_column(Password, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=True)
    gender: Mapped[str] = mapped_column(Enum(GenderChoices), default=GenderChoices.DEFAULT, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, index=True, nullable=True)
    image: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[str] = mapped_column(DateTime, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    expiration_date: Mapped[str] = mapped_column(DateTime, nullable=True, default=None)
    last_phone_token: Mapped[str] = mapped_column(String, nullable=True, default=None)
    last_login_at: Mapped[str] = mapped_column(DateTime, nullable=True, default=None)
    last_login_ip: Mapped[str] = mapped_column(String, nullable=True, default=None)
    email_confirmation_token: Mapped[str] = mapped_column(String, nullable=True, default=None)
    login_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    logedin_device: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=True, default=None)
    invited_by: Mapped[int] = mapped_column(Integer, ForeignKey('user_table.id'), nullable=True, default=None)
    social_links: Mapped[str] = mapped_column(String, nullable=True, default=None)
    invite_reward_points: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    
    licenses = relationship('UserLicense', back_populates='user')
    media_liked = relationship("MediaItemModel", back_populates="user")
    comment_liked = relationship("CommentItemLikeModel", back_populates="user")
    media_review = relationship("MediaItemReviewModel", back_populates="user")
    media_comment = relationship("MediaItemCommentModel", back_populates="user")
    user_ticket = relationship('UserTicketModel', back_populates='user')

    followed_users: Mapped[List["UserItemModel"]] = relationship(
        secondary=association_table_followers,
        primaryjoin=id == association_table_followers.c.follower_id,
        secondaryjoin=id == association_table_followers.c.followed_id,
        back_populates="followers",
        lazy="joined"
    )
    followers: Mapped[List["UserItemModel"]] = relationship(
        secondary=association_table_followers,
        primaryjoin=id == association_table_followers.c.followed_id,
        secondaryjoin=id == association_table_followers.c.follower_id,
        back_populates="followed_users",
        lazy="joined"
    )



class UserLicense(Base):
    __tablename__ = 'user_license_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)
    purchase_token = Column(String, nullable=True, default=None)
    purchase_date = Column(DateTime, nullable=True, default=None)
    expiration_date = Column(DateTime, nullable=True, default=None)

    user = relationship('UserItemModel', back_populates='licenses')



class UserTicketModel(Base):
    __tablename__ = "user_ticket_table"

    id = Column(Integer, primary_key=True, index=True) 
    ticket_title = Column(String, nullable=True, default=None)
    ticket_massage = Column(String, nullable=True, default=None)
    admin_answer = Column(String, nullable=True, default=None)
    closed = Column(Boolean, nullable=True, default=False)
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)

    user = relationship("UserItemModel", back_populates="user_ticket")
   
