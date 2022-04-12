from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import TravelPost
from myapp.travel_posts.forms import TravelPostForm

travel_posts = Blueprint('travel_posts', __name__)