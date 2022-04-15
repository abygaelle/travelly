# core/views.py 

from flask import render_template, request, Blueprint
from myapp.models import TravelPost

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    travel_posts = TravelPost.query.order_by(TravelPost.date.desc()).paginate(page=page, per_page=8)
    return render_template('index.html', travel_posts=travel_posts)

@core.route('/info')
def info():
    return render_template('info.html')