# app/routes/upload.py
from flask import render_template,jsonify,current_app
from . import routes
from app.models import Video, Category, Tag, Era, Resolution, Region
import os 
@routes.route('/update/<uuid>')
def update(uuid):
    categories = Category.query.all() 
    regions = Region.query.all() 
    eras = Era.query.all()
    resolutions = Resolution.query.all()
    tags = Tag.query.all()
    video = Video.query.filter_by(uuid=uuid).filter()
    if video:
        video_name = video._role_name
        thumb_path = os.path.join('/app/static/videos/.thmubs',f'{video.uuid}.jpg')
        return render_template('update.html', 
                                video_name=video_name,
                                thumb_path = thumb_path,
                                categories=categories, 
                                regions=regions, 
                                eras=eras, 
                                resolutions=resolutions, 
                                tags=tags)
    else:
        return jsonify({'error', 'Video is not found.'})

# video_categories = video.categories,
# video_tags = video.tags,
# video_region = video.region,
# video_era = video.era,
# video_resolution = video.resolution,