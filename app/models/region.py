from . import db, BaseMixin

# 地区与视频呈一对多关系
class Region(BaseMixin, db.Model):
    videos = db.relationship('Video', back_populates='region', lazy='select')

