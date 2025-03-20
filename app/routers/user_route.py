from typing import Annotated, List, Type
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app import get_db_session
from sqlalchemy import and_, asc, desc, select, or_
from sqlalchemy.orm import Session, joinedload
from app.models import UserItemModel



router = APIRouter(tags=["Discover and Browse Content in Users"])


