from enum import Enum


class URL_Constant:
    def __init__(self):
        self.anilist_api_base_url = "https://graphql.anilist.co"
        self.tokyo_insider_base_url = "https://www.tokyoinsider.com"
        self.anime_out_base_url = "https://www.animeout.xyz/wp-json/wp/v2/posts"
        self.hi10_anime_base_url = "https://hi10anime.com"
        self.gogoanime_base_url = "https://anitaku.to"
        self.drama_cool = "https://dramacool.com.pa/"
        self.hianime_base_url = "https://hianime.to"
        self.hianime_js_file = "https://megacloud.tv/js/player/a/prod/e1-player.min.js"
        
class GenderChoices(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    DEFAULT = 'DEFAULT'


class ErrorCode:
    INVALID_AUTHENTICATION_CREDENTIALS = 'INVALID_AUTHENTICATION_CREDENTIALS'
    INVALID_INPUT = "INVALID_INPUT"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PASSWORD_DOES_NOT_MATCH = "PASSWORD_DOES_NOT_MATCH"
    OLD_PASSWORD_DOES_NOT_MATCH = "OLD_PASSWORD_DOES_NOT_MATCH"


