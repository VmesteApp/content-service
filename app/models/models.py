from sqlalchemy import MetaData, Table, Integer, String, Column, UUID, ForeignKey
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
    Column("founder_id", Integer),
    Column("description", String),
    Column("short_description", String),
)

images = Table(
    "images",
    metadata,
    Column("image_id", UUID, primary_key=True),
    Column("pulse_id", Integer, ForeignKey("pulse.id")),
    Column("image_path", String),
)

files = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("file_id", UUID),
    Column("file_path", String),
)

tag = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

pulse_tags = Table(
    "pulse_tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("tag_id", Integer)
)

pulse_members = Table(
    "pulse_members",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("user_id", Integer)
)

images = Table(
    "images",
    metadata,
    Column("image_id", UUID, primary_key=True),
    Column("pulse_id", Integer)
)
