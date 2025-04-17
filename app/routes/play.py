#app/routes/play.py
from flask import render_template, current_app
from . import routes
from app.models import Video
from app.services import VideoService
import os
@routes.route('/play/<uuid>')
def play(uuid):
    video = Video.query.filter_by(uuid=uuid).first_or_404()
    video_path = os.path.join(current_app.config.get("VIDEO_FOLDER"), f"{uuid}.mp4")
    VideoService.play_video(video)
    return render_template('play-video.html', video_name=video.name, video_path=video_path)
