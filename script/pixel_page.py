# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
from PIL import Image
import hashlib
import datetime as dt
from settings import *
from pixel_converter import *
# hash tool
from hash_delete_tool import *
# for twitter
from private_key import secret_key, api_key, api_secret
import tweepy
import random
pixel_html_pre_path = 'pixel'
pixel_html_pro_path = '.html'
html_lang = 'tch'
def get_pixel_html_name():
    # pixel_lang.html
    return pixel_html_pre_path + '_' + html_lang + pixel_html_pro_path
pixel_html_path = get_pixel_html_name()
static_path = 'static/'

# file setting
# file max size how many MB
max_size_num = 2
# max image length
max_size_length = 2048

# app init
app = Flask(__name__)
config = {'MAX_CONTENT_LENGTH': 1024 * 1024 * max_size_num, 'DEBUG': False, 'SECRET_KEY':secret_key}
app.config.update(config)

# for twitter
@app.route('/twitter')
def twitter():
    auth = tweepy.OAuthHandler(api_key, api_secret)
    return redirect(auth.get_authorization_url())
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    args = request.args
    oauth_token = args['oauth_token']
    oauth_verifier = args['oauth_verifier']
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
    auth.get_access_token(oauth_verifier)
    user_token = auth.access_token
    user_secret_token = auth.access_token_secret
    # user_tokens = f"access-token={auth.access_token}<br>access-token-secret={auth.access_token_secret}"
    # return user_tokens
    return render_template(pixel_html_path)

@app.route('/tweet')
def tweet():
    # You would read these values from the session
    user_token = os.getenv('access-token')
    user_token_secret = os.getenv('access-token-secret')
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(user_token,user_token_secret)
    api = tweepy.API(auth)
    # Create a tweet - random() to not write same tweet twice
    api.update_status(f"A Tweet from Flask - {random.random()}")
 
    return "Tweet send with Flask"

def around_value(value, min_num, max_num):
    # return value between min and max
    value = max(value, min_num)
    value = min(value, max_num)
    return value

@app.route("/english",methods=['POST','GET'])
def english():
    # english to english
    global pixel_html_path, html_lang
    html_lang = 'en'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

@app.route("/traditional_chinese")
def traditional_chinese():
    # tch to tch
    global pixel_html_path, html_lang
    html_lang = 'tch'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

@app.route('/', methods=['GET'])
def index():
    return render_template(pixel_html_path, language=html_lang)

@app.route('/', methods=['POST'])
def post():
    # language part
    language = request.values['language']
    global pixel_html_path, html_lang
    if language:
        # if there is language set
        html_lang = language
    else:
        html_lang = 'en'
    pixel_html_path = get_pixel_html_name()

    # image process part
    img = request.files['image']
    last_image_name = request.values['last_image']
    format_support = ['mp4', 'avi', 'gif','png','jpg','jpeg']
    if img:
        # if it has image upload. Meaning it need to update new image.
        last_image_name = None
        img_file_name = img.filename
    elif '.' in last_image_name:
        # if it has last img name
        if 'img' in last_image_name:
            pass
        else:
            last_image_name = 'static/img/' + last_image_name
        img_file_name = last_image_name
        img_path = last_image_name
        result_path = last_image_name.replace('img', 'results')
    elif not img and not last_image_name:
        last_image_name = None
        if html_lang == 'tch':
            error='沒有選擇圖片'
        elif html_lang == 'en':
            error='Did not select image'
        return render_template(pixel_html_path, error=error)
    if img_file_name.split('.')[-1].lower() not in format_support:
        if html_lang == 'tch':
            error = "不支持這個格式。"
        elif html_lang == 'en':
            error = 'Do not support this file format.'
        return render_template(pixel_html_path, error=error)
    # get reference from page
    k = int(request.form['k'])
    scale = int(request.form['scale'])
    blur = int(request.form['blur'])
    erode = int(request.form['erode'])
    saturation = int(request.form['saturation'])
    contrast = int(request.form['contrast'])
    # avoid value broken
    # using around value to control between min and max
    k = around_value(k, 2, 16)
    scale = around_value(scale, 1, 10)
    blur = around_value(blur, 0, 255)
    erode = around_value(erode, 0, 255)
    saturation = around_value(saturation, -255, 255)
    contrast = around_value(contrast, -255, 255)

    # alpha and to_tw is check box so it need try and except
    try:
        alpha = bool(int(request.form['alpha']))
    except:
        alpha = False
    try:
        to_tw = bool(int(request.form['to_tw']))
    except:
        to_tw = False
    img_name = hashlib.md5(str(dt.datetime.now()).encode('utf-8')).hexdigest()

    if img:
        # if upload new img
        img_path = os.path.join(static_path+'img', img_name + os.path.splitext(img_file_name)[-1])
        img.save(img_path)
    # I move out to here to prevent error: not refreshing.
    result_path = os.path.join(static_path+'results', img_name + os.path.splitext(img_file_name)[-1])

    file_format = os.path.splitext(img_file_name)[-1].replace('.', '')
    if not file_format in ['mp4', 'avi', 'flv']:
        with Image.open(img_path) as img_pl:
            if max(img_pl.size) > max_size_length:
                img_pl.thumbnail((max_size_length, max_size_length), Image.ANTIALIAS)
                img_pl.save(img_path)
    # commands
    command_dict = pixel_set_to_dict(k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw, saturation=saturation, contrast=contrast)
    img_res, colors = convert(img_path, command_dict)

    if '\\' in img_path:
        last_image = img_path.split('\\')[-1]
    elif '/' in img_path:
        last_image = img_path.split('/')[-1]
    else:
        last_image = img_path

    if file_format in ['gif', 'GIF']:
        return render_template(pixel_html_path, org_img=img_path, result=result_path, colors=colors, last_image=last_image)
    elif file_format in ['mp4', 'avi', 'flv']:
        return render_template(pixel_html_path, org_img=img_path, vid_result=result_path, colors=colors, last_image=last_image)
    else:
        cv2.imwrite(result_path, img_res)
        check_image_by_path('static/results/', result_path)
        check_image_by_path('static/img/', img_path)
        return render_template(pixel_html_path, org_img=img_path, result=result_path, colors=colors, last_image=last_image)

@app.errorhandler(413)
def error_file_size(e):
    if html_lang == 'tch':
        error = '文件太大。 最大上傳大小為 ' + str(max_size_num) + 'MB。' + '  如果想要編輯大於' + str(max_size_num) + 'MB的檔案，請參考看看本地版：https://github.com/JingShing-Tools/Pixel-Art-transform-in-python'# + "<a href='https://github.com/JingShing-Tools/Pixel-Art-transform-in-python' target='_blank'>如果要沒有限制的本地版本，可以點擊這裡<\\a>"
    elif html_lang == 'en':
        error = 'File size is over restriction. Maxinum upload size is ' + str(max_size_num) + 'MB.' + '  If want to edit size more than' + str(max_size_num) + 'MB file. Please see local version: https://github.com/JingShing-Tools/Pixel-Art-transform-in-python'
    return render_template(pixel_html_path, error=error), 413

@app.errorhandler(404)
def not_found(e):
    error = 'Not found'
    return render_template(pixel_html_path, error=error), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
