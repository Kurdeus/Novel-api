from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Float, Table, Boolean, JSON
from sqlalchemy.orm import relationship
from app import Base


association_table_genre = Table(
    'association_table_media_genre',
    Base.metadata,
    Column('media_id', Integer, ForeignKey('media_table.id')),
    Column('genre_id', Integer, ForeignKey('media_genre_table.id'))
)

association_table_characters = Table(
    'association_table_media_characters',
    Base.metadata,
    Column('media_id', Integer, ForeignKey('media_table.id')),
    Column('character_id', Integer, ForeignKey('media_character_table.id'))  # Corrected column name to 'character_id'
)

association_table_staff = Table(
    'association_table_media_staff',
    Base.metadata,
    Column('media_id', Integer, ForeignKey('media_table.id')),
    Column('staff_id', Integer, ForeignKey('media_staff_table.id'))
)

association_table_tags = Table(
    'association_table_media_tags',
    Base.metadata,
    Column('media_id', Integer, ForeignKey('media_table.id')),
    Column('tag_id', Integer, ForeignKey('media_tag_table.id'))
)


class MediaItemModel(Base):
    __tablename__ = 'media_table'
    id = Column(Integer, primary_key=True)
    anilist_popularity = Column(Integer, nullable=True, default=None)
    anilist_trending = Column(Integer, nullable=True, default=None)
    anilist_favourites = Column(Integer, nullable=True, default=None)
    romaji_title = Column(String, nullable=True, default=None)
    english_title = Column(String, nullable=True, default=None)
    native_title = Column(String, nullable=True, default=None)
    synonyms_titles = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)
    fa_description = Column(String, nullable=True, default=None)
    volumes = Column(Integer, nullable=True, default=None)
    language = Column(String, nullable=True, default=None)
    countryOfOrigin = Column(String, nullable=True, default=None)
    format = Column(String, nullable=True, default=None)
    source = Column(String, nullable=True, default=None)
    anilist_id = Column(Integer, nullable=True, default=None)
    mal_id = Column(Integer, nullable=True, default=None)
    extra_large_image = Column(String, nullable=True, default=None)
    large_image = Column(String, nullable=True, default=None)
    medium_image = Column(String, nullable=True, default=None)
    bannerImage = Column(String, nullable=True, default=None)
    score = Column(Float, nullable=True, default=None)
    translate_status = Column(String, nullable=True, default=None)
    novel_status = Column(String, nullable=True, default=None)
    isAdult = Column(Boolean, nullable=True, default=False)
    startYear = Column(Integer, nullable=True, default=None)
    start_at = Column(DateTime, nullable=True, default=None)
    added_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    startDate = Column(JSON, nullable=True, default=None)
    endDate = Column(JSON, nullable=True, default=None)
    has_manga = Column(Boolean, nullable=True, default=None)
    has_anime = Column(Boolean, nullable=True, default=None)
    has_license = Column(Boolean, nullable=True, default=None)
    likes_count = Column(Integer, nullable=True, default=0)

    genres = relationship('Genre', secondary=association_table_genre, back_populates='media', lazy="selectin")
    characters = relationship('Characters', secondary=association_table_characters, back_populates='media', lazy="selectin")
    staff = relationship('Staff', secondary=association_table_staff, back_populates='media', lazy="selectin")
    tags = relationship('Tags', secondary=association_table_tags, back_populates='media', lazy="selectin")
    epub_volumes = relationship('EPUB_Volumes', back_populates='media', lazy="selectin")
    pdf_volumes = relationship('PDF_Volumes', back_populates='media', lazy="selectin")
    cover_volumes = relationship('Cover_Volumes', back_populates='media', lazy="selectin")
    audio_volumes = relationship('Audio_Volumes', back_populates='media', lazy="selectin")
    likes = relationship("MediaItemLikeModel", back_populates='media')
    reviews = relationship("MediaItemReviewModel", back_populates='media')
    comments = relationship("MediaItemCommentModel", back_populates='media')


class MediaItemLikeModel(Base):
    __tablename__ = "media_likes_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    media_id = Column(Integer, ForeignKey("media_table.id"))
    liked = Column(Boolean, default=False)

    user = relationship("UserItemModel", back_populates="media_liked")
    media = relationship("MediaItemModel", back_populates="likes")


class MediaItemReviewModel(Base):
    __tablename__ = "media_reviews_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    media_id = Column(Integer, ForeignKey("media_table.id"))
    review = Column(String, nullable=True, default=None)

    user = relationship("UserItemModel", back_populates="media_review")
    media = relationship("MediaItemModel", back_populates="reviews")


