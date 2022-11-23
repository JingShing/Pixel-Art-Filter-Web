import os
from PIL import Image
import imagehash

def check_image(folder_path, detect_file_name):
    check_file_format = ['png', 'jpg']
    detect_file = folder_path + detect_file_name
    detect_file_hash = imagehash.average_hash(Image.open(detect_file))
    for file_name in os.listdir(folder_path):
        if file_name.split('.')[-1] in check_file_format:
            hashed_image = imagehash.average_hash(Image.open(folder_path + file_name))
            if hashed_image==detect_file_hash and file_name != detect_file_name:
                os.remove(folder_path + file_name)
                print('removed: ' + folder_path + file_name)

def check_all_image(folder_path):
    check_file_format = ['png', 'jpg']
    for file_name in os.listdir(folder_path):
        if file_name.split('.')[-1] in check_file_format and os.path.isfile(folder_path+file_name):
            check_image(folder_path, file_name)