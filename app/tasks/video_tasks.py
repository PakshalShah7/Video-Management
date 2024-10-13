import asyncio
import logging
import os
import subprocess

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Video


logger = logging.getLogger(__name__)


async def convert_video_task(file_path: str, file_size: int, db: AsyncSession):
    try:
        file_name, _ = os.path.splitext(file_path)
        output_path = f"{file_name}_converted.mp4"
        await convert_video_ffmpeg(file_path, output_path)
        new_video = Video(file_name=output_path, file_size=file_size, format="mp4")
        db.add(new_video)
        await db.commit()
        await db.refresh(new_video)
    except Exception as e:
        logger.error(f"Error during video conversion: {e}")


async def convert_video_ffmpeg(input_path: str, output_path: str):
    """
    Convert any video format to .mp4 using ffmpeg.
    """
    command = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '22',
        '-strict', '-2',
        output_path
    ]
    proc = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        logger.error(f"ffmpeg error: {stderr.decode()}")
    else:
        logger.info(f"ffmpeg output: {stdout.decode()}")

    subprocess.run(command, check=True)
