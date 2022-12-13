# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import os

# random file name
import hashlib
import datetime as dt

# image process
import cv2
from PIL import Image
from settings import *
from pixel_converter import *

# hash tool
from hash_delete_tool import *

# for twitter
from private_key import *
# private_key: secret_key, api_key, api_secret
import tweepy

# qrcode
from qrcode_process import qr_code_process

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

# for gallery
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')

# for twitter
@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
    auth = tweepy.OAuthHandler(api_key, api_secret)
    try:
        user_key = request.form['user_key']
        user_secret_key = request.form['user_secret_key']
    except:
        return redirect(auth.get_authorization_url())

    orginal_image = request.form['original_img_src']
    result_image = request.form['result_img_src']
    status = request.form['tweet_content'] + ' #PixelArtFilterWeb'
    filenames = [orginal_image, result_image]
    tweet(user_token=user_key, user_token_secret=user_secret_key, filenames=filenames, status=status)
    # filename = result_image
    # tweet(user_token=user_token, user_token_secret=user_secret_token, filenames=filenames, status=status)
    return redirect(url_for('index'))

# if user choose to give auth then will get callback
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    # get token or keys from url args
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

    return render_template(pixel_html_path, user_key = user_token, user_secret_key=user_secret_token)

    # this area is for debugging and testing twitter api

    # orginal_image = request.form['original_img_src']
    # result_image = request.form['result_img_src']
    # status = request.form['tweet_content']
    # filenames = [orginal_image, result_image]
    # filename = result_image
    # filename = 'static/sample/test.jpg'
    # filenames = ['static/sample/test.jpg', 'static/sample/test.png']
    # status = 'This message is from #PixelArtFilterWeb'
    # tweet(user_token=user_token, user_token_secret=user_secret_token, filenames=filenames, status=status)
    # return redirect(url_for('index'))
    # return user_token, user_secret_token

# you can't only use this route to tweet it need to get auth first
@app.route('/tweet')
def tweet(user_token=None, user_token_secret=None, filenames=['static/sample/test.jpg'], status='This message is from #PixelArtFilterWeb'):
    if user_token == None or user_token_secret == None:
        user_token = os.getenv('access-token')
        user_token_secret = os.getenv('access-token-secret')

    # api.update_status(f"A Tweet from PixelArtFilterWeb - {random.random()}")
    # You would read these values from the session
    
    # try:
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(user_token,user_token_secret)
    api = tweepy.API(auth)

    # api.update_status_with_media(filename=filename, status=status)

    # Upload images and get media_ids
    media_ids = []
    for filename in filenames:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)
    # Tweet with multiple images
    api.update_status(status=status, media_ids=media_ids)

    # except:
        # return render_template(pixel_html_path, user_key = '', user_secret_key='')

# return value between min and max
def around_value(value, min_num, max_num):
    value = max(value, min_num)
    value = min(value, max_num)
    return value

# change to 'en' lang
@app.route("/english",methods=['POST','GET'])
def english():
    # english to english
    global pixel_html_path, html_lang
    html_lang = 'en'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

# change to 'zh' lang
@app.route("/traditional_chinese")
def traditional_chinese():
    # tch to tch
    global pixel_html_path, html_lang
    html_lang = 'tch'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

# index get
@app.route('/', methods=['GET'])
def index():
    return render_template(pixel_html_path, language=html_lang)

# index post
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
    format_support = ['mp4', 'avi', 'gif','png','jpg','jpeg', 'webp']
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
        # if no image upload and no last image
        last_image_name = None
        if html_lang == 'tch':
            error='沒有選擇圖片'
        elif html_lang == 'en':
            error='Did not select image'
        return render_template(pixel_html_path, error=error)
    if img_file_name.split('.')[-1].lower() not in format_support:
        # if file type is not supported
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
    try:
        qrcode = bool(int(request.form['qr_code']))
    except:
        qrcode = False
    try:
        qrcode = bool(int(request.form['qr_code']))
    except:
        qrcode = False
    if qrcode:
        qrcode_content = request.values['qr_code_content']

    # twitter key
    try:
        user_key = request.form['user_key2']
    except:
        user_key = None
    try:
        user_secret_key = request.form['user_secret_key2']
    except:
        user_secret_key = None

    # random file name
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
    command_dict = pixel_set_to_dict(k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw, saturation=saturation, contrast=contrast, save_name=result_path)
    img_res, colors = convert(img_path, command_dict)

    if '\\' in img_path:
        last_image = img_path.split('\\')[-1]
    elif '/' in img_path:
        last_image = img_path.split('/')[-1]
    else:
        last_image = img_path

    if file_format in ['mp4', 'avi', 'flv']:
        # for videoes
        return render_template(pixel_html_path, user_key=user_key,  user_secret_key=user_secret_key, org_img=img_path, vid_result=result_path, colors=colors, last_image=last_image)
    else:
        # for gif and image
        if file_format in ['gif', 'GIF']:
            pass
        else:
            cv2.imwrite(result_path, img_res)
            # check_image_by_path('static/results/', result_path)
            # check_image_by_path('static/img/', img_path)
        if qrcode:
            result_path = qr_code_process(result_path, qrcode_content)

        return render_template(pixel_html_path, user_key=user_key,  user_secret_key=user_secret_key, org_img=img_path, result=result_path, colors=colors, last_image=last_image)

# page 413 error
@app.errorhandler(413)
def error_file_size(e):
    if html_lang == 'tch':
        error = '文件太大。 最大上傳大小為 ' + str(max_size_num) + 'MB。' + '  如果想要編輯大於' + str(max_size_num) + 'MB的檔案，請參考看看本地版：https://github.com/JingShing-Tools/Pixel-Art-transform-in-python'# + "<a href='https://github.com/JingShing-Tools/Pixel-Art-transform-in-python' target='_blank'>如果要沒有限制的本地版本，可以點擊這裡<\\a>"
    elif html_lang == 'en':
        error = 'File size is over restriction. Maxinum upload size is ' + str(max_size_num) + 'MB.' + '  If want to edit size more than' + str(max_size_num) + 'MB file. Please see local version: https://github.com/JingShing-Tools/Pixel-Art-transform-in-python'
    return render_template(pixel_html_path, error=error), 413

# page 404 error
@app.errorhandler(404)
def not_found(e):
    error = 'Not found'
    return render_template(pixel_html_path, error=error), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
