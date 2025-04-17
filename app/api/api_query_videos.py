from flask import render_template, request, jsonify, current_app
from app.services import VideoService
from app.enums import SortField
from . import api
import os


def format_play_count(play_count:int) ->str:
    """
    Format play count
    """
    return f'{play_count}' if play_count < 10000 else f'{play_count/1000}K'

def format_duration(duration:float) ->str:
    """
    Format duration to __m__s (duration < 1 hour) or __h__m(duration >= 1 hour)

    :param duration:
    :return formated duration:
    """
    duration = int(duration)
    return f'{duration//60:02d}m{duration%60:02d}s' if duration < 3600 else f'{duration//3600:02d}h{duration%3600:02d}m'

def format_size(size:float):
    """
    Format file size
    """
    return f'{size:.2f} MB' if size < 1024 else f'{size/1024:.2f} GB'


@api.route('/videos', methods=['GET'])
def api_videos():
    search = request.args.get('search', '').strip()
    category_id = request.args.get('Category', '')
    region_id = request.args.get('Region', '')
    era_id  = request.args.get('Era', '')
    resolution_id = request.args.get('Resolution', '')
    
    sort_by= request.args.get('sort', '')
    sort_order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    
    pagination = VideoService.query_videos(search = search,
                                          category_id = category_id,
                                          region_id = region_id,
                                          era_id = era_id,
                                          resolution_id = resolution_id,
                                          sort_by = sort_by,
                                          sort_order = sort_order,
                                          page = page,per_page = per_page)
    
    thumbnail_folder = current_app.config.get('THUMB_FOLDER')
    
    videos = [
                render_template('video-card.html',
                            video_name = video.name,
                            video_uuid = video.uuid,
                            thumb_path = os.path.join(thumbnail_folder, f'{video.uuid}.jpg'),
                            video_play_count = format_play_count(video.play_count),
                            video_duration = format_duration(video.duration),
                            video_resolution = video.resolution.name,
                            video_size = format_size(video.size),
                            video_upload_date = video.upload_date)
            for video in pagination.items]
    
    pages = render_template('pagination.html',
                            total = pagination.total,
                            has_prev = pagination.has_prev,
                            has_next = pagination.has_next,
                            current_page = pagination.page,
                            iter_pages = [p for p in pagination.iter_pages(left_edge=1, left_current=2, right_current=2, right_edge=1)]
    )
    
    return jsonify({
        'total':pagination.total,
        'videos': videos,
        'pages': pages
    })