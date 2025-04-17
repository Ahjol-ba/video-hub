#app/api/update
from . import api
from flask  import jsonify, request, current_app
from app.extensions import db
from app.utils import thumbnail_generator
from app.models import Video
from app.services import VideoService
from app.enums import ModelField

@api.route('/update', methods=['POST'])
def api_update_video():
    # 获取表单数据
    video_name = request.form.get('video_name', '')
    video_uuid = request.form.get('video_uuid', '')
    categories_str = request.form.get('categories', '')
    tags_str = request.form.get('tags', '')
    category_names = [c.strip() for c in categories_str.split(',') if c.strip()]
    tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
    
    
    video = Video.query.filter_by(uuid=video_uuid).first()
    if video:
        return jsonify({'error': 'Video is not found.'}), 400
    
    video.name = video_name
    db.session.commit()

    for cat_name in category_names:
        VideoService.add_video_to(video, ModelField.CATEGORY, cat_name)    
    for tag_name in tag_names:
        VideoService.add_video_to(video, ModelField.TAG, tag_name)    
    VideoService.add_video_to(video, ModelField.REGION, request.form.get('region'))    
    VideoService.add_video_to(video, ModelField.ERA, request.form.get('era'))
    
    return jsonify({
        'message': 'Video info update successfully.',
        'video': {
            'id': video.id,
            'uuid': video.uuid,
            'name': video.name,
            'categories': video.categories,
            'tags': video.tags,
            'era': video.era,
            'region': video.region,
        }
    }), 200

