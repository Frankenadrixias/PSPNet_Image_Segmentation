# --------------------------------------------#
# json_to_dataset.py
# 将labelme标注出的json文件转换为数据集
# --------------------------------------------#
import base64
import json
import os
import os.path as osp
import numpy as np
import PIL.Image
import defaults
from labelme import utils

# 原始图像文件存储路径
jpgs_path = "datasets/JPEGImages"

# 标签文件存储路径
pngs_path = "datasets/SegmentationClass"

# 原始图像文件与json文件处理前的路径
count = os.listdir("./datasets/before/")

# 对所有文件循环遍历
for i in range(len(count)):
    path = os.path.join("./datasets/before", count[i])

    # 识别打开json文件
    if os.path.isfile(path) and path.endswith('json'):
        data = json.load(open(path))

        # 从imageData字段读取图像数据
        if data['imageData']:
            imageData = data['imageData']
        else:
            imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
            with open(imagePath, 'rb') as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode('utf-8')

        img = utils.img_b64_to_arr(imageData)
        label_name_to_value = {'background': 0}
        for shape in data['shapes']:
            label_name = shape['label']
            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value

        # label_values must be dense
        label_values, label_names = [], []
        for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
            label_values.append(lv)
            label_names.append(ln)
        assert label_values == list(range(len(label_values)))

        lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)

        PIL.Image.fromarray(img).save(osp.join(jpgs_path, count[i].split(".")[0] + '.jpg'))

        new = np.zeros([np.shape(img)[0], np.shape(img)[1]])
        for name in label_names:
            index_json = label_names.index(name)
            index_all = defaults.classes.index(name)
            new = new + index_all * (np.array(lbl) == index_json)

        # 存储图像文件和标签文件
        utils.lblsave(osp.join(pngs_path, count[i].split(".")[0] + '.png'), new)
        print('Saved ' + count[i].split(".")[0] + '.jpg and ' + count[i].split(".")[0] + '.png')
