from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.sql.expression import text
from datetime import datetime 

class Base(DeclarativeBase):
    pass

class Tasks(Base):

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str|None] = mapped_column(nullable=True) #? mentioned here because explicit is better than implicit
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    completed: Mapped[bool] = mapped_column(nullable=False, server_default='false')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}







