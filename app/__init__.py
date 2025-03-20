import logging, time, os, datetime
from dotenv import load_dotenv
from datetime import timedelta


#sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ', 
                    level=logging.ERROR)
LOGGER = logging.getLogger(__name__)



load_dotenv('config.env')

def getConfig(name: str):
    return os.environ[name]





DATABASE_URL = getConfig('DATABASE_URL')
ALGORITHM = getConfig('ALGORITHM')
SECRET_KEY = getConfig('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getConfig('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(getConfig('REFRESH_TOKEN_EXPIRE_MINUTES'))
ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_LIFETIME: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)




# Create an engine and Create a base class for ORM models
engine = create_engine(DATABASE_URL)
Base = declarative_base()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)





botStartTime = time.time()
current_year = datetime.datetime.now().year





def get_db_session():
    with session() as ses:
        yield ses
