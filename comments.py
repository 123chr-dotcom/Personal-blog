from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Comment, Post
from extensions import db
from datetime import datetime

comments = Blueprint('comments', __name__)

@comments.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    
    if not content:
        flash('评论内容不能为空')
        return redirect(url_for('posts.view_post', id=post_id))
    
    post = Post.query.get_or_404(post_id)
    
    new_comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post.id
    )
    
    db.session.add(new_comment)
    db.session.commit()
    flash('评论已添加')
    return redirect(url_for('posts.view_post', id=post_id))

@comments.route('/comment/<int:id>/delete')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.author != current_user:
        flash('你没有权限删除这条评论')
        return redirect(url_for('posts.view_post', id=comment.post_id))
    db.session.delete(comment)
    db.session.commit()
    flash('评论已删除')
    return redirect(url_for('posts.view_post', id=comment.post_id))
