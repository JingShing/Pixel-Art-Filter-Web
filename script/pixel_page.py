# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, abort, logging
import os
import cv2
from PIL import Image
import hashlib
import datetime as dt
from settings import *
from pixel_converter import *
pixel_html_path = 'pixel.html'
static_path = 'static/'
app = Flask(__name__)
config = {'MAX_CONTENT_LENGTH': 1024 * 1024 * 2, 'DEBUG': False}
app.config.update(config)

@app.route('/', methods=['GET'])
def index():
    return render_template(pixel_html_path)

@app.route('/', methods=['POST'])
def post():
    img = request.files['image']
    if not img:
        error='沒有選擇圖片'
        return render_template(pixel_html_path, error=error)
    k = int(request.form['k'])
    scale = int(request.form['scale'])
    blur = int(request.form['blur'])
    erode = int(request.form['erode'])
    try:
        alpha = bool(int(request.form['alpha']))
    except:
        alpha = False

    try:
        to_tw = bool(int(request.form['to_tw']))
    except:
        to_tw = False
    img_name = hashlib.md5(str(dt.datetime.now()).encode('utf-8')).hexdigest()
    img_path = os.path.join(static_path+'img', img_name + os.path.splitext(img.filename)[-1])
    result_path = os.path.join(static_path+'results', img_name + '.png')
    img.save(img_path)
    with Image.open(img_path) as img_pl:
        if max(img_pl.size) > 1024:
            img_pl.thumbnail((1024, 1024), Image.ANTIALIAS)
            img_pl.save(img_path)
    # commands
    command_dict = pixel_set_to_dict(k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw)
    img_res, colors = convert(img_path, command_dict)
    cv2.imwrite(result_path, img_res)
    return render_template(pixel_html_path, org_img=img_path, result=result_path, colors=colors)

@app.errorhandler(413)
def error_file_size(e):
    error = '文件太大。 最大上傳大小為 2MB。'
    return render_template(pixel_html_path, error=error), 413

@app.errorhandler(404)
def not_found(e):
    error = 'Not found'
    return render_template(pixel_html_path, error=error), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
