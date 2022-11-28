import os
import zipfile
import datetime

# print(datetime.date.today())

def zip_file_backup(backup_path, src_folder_path, name):
    now_time = str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '-')
    backup_file = backup_path + name + '-' + now_time + '.zip'
    backup_file = backup_file.replace(' ', '')
    with zipfile.ZipFile(backup_file, mode='w') as zf:
        for parent, dirnames, filenames in os.walk(src_folder_path):        
            for filename in filenames:
                zf.write(src_folder_path + filename)

def remove_all_folder_file(src_folder_path):
    for parent, dirnames, filenames in os.walk(src_folder_path):        
            for filename in filenames:
                if (os.path.exists(src_folder_path + filename)):
                    # print(src_folder_path + filename)
                    os.remove(src_folder_path + filename)

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    print(dir + 'size is : ' + str(size) + ' bytes')
    return size

def backup(size):
    if getdirsize('static/img/') > size or getdirsize('static/results/') > size:
        zip_file_backup('static/backups/', 'static/img/', 'img')
        zip_file_backup('static/backups/', 'static/results/', 'results')
        remove_all_folder_file('static/img/')
        remove_all_folder_file('static/results/')

backup(size=100*1024*1024)
# 1024 * 1024 = 1 MB
# backup(size=1024*1024)