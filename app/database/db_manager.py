"""
db_manager.py

Purpose:
    Provides class DatabaseManager

Depends on:
    None
"""



from pymongo import AsyncMongoClient
from app.utils.config_manager import ConfigManager
import logging 
from rich.logging import RichHandler
logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
    datefmt="[%X]",
)


class DatabaseManager():
    """
    Class DatabaseManager provides a Mongo Asynchronous Client

    Args:
        - mongo_url (str): mongo url string
    """

    def __init__(self, mongo_url):
        """
        Class constructor method
        """
        url = mongo_url
        if url is None:
            logger.debug("Error: Cannot connect to DB!!")
            return False


        logger.debug("Connection successfull")
        self.client = AsyncMongoClient(url)
        self.db = self.client["devtrack"] # name of the database

    
    async def close(self):
        """
        Method close is used to close the asynchronous mongoclient connection
        """
        await self.client.close()






