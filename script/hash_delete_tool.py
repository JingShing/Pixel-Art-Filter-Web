import os
from PIL import Image
import imagehash

def check_image_by_path(folder_path, detect_file_path):
    check_file_format = ['png', 'jpg']
    detect_file = detect_file_path
    detect_file_name = detect_file.split('\\')[-1].split('//')[-1]
    detect_file_hash = imagehash.average_hash(Image.open(detect_file))
    for file_name in os.listdir(folder_path):
        if file_name.split('.')[-1] in check_file_format:
            try:
                hashed_image = imagehash.average_hash(Image.open(folder_path + file_name))
            except:
                continue
            if hashed_image==detect_file_hash and (folder_path+file_name != detect_file_path) and detect_file_name!=file_name:
                os.remove(folder_path + file_name)
                print('removed: ' + folder_path + file_name)

def check_image(folder_path, detect_file_name, hash_dict=dict()):
    check_file_format = ['png', 'jpg']
    detect_file = folder_path + detect_file_name
    detect_file_hash = imagehash.average_hash(Image.open(detect_file))
    hash_dict[detect_file]=detect_file_hash
    for file_name in os.listdir(folder_path):
        if file_name.split('.')[-1] in check_file_format:
            file_path = folder_path + file_name
            if file_path in hash_dict:
                hashed_image = hash_dict[file_path]
                print('hashed_image')
            else:
                try:
                    hashed_image = imagehash.average_hash(Image.open(file_path))
                    hash_dict[file_path] = hashed_image
                except:
                    continue
            if hashed_image==detect_file_hash and file_name != detect_file_name:
                os.remove(folder_path + file_name)
                print('removed: ' + folder_path + file_name)
    return hashed_image

def check_all_image(folder_path):
    hash_dict = {}
    check_file_format = ['png', 'jpg']
    for file_name in os.listdir(folder_path):
        if file_name.split('.')[-1] in check_file_format and os.path.isfile(folder_path+file_name):
            check_image(folder_path, file_name, hash_dict)
