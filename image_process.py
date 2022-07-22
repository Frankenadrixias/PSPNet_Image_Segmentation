# --------------------------------------------#
# image_process.py
# 图像处理相关功能
# --------------------------------------------#
import os
import exifread
from PIL import Image


# 批量读取文件夹内图像拍摄信息，并重命名
def image_rename(image_path: str):

    folder = os.listdir(image_path)
    for file_name in folder:

        # 读取图像的exif信息
        img = exifread.process_file(open(image_path + file_name, 'rb'))
        shot_time_str = img['Image DateTime'].values

        # 重命名图像
        shot_time_str = shot_time_str.replace(':', '')
        shot_time_str = shot_time_str.replace(' ', '_')
        new_name = 'IMG_' + shot_time_str + '.jpg'
        print(new_name)

        os.rename(image_path + file_name, image_path + new_name)


# 对图片进行缩放裁剪
def image_resize(input_path: str, output_path: str, out_width: int , out_height: int):

    img = Image.open(input_path)
    width, height = img.size
    ratio = out_height / out_width

    # 如果图片过宽
    if width * ratio > height:

        # 应该裁剪左右两侧
        outlier = int((width - height / ratio) / 2)

        # 前两个坐标点是左上角坐标，后两个坐标点是右下角坐标，width在前，height在后
        box = (outlier, 0, width - outlier, height)

    else:
        # 应该裁剪上下两侧
        outlier = int((height - width * ratio) / 2)

        # 前两个坐标点是左上角坐标，后两个坐标点是右下角坐标，width在前，height在后
        box = (0, outlier, width, height - outlier)

    # 对图片进行裁剪与缩放
    region = img.crop(box)
    region = region.resize((out_width, out_height))

    region.save(output_path)


if __name__ == '__main__':

    # 当前图片存储路径
    img_path = './image/'
    # image_rename(img_path)

    file_folder = os.listdir(img_path)
    for files in file_folder:
        image_resize(img_path + files, 'image1/' + files, 1920, 1080)
