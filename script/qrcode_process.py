from MyQR import myqr

def qr_code_process(src_path, content):
    result_paths = src_path.split('.')
    if result_paths[-1].lower()=='jpg':result_paths[-1]='png'
    result_path = result_paths[0] + '_qrcode.' + result_paths[-1]
    result_path = src_path.split('.')[0] + '_qrcode.' + src_path.split('.')[-1]
    myqr.run(words = content,
         picture = src_path,
         version=10, # this is length
         level = 'H', # debug level
         colorized = True, # color image
         save_name = result_path)
    return result_path

# qr_code_process(src_path='static/results/test.png', content='test')
