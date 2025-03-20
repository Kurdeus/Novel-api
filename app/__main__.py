from fastapi import FastAPI
from app import models
from app import Base, engine, session
#from app.routers.media_route import router as media_route
#app = FastAPI()

Base.metadata.create_all(engine)

from datetime import datetime
import requests




def add_anime(anime):
    item = models.MediaItemModel()
    item.anilist_popularity = int(anime["data"]["Media"]["popularity"])
    item.anilist_trending = int(anime["data"]["Media"]["trending"])
    item.anilist_favourites = int(anime["data"]["Media"]["favourites"])
    item.english_title = anime["data"]["Media"]["title"]["english"]
    item.romaji_title = anime["data"]["Media"]["title"]["romaji"]
    item.native_title = anime["data"]["Media"]["title"]["native"]
    item.volumes =  anime["data"]["Media"]["volumes"]
    item.synonyms_titles = "\n".join(anime["data"]["Media"]["synonyms"]) if len(anime["data"]["Media"]["synonyms"]) != 0 else None
    item.description = anime["data"]["Media"]["description"]
    item.language = "ENG"
    item.countryOfOrigin = anime["data"]["Media"]["countryOfOrigin"]
    item.source = anime["data"]["Media"]["source"]
    item.anilist_id = int(anime["data"]["Media"]["id"])
    item.mal_id = int(anime["data"]["Media"]["idMal"] if anime["data"]["Media"]["idMal"] is not None else 0)
    item.extra_large_image = anime["data"]["Media"]["coverImage"]["extraLarge"]
    item.large_image = anime["data"]["Media"]["coverImage"]["large"]
    item.medium_image = anime["data"]["Media"]["coverImage"]["medium"]
    item.bannerImage = anime["data"]["Media"]["bannerImage"]
    item.score = (float(anime["data"]["Media"]["meanScore"]) / 10.0)
    item.novel_status = anime["data"]["Media"]["status"]
    item.isAdult = anime["data"]["Media"]["isAdult"]
    item.startDate = anime["data"]["Media"]["startDate"]
    item.endDate = anime["data"]["Media"]["endDate"]
    item.startYear = anime["data"]["Media"]["startDate"]["year"]
    sy = anime["data"]["Media"]["startDate"]["year"] if anime["data"]["Media"]["startDate"]["year"] != None else 1
    sm = anime["data"]["Media"]["startDate"]["month"] if anime["data"]["Media"]["startDate"]["month"] != None else 1
    sd = anime["data"]["Media"]["startDate"]["day"] if anime["data"]["Media"]["startDate"]["day"] != None else 1
    item.start_at = datetime(sy, sm, sd)
    item.has_license = True
    item.has_anime = True
    item.has_manga = True

    session.add(item)
    for title in anime["data"]["Media"]["genres"]:
        genre = session.query(models.Genre).filter_by(name=title).first()
        if not genre:
            genre = models.Genre(name=title)
            session.add(genre)
        item.genres.append(genre)

    for data in anime["data"]["Media"]["tags"]:
        tag = models.Tags()
        tag.name = data["name"]
        tag.rank = data["rank"]
        tag.isGeneralSpoiler = data["isGeneralSpoiler"]
        tag.isMediaSpoiler = data["isMediaSpoiler"]
        tag.isAdult = data["isAdult"]
        session.add(tag)
        item.tags.append(tag)

    for data in anime["data"]["Media"]["characters"]["edges"]:
        character_id = int(data["id"])
        character = session.query(models.Characters).filter_by(character_id=character_id).first()
        if not character:
            character = models.Characters()
            character.character_id = int(data["id"])
            character.role = data["role"] 
            character.first = data["node"]["name"]["first"] 
            character.middle = data["node"]["name"]["middle"] 
            character.last = data["node"]["name"]["last"] 
            character.full = data["node"]["name"]["full"] 
            character.userPreferred = data["node"]["name"]["userPreferred"] 
            character.large_image = data["node"]["image"]["large"] 
            character.medium_image = data["node"]["image"]["medium"] 
            character.age = data["node"]["age"]
            character.description = data["node"]["description"] 
            character.gender = data["node"]["gender"]
            session.add(character)
            item.characters.append(character)
        
    for data in anime["data"]["Media"]["staff"]["edges"]:
        staff_id = int(data["node"]["id"])
        staff = session.query(models.Staff).filter_by(staff_id=staff_id).first()
        if staff is None:
            staff = models.Staff(
                staff_id=staff_id,
                role=data["role"],
                first=data["node"]["name"]["first"],
                middle=data["node"]["name"]["middle"],
                last=data["node"]["name"]["last"],
                full=data["node"]["name"]["full"],
                userPreferred=data["node"]["name"]["userPreferred"],
                large_image=data["node"]["image"]["large"],
                medium_image=data["node"]["image"]["medium"],
                age=data["node"]["age"],
                description=data["node"]["description"],
                gender=data["node"]["gender"])
            session.add(staff)
        item.staff.append(staff)




    session.commit()

json_data = {
            'query': open("./graphql/MediaQuery.graphql", "rt").read(),
            'variables': {
                "id":85470
            }
        }
anime = requests.post("https://graphql.anilist.co", json=json_data).json()
add_anime(anime)
          

#app.include_router(media_route)