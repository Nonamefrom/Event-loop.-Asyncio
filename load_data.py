import asyncio
from aiohttp import ClientSession
from databases import Database
from sqlalchemy.sql import insert
from migrate import characters

DATABASE_URL = "sqlite:///./database.db"

database = Database(DATABASE_URL)

API_URL = "https://swapi.dev/api/people/"


async def fetch_character(session, url):
    async with session.get(url) as response:
        character = await response.json()

        async def fetch_names(urls):
            names = []
            for u in urls:
                async with session.get(u) as res:
                    data = await res.json()
                    names.append(data.get("title") or data.get("name"))
            return ", ".join(names)

        films = await fetch_names(character["films"])
        species = await fetch_names(character["species"])
        starships = await fetch_names(character["starships"])
        vehicles = await fetch_names(character["vehicles"])

        return {
            "id": int(character["url"].split("/")[-2]),
            "birth_year": character.get("birth_year"),
            "eye_color": character.get("eye_color"),
            "films": films,
            "gender": character.get("gender"),
            "hair_color": character.get("hair_color"),
            "height": character.get("height"),
            "homeworld": character.get("homeworld"),
            "mass": character.get("mass"),
            "name": character.get("name"),
            "skin_color": character.get("skin_color"),
            "species": species,
            "starships": starships,
            "vehicles": vehicles,
        }


async def fetch_all_characters():
    async with ClientSession() as session:
        tasks = []
        async with session.get(API_URL) as response:
            data = await response.json()
            tasks.extend(fetch_character(session, p["url"]) for p in data["results"])
            while data.get("next"):
                async with session.get(data["next"]) as res:
                    data = await res.json()
                    tasks.extend(fetch_character(session, p["url"]) for p in data["results"])

        return await asyncio.gather(*tasks)


async def save_characters_to_db(data):
    async with database.transaction():
        query = insert(characters)
        await database.execute_many(query, data)


async def main():
    await database.connect()
    print("Fetching characters from SWAPI...")
    characters = await fetch_all_characters()
    print(f"Fetched {len(characters)} characters.")
    print("Saving to database...")
    await save_characters_to_db(characters)
    print("All characters saved.")
    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
