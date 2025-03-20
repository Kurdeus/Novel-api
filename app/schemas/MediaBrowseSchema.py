from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from app import current_year


class MediaBrowseSchemaArguments(BaseModel):
    keyword: Optional[str] = Field(default=None, example="Mushoku Tensei")
    tags: Optional[List[str]] = Field(default=None)
    excludedTags: Optional[List[str]] = Field(default=None)
    score_greater_than: Optional[float] = Field(default=None, example=2.5)
    score_lesser_than: Optional[float] = Field(default=None, example=9.5)
    isLicensed: Optional[bool] = Field(default=None, example=True)
    has_manga: Optional[bool] = Field(default=None, example=True)
    has_anime: Optional[bool] = Field(default=None, example=True)
    isAdult: Optional[bool] = Field(default=None, example=True)
    novel_status: Optional[str] = Field(default=None)
    translate_status: Optional[str] = Field(default=None)
    page: Optional[int] = Field(default=1, example=1)
    per_page: Optional[int] = Field(default=25, description="for how meny item in response should be.", example=25)
    countryOfOrigin: Optional[Literal["JP","CN","KR","TW",]] = Field(default=None, example="JP")
    format: Optional[Literal["LIGHT_NOVEL", "WEB_NOVEL", "NOVEL"]] = Field(default=None, example=["TV"])
    source: Optional[Literal["ORIGINAL", "MANGA", "LIGHT_NOVEL", "WEB_NOVEL", "NOVEL", "ANIME", "VISUAL_NOVEL", "VIDEO_GAME", "DOUJINSHI", "COMIC", "LIVE_ACTION", "GAME", "MULTIMEDIA_PROJECT"]] = Field(default=None)
    startYear: Optional[int] = Field(default=None, description="an int year number like: 1969", ge=1969, le=int("{}".format(current_year+1)), example=2017)
    yearLesser: Optional[int] = Field(default=None, description="an int year number like: 1969", ge=196, le=int("{}".format(current_year+1)), example=2017)
    yearGreater: Optional[int] = Field(default=None, description="an int year number like: 1969", ge=1969, le=int("{}9999".format(current_year+1)), example=2017)
    genres: Optional[List[Literal["Action", "Adventure", "Comedy", "Drama", "Ecchi","Fantasy", "Horror", "Mahou Shoujo", "Mecha", "Music","Mystery", "Psychological", "Romance", "Sci-Fi","Slice of Life", "Sports", "Supernatural", "Thriller"]]] = Field(default=None, example=["Action", "Adventure", "Comedy"])
    excludedGenres: Optional[List[Literal["Action", "Adventure", "Comedy", "Drama", "Ecchi","Fantasy", "Horror", "Mahou Shoujo", "Mecha", "Music","Mystery", "Psychological", "Romance", "Sci-Fi","Slice of Life", "Sports", "Supernatural", "Thriller"]]] = Field(default=None, example=["Thriller", "Supernatural"])
    sort: Optional[str] = Field(default=None)



