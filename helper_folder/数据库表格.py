from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


#####sql 数据库设计



class NewsData(db.Model):
    __tablename__ = "舆情资料"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    test_version = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<舆情资料 {self.id}>'


class TestOnly(db.Model):
    __tablename__ = "测试表格"
    id = db.Column(db.String(100), primary_key=True)
    test_result = db.Column(db.String(100))
    ai_response = db.Column(db.String(100))


    def __repr__(self):
        return f'<测试表格 {self.client_id}>'
