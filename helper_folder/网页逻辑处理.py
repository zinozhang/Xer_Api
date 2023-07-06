import os

import pandas as pd
from flask import url_for, redirect
from sqlalchemy import desc, and_

from helper_folder.数据库表格 import NewsData
from helper_folder.解读过程 import total_process


def allowed_file(filename, valid_type):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in valid_type


def upload_handle(request, db, folder, valid_type):
    if 'file' not in request.files:
        print('No file part')
        return 0
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return 0
    if file and allowed_file(file.filename, valid_type):

        # figure out test_version
        last_version = db.session.query(NewsData.test_version).order_by(desc(NewsData.test_version)).first()
        if last_version is None:
            last_version = 1
        else:
            last_version = int(last_version[0]) + 1

        filename = file.filename

        file.save(os.path.join(folder, filename))

        df = pd.read_excel(os.path.join(folder, filename))

        i = 0
        for index, row in df.iterrows():
            print(f"正在入库第{i}条")
            i += 1
            db_news = NewsData.query.filter(NewsData.text == row['文本']).first()

            if db_news is not None:
                print("news already exist")
                continue

            print("常规")
            newsData = NewsData(
                text=row['文本'],
                test_version=last_version,
            )
            db.session.add(newsData)

            db.session.commit()

        ###逻辑method
        total_process(1, 0, db)

        return redirect(request.url)