class MediaItemCommentModel(Base):
    __tablename__ = "media_comments_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    media_id = Column(Integer, ForeignKey("media_table.id"))
    comment = Column(String, nullable=True, default=None)
    reply_to_comment = Column(Integer, nullable=True, default=None)
    likes_count = Column(Integer, nullable=True, default=0)

    user = relationship("UserItemModel", back_populates="media_comment")
    media = relationship("MediaItemModel", back_populates="comments")
    likes = relationship("CommentItemLikeModel", back_populates='comment')


class CommentItemLikeModel(Base):
    __tablename__ = "comment_likes_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    comment_id = Column(Integer, ForeignKey("media_comments_table.id"))
    liked = Column(Boolean, default=False)

    user = relationship("UserItemModel", back_populates="comment_liked")
    comment = relationship("MediaItemCommentModel", back_populates="likes")


class Cover_Volumes(Base):
    __tablename__ = 'media_cover_volumes_table'
    id = Column(Integer, primary_key=True)
    volume_title = Column(String, nullable=True, default=None)
    volume_number = Column(Float, nullable=True, default=None)
    path = Column(String, nullable=True, default=None)
    media_id = Column(Integer, ForeignKey('media_table.id'))

    media = relationship("MediaItemModel", back_populates="cover_volumes")


class EPUB_Volumes(Base):
    __tablename__ = 'media_epub_volumes_table'
    id = Column(Integer, primary_key=True)
    volume_title = Column(String, nullable=True, default=None)
    volume_number = Column(Float, nullable=True, default=None)
    path = Column(String, nullable=True, default=None)
    media_id = Column(Integer, ForeignKey('media_table.id'))

    media = relationship("MediaItemModel", back_populates="epub_volumes")


class PDF_Volumes(Base):
    __tablename__ = 'media_pdf_volumes_table'
    id = Column(Integer, primary_key=True)
    volume_title = Column(String, nullable=True, default=None)
    volume_number = Column(Float, nullable=True, default=None)
    path = Column(String, nullable=True, default=None)
    media_id = Column(Integer, ForeignKey('media_table.id'))

    media = relationship("MediaItemModel", back_populates="pdf_volumes")


class Audio_Volumes(Base):
    __tablename__ = 'media_audio_volumes_table'
    id = Column(Integer, primary_key=True)
    volume_title = Column(String, nullable=True, default=None)
    volume_number = Column(Float, nullable=True, default=None)
    path = Column(String, nullable=True, default=None)
    media_id = Column(Integer, ForeignKey('media_table.id'))

    media = relationship("MediaItemModel", back_populates="audio_volumes")


class Genre(Base):
    __tablename__ = 'media_genre_table'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, default=None)

    media = relationship('MediaItemModel', secondary=association_table_genre, back_populates='genres')


class Tags(Base):
    __tablename__ = 'media_tag_table'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer, nullable=True, default=None)
    name = Column(String, nullable=True, default=None)
    isGeneralSpoiler = Column(Boolean, nullable=True, default=False)
    isMediaSpoiler = Column(Boolean, nullable=True, default=False)
    isAdult = Column(Boolean, nullable=True, default=False)

    media = relationship('MediaItemModel', secondary=association_table_tags, back_populates='tags')


class Staff(Base):
    __tablename__ = 'media_staff_table'
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, nullable=True, default=None)
    age = Column(String, nullable=True, default=None)
    first = Column(String, nullable=True, default=None)
    middle = Column(String, nullable=True, default=None)
    last = Column(String, nullable=True, default=None)
    full = Column(String, nullable=True, default=None)
    userPreferred = Column(String, nullable=True, default=None)
    role = Column(String, nullable=True, default=None)
    large_image = Column(String, nullable=True, default=None)
    medium_image = Column(String, nullable=True, default=None)
    gender = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)

    media = relationship('MediaItemModel', secondary=association_table_staff, back_populates='staff')


class Characters(Base):
    __tablename__ = 'media_character_table'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=True, default=None)
    role = Column(String, nullable=True, default=None)
    first = Column(String, nullable=True, default=None)
    middle = Column(String, nullable=True, default=None)
    last = Column(String, nullable=True, default=None)
    full = Column(String, nullable=True, default=None)
    userPreferred = Column(String, nullable=True, default=None)
    large_image = Column(String, nullable=True, default=None)
    medium_image = Column(String, nullable=True, default=None)
    age = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)
    gender = Column(String, nullable=True, default=None)

    media = relationship('MediaItemModel', secondary=association_table_characters, back_populates='characters')
