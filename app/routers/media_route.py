from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from app.models import MediaItemModel, Genre, Tags, UserItemModel, MediaItemLikeModel
from fastapi import Depends
from app import get_db_session
from sqlalchemy import and_, asc, desc, select, or_
from sqlalchemy.orm import Session, joinedload
from app.schemas.MediaBrowseSchema import MediaBrowseSchemaArguments
from app.utils.exceptions import BadRequest
from pydantic import BaseModel





class UserResponse(BaseModel):
    id: int 
    romaji_title: str 
    medium_image: str
    isAdult: bool
    score: float








router = APIRouter(tags=["Discover and Browse Content in Media"])

@router.post("/api/search", status_code=201, response_model=List[UserResponse])
async def search_media(data_request: MediaBrowseSchemaArguments, db: Session = Depends(get_db_session)):
    query = db.query(MediaItemModel)

    if data_request.keyword:
        query = query.where(or_(
            MediaItemModel.romaji_title.ilike(f"%{data_request.keyword}%"),
            MediaItemModel.english_title.ilike(f"%{data_request.keyword}%"),
            MediaItemModel.synonyms_titles.ilike(f"%{data_request.keyword}%"),
            MediaItemModel.native_title.ilike(f"%{data_request.keyword}%")
        ))

    filters = [
        (data_request.countryOfOrigin, MediaItemModel.countryOfOrigin),
        (data_request.novel_status, MediaItemModel.novel_status),
        (data_request.translate_status, MediaItemModel.translate_status),
        (data_request.source, MediaItemModel.source),
        (data_request.format, MediaItemModel.format),
        (data_request.isAdult, MediaItemModel.isAdult),
        (data_request.has_anime, MediaItemModel.has_anime),
        (data_request.has_manga, MediaItemModel.has_manga),
        (data_request.isLicensed, MediaItemModel.has_license),
        (data_request.startYear, MediaItemModel.startYear),
    ]
    for filter_value, filter_column in filters:
        if filter_value is not None:
            query = query.where(filter_column == filter_value)

    if data_request.genres is not None:
            genre_conditions = [ MediaItemModel.genres.any(Genre.name == genre) for genre in data_request.genres]
            query = query.filter(and_(*genre_conditions))
    if data_request.excludedGenres is not None:
        excluded_genre_conditions = [~MediaItemModel.genres.any(Genre.name == genre) for genre in data_request.excludedGenres]
        query = query.filter(and_(*excluded_genre_conditions))

        # Apply tag filters
    if data_request.tags:
        tag_conditions = [ MediaItemModel.tags.any(Tags.name == tag) for tag in data_request.tags]
        query = query.filter(and_(*tag_conditions))

    if data_request.excludedTags:
        excludedTags_conditions = [~MediaItemModel.tags.any(Tags.name == tag) for tag in data_request.excludedTags]
        query = query.filter(and_(*excludedTags_conditions))

    if data_request.score_greater_than is not None and data_request.score_lesser_than is not None:
        query = query.where(MediaItemModel.score.between(data_request.score_greater_than, data_request.score_lesser_than))
    elif data_request.score_greater_than is not None:
        query = query.where(MediaItemModel.score >= data_request.score_greater_than)
    elif data_request.score_lesser_than is not None:
        query = query.where(MediaItemModel.score <= data_request.score_lesser_than)

    if data_request.yearGreater is not None and data_request.yearLesser is not None:
        query = query.where(MediaItemModel.startYear.between(data_request.yearGreater, data_request.yearLesser))
    elif data_request.yearGreater is not None:
        query = query.where(MediaItemModel.startYear >= data_request.yearGreater)
    elif data_request.yearLesser is not None:
        query = query.where(MediaItemModel.startYear <= data_request.yearLesser)

    if data_request.sort:
        sort_mapping = {
            "popularity": desc(MediaItemModel.popularity),
            "trending": desc(MediaItemModel.trending),
            "favourites": desc(MediaItemModel.favourites),
            "title": asc(MediaItemModel.romaji_title),
            "score":desc(MediaItemModel.score),
            "release-date": desc(MediaItemModel.start_at),
            "recently-added": desc(MediaItemModel.added_at),
            "recently-updated": desc(MediaItemModel.updated_at),
            
        }
        if data_request.sort in sort_mapping:
            query = query.order_by(sort_mapping[data_request.sort])

    offset = (data_request.page - 1) * data_request.per_page
    query = query.limit(data_request.per_page).offset(offset)

    query = query.with_entities(
        MediaItemModel.id, 
        MediaItemModel.romaji_title, 
        MediaItemModel.medium_image, 
        MediaItemModel.isAdult,
        MediaItemModel.score
        ).all()
    
    if len(query) == 0:
        raise BadRequest
    return query



@router.get("/api/novel/{content_id}", status_code=201)
async def get_media(content_id: int, db: Session = Depends(get_db_session)):
    query = db.query(MediaItemModel)
    query = query.where(MediaItemModel.id == content_id)
    query = query.first()
    if not query:
        raise BadRequest
    return query


@router.get("/api/user/{user_id}/liked", response_model=list[UserResponse])
def get_liked_media(user_id: int, db: Session = Depends(get_db_session)):

    user = db.query(UserItemModel).filter(UserItemModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(MediaItemModel).join(MediaItemLikeModel).filter(
        MediaItemLikeModel.user_id == user.id,
        MediaItemLikeModel.liked == True
    ).options(joinedload(MediaItemModel.likes))
    
    data = query.with_entities(
        MediaItemModel.id, 
        MediaItemModel.romaji_title, 
        MediaItemModel.medium_image, 
        MediaItemModel.isAdult,
        MediaItemModel.score
        ).all()

    if len(data) == 0:
        raise HTTPException(status_code=404, detail="media not found")

    return data