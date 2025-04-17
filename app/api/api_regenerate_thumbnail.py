import os
from . import api
from flask  import jsonify, request,current_app
from app.extensions import db
from app.models import Video
from app.utils import thumbnail_generator


@api.route('/regenerate_thumbnail', methods=['POST'])
def api_regenerate_thumbnail():
    """
    Api for generating thumbnail.
    """
    video_uuid = request.form.get('video_uuid')
    custom_time = request.form.get('custom_time')

    video_folder = current_app.config.get('VIDEO_FOLDER')
    thumb_folder = current_app.config.get('THUMB_FOLDER')
    
    video_path = os.path.join(video_folder, f'{video_uuid}.mp4')
    thumb_path = os.path.join(thumb_folder, f'{video_uuid}.jpg')
    
    custom_time = float(custom_time) if custom_time else None

    video = Video.query.filter(Video.uuid == video_uuid)
    if not video:
        return jsonify({'error': 'Video not recorded.'}), 404
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'The video does not exist'}), 404    
    
    if thumbnail_generator(video_path, thumb_path, custom_time) is None:
        return jsonify({'error': 'Thumbnail generate failed.'}), 500
    
    return jsonify({'message': 'Thumbnail is generated successfully.'}), 200