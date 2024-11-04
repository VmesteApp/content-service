from sqlalchemy import MetaData, Table, Integer, String, Column, UUID, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func


metadata = MetaData()

application = Table(
    "application",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("candidate_id", Integer),
    Column("message", String),
    Column("status", String, default="PENDING"),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
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
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
    Column("blocked", Boolean, default=False)
)

images = Table(
    "images",
    metadata,
    Column("image_id", UUID, primary_key=True),
    Column("pulse_id", Integer, ForeignKey("pulse.id", ondelete="CASCADE")),
    Column("full_name", String),
    Column("image_path", String),
    Column("uploaded_at", DateTime, default=func.now()),
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

complaints = Table(
    "complaints",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pulse_id", Integer),
    Column("message", String),
    Column("status", String, default="PENDING"),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)
