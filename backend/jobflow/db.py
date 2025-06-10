"""
SQLAlchemy ORM – single table storing every workflow step.
"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    JSON,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import SQLITE_URL

engine = create_engine(SQLITE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id          = Column(Integer, primary_key=True)
    run_id      = Column(String, index=True)
    step        = Column(Integer)
    action      = Column(String(8))
    description = Column(Text)
    output      = Column(JSON)
    created_at  = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)