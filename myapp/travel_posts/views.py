from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import TravelPost
from myapp.travel_posts.forms import TravelPostForm

travel_posts = Blueprint('travel_posts', __name__)

@travel_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = TravelPostForm()
    if form.validate_on_submit():
        travel_post = TravelPost(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(travel_post)
        db.session.commit()
        flash('Travel Post Created')
        print('Travel post was created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@travel_posts.route('/<int:travel_post_id>')
def travel_post(travel_post_id):
    travel_post = TravelPost.query.get_or_404(travel_post_id) 
    return render_template('travel_post.html', title=travel_post.title, date=travel_post.date, post=travel_post)

@travel_posts.route('/<int:travel_post_id>/update',methods=['GET','POST'])
@login_required
def update(travel_post_id):
    travel_post = TravelPost.query.get_or_404(travel_post_id)

    if travel_post.author != current_user:
        abort(403)

    form = TravelPostForm()

    if form.validate_on_submit():
        travel_post.title = form.title.data
        travel_post.text = form.text.data
        db.session.commit()
        flash('Travel Post Updated')
        return redirect(url_for('travel_posts.travel_post',travel_post_id=travel_post.id))

    elif request.method == 'GET':
        form.title.data = travel_post.title
        form.text.data = travel_post.text

    return render_template('create_post.html',title='Updating',form=form)

@travel_posts.route('/<int:travel_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(travel_post_id):

    travel_post = TravelPost.query.get_or_404(travel_post_id)
    if travel_post.author != current_user:
        abort(403)

    db.session.delete(travel_post)
    db.session.commit()
    flash('Travel Post Deleted')
    return redirect(url_for('core.index'))