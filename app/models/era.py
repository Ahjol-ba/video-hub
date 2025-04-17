from . import db, BaseMixin

# 年代与视频呈一对多关系
class Era(BaseMixin, db.Model):
    videos = db.relationship('Video', back_populates='era', lazy='select')
