from sqlalchemy import Column, Integer, String, Boolean

from app.db import Base


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    format = Column(String, default="mp4")
    is_blocked = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "format": self.format,
            "is_blocked": self.is_blocked
        }
