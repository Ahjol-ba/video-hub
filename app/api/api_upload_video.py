#app/api/upload.py
from . import api
from flask  import jsonify, request
from app.services import VideoService



@api.route('/upload', methods=['POST'])
def api_upload_video():
    """
    Api for uploading videos.
    1. Check and save the uploaded video to the configured ABS_VIDEO_FOLDER.
    2. Return response information in JSON format.
    """
    if 'video' not in request.files:
        return jsonify({'error': 'There is not video file.'}), 400
    results = VideoService.append_video(request.files['video'])
    if results[0]:
        return jsonify({'message': 'Video is uploaded successfully'}), 200
    else:
        return jsonify('error', results[1]), 400


