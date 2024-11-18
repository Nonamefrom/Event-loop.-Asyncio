from sqlalchemy import (Column, Integer, String, create_engine, MetaData, Table)

DATABASE_URL = "sqlite:///./database.db"

metadata = MetaData()

characters = Table(
    "characters",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("birth_year", String),
    Column("eye_color", String),
    Column("films", String),  # Список фильмов через запятую
    Column("gender", String),
    Column("hair_color", String),
    Column("height", String),
    Column("homeworld", String),
    Column("mass", String),
    Column("name", String),
    Column("skin_color", String),
    Column("species", String),  # Список видов через запятую
    Column("starships", String),  # Список кораблей через запятую
    Column("vehicles", String),  # Список транспорта через запятую
)

engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Database schema created.")
