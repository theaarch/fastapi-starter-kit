from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Recommended naming convention for constraints and indices
convention = {
    "ix": "%(table_name)s_%(column_0_label)s_index",
    "uq": "%(table_name)s_%(column_0_name)s_unique",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_foreign",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy 2.0 models."""

    metadata = MetaData(naming_convention=convention)
