#app/models/video.py
from . import db, video_category, video_tag, BaseMixin
import pytz
from datetime import datetime
from app.enums import ModelField
class Video(BaseMixin, db.Model):
    uuid = db.Column(db.String(255), unique=True, nullable=False, index=True) 
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(tz=pytz.timezone('Asia/Shanghai')))
    play_count = db.Column(db.Integer, default=0) 
    duration = db.Column(db.Float) 
    size = db.Column(db.Float)

    # 分类，多对多关系
    categories = db.relationship('Category', secondary=video_category, back_populates='videos', lazy='dynamic')    
    # 标签，多对多关系
    tags = db.relationship('Tag', secondary=video_tag, back_populates='videos', lazy='dynamic')

    # 外键关联到 Resolution 表
    resolution_id = db.Column(db.Integer, db.ForeignKey('resolution.id'))
    resolution = db.relationship('Resolution', back_populates='videos')

    # 外键关联到 Region 表
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), default=0)
    region = db.relationship('Region', back_populates='videos')

    # 外键关联到 Era 表
    era_id = db.Column(db.Integer, db.ForeignKey('era.id'), default=0)
    era = db.relationship('Era', back_populates='videos')
    
    def get_m2m_dict(self):
        return {ModelField.CATEGORY: list(self.categories), ModelField.TAG: list(self.tags)}

    def get_o2m_dict(self):
        return {ModelField.TAG: self.region, ModelField.ERA: self.era, ModelField.RESOLUTION: self.resolution}
