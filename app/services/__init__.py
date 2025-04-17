#app/services/video_service.py
from app.models import Video,Category,Region,Era,Tag,Resolution, db
from flask_sqlalchemy.pagination import Pagination
from werkzeug.datastructures import FileStorage
from flask import current_app
from app.enums import SortField, ModelField
from app.utils import thumbnail_generator, get_video_duration, get_video_resolution, secure_filename
import os,uuid




def allowed_file(filename:str) -> bool:
    """判断上传文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS')

class VideoService:
    @staticmethod
    def append_video(file:FileStorage):
        if file.filename == '':
            return [False, 'No file selected']
    
        if not allowed_file(file.filename):
            return [False, 'The file extension is unsupported.']
        
        
        video_name = secure_filename(file.filename.rsplit('.', 1)[0])
        if Video.query.filter_by(name = video_name).first() is not None:
            return [False, 'The file name has been used.']
        
        abs_video_folder = current_app.config.get('ABS_VIDEO_FOLDER')
        abs_thumb_folder = current_app.config.get('ABS_THUMB_FOLDER')

        video_uuid = f"{uuid.uuid4().hex}"
        while Video.query.filter_by(uuid = video_uuid).first() is not None:
            video_uuid = f"{uuid.uuid4().hex}"
        
        
        video_path = os.path.join(abs_video_folder, f'{video_uuid}.mp4')
        thumb_path = os.path.join(abs_thumb_folder, f'{video_uuid}.jpg')
        
        file.save(video_path)
        os.chmod(video_path, 0o666)
        video_size = os.path.getsize(video_path)/(1024*1024) # bit -> mb
        video_dura = get_video_duration(video_path) 
        video_resl = get_video_resolution(video_path)
        thumbnail_generator(video_path, thumb_path)
        
        video = Video(name=video_name, uuid=video_uuid, size=video_size, duration=video_dura)
        resolution = Resolution.query.filter_by(name = video_resl).first()
        if not resolution:
            resolution = Resolution(name = video_resl)
            db.session.add(resolution)

            video.resolution = resolution
            db.session.add(video)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return [False, 'Fail to commit changes to db.']
        
    @staticmethod
    def delete_video(video_id:int):
        video = Video.query.get(video_id)
        video:Video
        if not video:
            return [False, "Video doesn't exist."]
        
        m2m_dict = video.get_m2m_dict()
        o2m_dict = video.get_o2m_dict()

        for cls_name, lst in m2m_dict.items():
            for obj_name in lst:
                VideoService.rm_video_from(video, cls_name, obj_name)

        for cls_name, obj_name in o2m_dict.items():
            VideoService.rm_video_from(video, cls_name, obj_name)

        try:
            db.session.delete(video)
            db.session.commit()
            return [True]
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return [False, 'Fail to commit changes to db.']

    @staticmethod
    def query_videos(search=None, 
                     category_id=None, 
                     region_id=None, 
                     era_id=None, 
                     resolution_id=None, 
                     tags=None, 
                     sort_by=SortField.DATE.value, sort_order='desc',
                     page=1, per_page=20) -> Pagination:
        
        query_obj = Video.query
        # --- 文字搜索 ---
        if search:
            query_obj = query_obj.filter(Video.name.contains(search))
    
        # --- 筛选 ---
        if category_id:
            query_obj = query_obj.filter(Video.categories.any(Category.id == category_id))
        if region_id:
            query_obj = query_obj.filter(Video.region_id == region_id)
        if era_id:
            query_obj = query_obj.filter(Video.era_id == era_id)
        if resolution_id:
            query_obj = query_obj.filter(Video.resolution_id == resolution_id)
        
        if tags and isinstance(tags, list):
            for tag_id in tags:
                query_obj = query_obj.filter(Video.tags.any(Tag.id == tag_id))

        sort_fields_map = {
            SortField.DATE.value: Video.upload_date,
            SortField.PLAYBACK.value: Video.play_count,
            SortField.DURATION.value: Video.duration,
            SortField.SIZE.value: Video.size,
        }
        
        sort_column = sort_fields_map.get(sort_by, Video.upload_date)
        if not sort_column:
            sort_column = Video.upload_date
        if sort_order == 'asc':
            query_obj = query_obj.order_by(sort_column.asc())
        else:
            query_obj = query_obj.order_by(sort_column.desc())

        return query_obj.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def play_video(video:Video):
        video.play_count += 1
        db.session.commit()
    
    @staticmethod
    def add_video_to(video_id, cls_neme, obj_name):

        model_field_map = {
            ModelField.CATEGORY: Category,
            ModelField.TAG: Tag,
            ModelField.ERA: Era,
            ModelField.REGION: Region,
            ModelField.RESOLUTION: Resolution,
        }

        cls = model_field_map.get(cls_neme, None)
        if not cls:
            return [False, 'Invalid model type.']
        video = Video.query.get(video_id)
        if not video:
            return [False, "Video doesn't exist."]
        if not obj_name:
            return [False, 'Object name is required.']
        obj = cls.query.filter_by(name = obj_name).first()
        if not obj:
            obj = cls(name = obj_name)
            db.session.add(obj)

        if video not in obj.videos:
            obj.videos.append(video)
        try:
            db.session.commit()
            return [True, f'Add {video.name} to {obj.name} successfully.']
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return [False, 'Fail to commit changes to db.']

    @staticmethod
    def rm_video_from(video_id, cls_name, obj_name):
        model_field_map = {
            ModelField.CATEGORY: Category,
            ModelField.TAG: Tag,
            ModelField.ERA: Era,
            ModelField.REGION: Region,
            ModelField.RESOLUTION: Resolution,
        }
        # cls = Category, Tag, Era, Region or Resolution
        cls = model_field_map.get(cls_name, None)
        if not cls:
            return [False, 'Invalid model type.']
        # comfirm video is exist.
        video = Video.query.get(video_id)
        if not video:
            return [False, "Video doesn't exist."]
        
        if not obj_name:
            return [False, 'Object name is required.']
        obj = cls.query.filter_by(name = obj_name).first()
        
        if not obj:
            return [False, f"The object {obj_name} doesn't exist."]
        
        if video not in obj.videos:
            return [False, f"The video {video.name} doesn't belong to {obj.name}."]
        
        obj.videos.remove(video)
        if not obj.videos:
            db.session.delete(obj)

        try:
            db.session.commit()
            return [True, f'Remove {video.name} from {obj.name} successfully.']
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return [False, 'Fail to commit changes to db.']
        

