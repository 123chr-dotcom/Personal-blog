from flask import Flask
from extensions import db, login_manager
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db.init_app(app)
login_manager.init_app(app)

# 导入蓝图
from auth import auth as auth_blueprint
from posts import posts as posts_blueprint
from comments import comments as comments_blueprint

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(comments_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
