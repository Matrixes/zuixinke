# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask.ext.login import login_required, current_user
from ..models import User, Post, Category
from .. import db
from . import blog
from .forms import PostForm


@blog.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items

    categories = Category.query.order_by(Category.tag).all()

    return render_template("blog/index.html",
                           posts = posts,
                           pagination = pagination,
                           categories = categories)



@blog.route('/post/<int:id>')
def post(id):
    post=Post.query.get_or_404(id)
    return render_template("blog/post.html",post=post)


@blog.route('/category/<int:id>')
def category(id):
    # 参数不使用url而是tag的话，模板中url_for('blog.category',tag=category.tag)
    # 会提示缺失tag，搞不懂为什么
    category = Category.query.get_or_404(id)
    if category.tag is None:
        abort(403)
    posts = category.posts.order_by(Post.timestamp.desc())
    return render_template('blog/category.html',category=category,posts=posts)


@blog.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category.tag = form.tag.data
        post.summary = form.summary.data
        post.body = form.body.data

        db.session.add(post)
        db.session.commit()


        flash(u'更改成功')
        return redirect(url_for('blog.post',id=post.id))
    form.title.data = post.title
    form.tag.data = post.category.tag
    form.summary.data = post.summary
    form.body.data = post.body
    return render_template('blog/publish.html',form=form)


@blog.route('/publish',methods=['GET','POST'])
@login_required
def publish():
    form = PostForm()

    try:
        category = Category.query.filter_by(tag = form.tag.data).first()
        if category is None:
            category = Category(tag = form.tag.data)
            db.session.add(category)
            db.session.commit()
    # 这个方法并不好，应该自定义个category为None的异常再捕获
    # 不知为什么第一个tag会提交个null上去
    except:
        abort(403)

    if form.validate_on_submit():
        # 不加上下面这句的话，post里的category=category会提示局部变量未定义
        category = Category.query.filter_by(tag = form.tag.data).first()

        post = Post(title = form.title.data,
                    summary = form.summary.data,
                    body = form.body.data,
                    category = category, #这个地方差点要了我的老命，千万别写成category=form.tag.data
                    author = current_user._get_current_object())

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.post',id=post.id))
    return render_template('blog/publish.html',form=form)
