# from uuid import UUID
from sqlalchemy import MetaData, Table, Integer, String, Column, UUID
from sqlalchemy.orm import declarative_base


metadata = MetaData()
Base = declarative_base()

application = Table(
    "application",
    metadata,
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("candidate_id", Integer),
    Column("message", String),
    Column("status", String, default="PENDING"),
)

pulse = Table(
    "pulse",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String),
    Column("name", String),
    Column("description", String),
    Column("short_description", String),
)

tag = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("decription", String),
)

pulse_tags = Table(
    "pulse_tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("tag_id", Integer)
)

images = Table(
    "images",
    metadata,
    Column("image_id", UUID, primary_key=True),
    Column("pulse_id", Integer)
)
