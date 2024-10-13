import os

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Video


def save_temp_video(file: UploadFile):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    file_size = os.path.getsize(temp_path)
    return temp_path, file_size


async def search_videos(db: AsyncSession, file_name: str = None, file_size: int = None):
    query = select(Video)
    if file_name:
        query = query.where(Video.file_name.ilike(f"%{file_name}%"))
    if file_size:
        query = query.where(Video.file_size == file_size)
    result = await db.execute(query)
    videos = result.scalars().all()
    return videos
