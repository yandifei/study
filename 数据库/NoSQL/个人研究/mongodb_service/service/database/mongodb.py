from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.user import User
from app.models.image import Image
from app.models.browse import Browse
from app.models.favorite import Favorite


async def init_db():

    client = AsyncIOMotorClient(
        "mongodb://root:root@localhost:27017"
    )

    db = client["graduation_project"]

    await init_beanie(
        database=db,
        document_models=[
            User,
            Image,
            Browse,
            Favorite
        ]
    )

if __name__ == '__main__':
    init_db()