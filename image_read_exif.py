# --------------------------------------------#
# image_read_exif.py
# 批量读取文件夹内图像拍摄信息，并重命名
# --------------------------------------------#
import os
import exifread

# 当前图片存储路径
img_path = './image/'
folder = os.listdir(img_path)

for file_name in folder:

    # 读取图像的exif信息
    img = exifread.process_file(open(img_path + file_name, 'rb'))
    shot_time_str = img['Image DateTime'].values

    # 重命名图像
    shot_time_str = shot_time_str.replace(':', '')
    shot_time_str = shot_time_str.replace(' ', '_')
    new_name = 'IMG_' + shot_time_str + '.jpg'
    print(new_name)

    os.rename(img_path + file_name, img_path + new_name)
