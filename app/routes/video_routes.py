from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app.db import get_db_session
from app.models import Video
from app.services.video_service import save_temp_video, search_videos
from app.tasks.video_tasks import convert_video_task

router = APIRouter()


@router.post("/videos/upload")
async def upload_video(file: UploadFile, db: AsyncSession = Depends(get_db_session)):
    try:
        temp_path, file_size = save_temp_video(file)
        await convert_video_task(temp_path, file_size, db)
        return {"message": "Video upload initiated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/videos/search")
async def search_videos_endpoint(
        file_name: str = None, file_size: int = None, db: AsyncSession = Depends(get_db_session)
):
    videos = await search_videos(db, file_name=file_name, file_size=file_size)
    return {"videos": [video.to_dict() for video in videos]}


@router.get("/videos/download/{video_id}")
async def download_video(video_id: int, db: AsyncSession = Depends(get_db_session)):
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=400, detail="Video not found")
    if video.is_blocked:
        raise HTTPException(status_code=403, detail="Video is blocked from downloading")
    return FileResponse(video.file_name, media_type="application/octet-stream", filename=f"{video_id}.mp4")
