from sqlalchemy import Table, Column, Integer, DateTime, FLOAT
from datetime import datetime
import database


class Heart(database.Base):

    __tablename__ = 'heart'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow())
    bpm = Column(FLOAT, nullable=False)
