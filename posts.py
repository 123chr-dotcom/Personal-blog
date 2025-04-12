from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Post, Comment
from extensions import db
from datetime import datetime

posts = Blueprint('posts', __name__)

@posts.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@posts.route('/create')
@login_required
def create():
    return render_template('create_post.html')

@posts.route('/create', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if not title or not content:
        flash('标题和内容不能为空')
        return redirect(url_for('posts.create'))
    
    new_post = Post(
        title=title,
        content=content,
        user_id=current_user.id
    )
    
    db.session.add(new_post)
    db.session.commit()
    flash('文章创建成功')
    return redirect(url_for('posts.index'))

@posts.route('/post/<int:id>')
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@posts.route('/edit/<int:id>')
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('你没有权限编辑这篇文章')
        return redirect(url_for('posts.index'))
    return render_template('edit_post.html', post=post)

@posts.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('你没有权限编辑这篇文章')
        return redirect(url_for('posts.index'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    if not title or not content:
        flash('标题和内容不能为空')
        return redirect(url_for('posts.edit', id=id))
    
    post.title = title
    post.content = content
    post.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash('文章更新成功')
    return redirect(url_for('posts.view_post', id=id))

@posts.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('你没有权限删除这篇文章')
        return redirect(url_for('posts.index'))
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除')
    return redirect(url_for('posts.index'))
