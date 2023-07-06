
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv


from helper_folder.数据库表格 import  db
from helper_folder.网页逻辑处理 import upload_handle

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
session = db.session

current_directory = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_directory, 'ODS', '原始数据集')
app.config['UPLOAD_FOLDER'] = relative_path
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}

with app.app_context():
    db.create_all()
    db.session.commit()


####唯一需要封装的接口，request用来前端接excel的
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return upload_handle(request, db, app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])
    return render_template('upload.html')




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

