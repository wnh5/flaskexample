# -*- coding:utf-8 -*-
#pip install flask-uploads
import os
from flask import Flask, request, g, flash, redirect, url_for, render_template, abort
from flask_uploads import UploadSet, configure_uploads

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '123456'

IMAGES = tuple('jpg JPG jpe jpeg png gif svg bmp'.split())

#第一个参数一定要是大写
photos = UploadSet('PHOTO',IMAGES)

# app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOADED_PHOTO_DEST'] = "/Users/liuche/tmp/"
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES

configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        # Flask-CouchDB 存储
        # rec = Photo(filename=filename, user=g.user.id)
        # rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', filename=filename))
    return render_template('upload.html')

@app.route('/photo/<filename>')
def show(filename):
    url = photos.url(filename)
    print url
    return render_template('show.html', url=url, filename=filename)

if __name__ == '__main__':
    app.run(port=8080)