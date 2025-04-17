# app/routes/index.py
from flask import render_template
from . import routes
from app.models import Category, Region, Era, Resolution
from app.enums import SortField

@routes.route('/')
def index():
    categories = Category.query.all() 
    regions = Region.query.all() 
    eras = Era.query.all()
    resolutions = Resolution.query.all()


    # 传入模板的筛选项和排序选项
    filters = { 'Category': categories, 'Region': regions, 'Era': eras, 'Resolution': resolutions }
    sort_keys = [sort_by.value for sort_by in SortField]

    return render_template('index.html', filtes=filters, sort_keys=sort_keys)

