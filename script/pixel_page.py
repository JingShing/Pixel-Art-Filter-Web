# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import os
import hashlib
import datetime as dt
import cv2
from PIL import Image
from pixel_process.settings import *
from pixel_process.pixel_converter import *
from pixel_process.qrcode_process import qr_code_process

app = Flask(__name__)
app.config.update({
    'MAX_CONTENT_LENGTH': 1024 * 1024 * 100,  # 100MB
    'DEBUG': False
})

# 常量設定
pixel_html_pre_path = 'pixel'
pixel_html_pro_path = '.html'
html_lang = 'tch'
SUPPORTED_FORMATS = ['mp4', 'avi', 'gif', 'png', 'jpg', 'jpeg', 'webp']
static_path = 'static/'
max_size_length = 50000  # Max image resolution
max_size_num = 100  # Max upload file size in MB

# HTML 路徑生成
def get_pixel_html_name():
    return f"{pixel_html_pre_path}_{html_lang}{pixel_html_pro_path}"

# 圖片檔名生成
def generate_file_name(extension=""):
    return hashlib.md5(str(dt.datetime.now()).encode('utf-8')).hexdigest() + extension

# 確保值在指定範圍內
def clamp_value(value, min_num, max_num):
    return max(min(value, max_num), min_num)

# 路由：畫廊頁面
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')

# 路由：首頁 (GET)
@app.route('/', methods=['GET'])
def index():
    return render_template(get_pixel_html_name(), language=html_lang)

# 路由：首頁 (POST)
@app.route('/', methods=['POST'])
def post():
    global html_lang
    html_lang = request.values.get('language', html_lang)
    
    # 圖片處理邏輯
    img = request.files.get('image')
    last_image_name = request.values.get('last_image')
    
    if not img and not last_image_name:
        return render_template(get_pixel_html_name(), error="沒有選擇圖片" if html_lang == 'tch' else "No image selected")

    img_file_name = img.filename if img else last_image_name
    img_path = os.path.join(static_path, 'img', generate_file_name(os.path.splitext(img_file_name)[-1]))
    result_path = img_path.replace('img', 'results')

    # 檢查支持的文件格式
    file_format = img_file_name.rsplit('.', 1)[-1].lower()
    if file_format not in SUPPORTED_FORMATS:
        return render_template(get_pixel_html_name(), error="不支持這個格式。" if html_lang == 'tch' else "Unsupported format")

    # 參數處理
    try:
        k = clamp_value(int(request.form['k']), 2, 16)
        scale = clamp_value(int(request.form['scale']), 1, 10)
        blur = clamp_value(int(request.form['blur']), 0, 255)
        erode = clamp_value(int(request.form['erode']), 0, 255)
        saturation = clamp_value(int(request.form['saturation']), -255, 255)
        contrast = clamp_value(int(request.form['contrast']), -255, 255)
        alpha = bool(int(request.form.get('alpha', 0)))
        to_tw = bool(int(request.form.get('to_tw', 0)))
        qrcode = bool(int(request.form.get('qr_code', 0)))
        qrcode_content = request.values.get('qr_code_content') if qrcode else ""
    except ValueError:
        return render_template(get_pixel_html_name(), error="無效的輸入參數")

    # 儲存圖片
    if img:
        img.save(img_path)

    # 圖片縮放
    if file_format not in ['mp4', 'avi']:
        with Image.open(img_path) as img_pl:
            if max(img_pl.size) > max_size_length:
                img_pl.thumbnail((max_size_length, max_size_length), Image.ANTIALIAS)
                img_pl.save(img_path)

    # 設定轉換參數
    command_dict = pixel_set_to_dict(k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, 
                                     saturation=saturation, contrast=contrast, save_name=result_path)

    img_res, colors = convert(img_path, command_dict)
    
    if file_format in ['mp4', 'avi']:
        return render_template(get_pixel_html_name(), org_img=img_path, vid_result=result_path, colors=colors)
    else:
        # 保存結果圖片
        cv2.imwrite(result_path, img_res)
        
        # 處理 QR Code
        if qrcode:
            result_path = qr_code_process(result_path, qrcode_content)

        return render_template(get_pixel_html_name(), org_img=img_path, result=result_path, colors=colors)

# 錯誤處理: 413 文件過大
@app.errorhandler(413)
def error_file_size(e):
    error_msg = f"文件太大。最大上傳大小為 {max_size_num}MB。"
    if html_lang == 'tch':
        error_msg += f" 如果想要編輯大於 {max_size_num}MB 的檔案，請參考本地版：https://github.com/JingShing-Tools/Pixel-Art-transform-in-python"
    return render_template(get_pixel_html_name(), error=error_msg), 413

# 錯誤處理: 404 未找到
@app.errorhandler(404)
def not_found(e):
    return render_template(get_pixel_html_name(), error='未找到頁面'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
