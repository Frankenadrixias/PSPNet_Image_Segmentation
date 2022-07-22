import os
import random
from defaults import dataset_path

# 训练集和验证集数据的比例
train_val_percent = 1

# 训练集数据的比例
train_percent = 0.8

if __name__ == "__main__":
    print("Generate txt in ImageSets.")
    segFilePath = os.path.join(dataset_path, 'SegmentationClass')
    saveBasePath = os.path.join(dataset_path, 'ImageSets/Segmentation')

    # 筛选所有png文件
    temp_seg = os.listdir(segFilePath)
    total_seg = []
    for seg in temp_seg:
        if seg.endswith(".png"):
            total_seg.append(seg)

    # 划分训练集、验证集、测试集
    num = len(total_seg)
    tv = int(num * train_val_percent)
    tr = int(tv * train_percent)
    train_val = random.sample(range(num), tv)
    train = random.sample(train_val, tr)

    # 划分结果写入txt
    print("train and val size", tv)
    print("train size", tr)
    f_train_val = open(os.path.join(saveBasePath, 'train_val.txt'), 'w')
    f_test = open(os.path.join(saveBasePath, 'test.txt'), 'w')
    f_train = open(os.path.join(saveBasePath, 'train.txt'), 'w')
    f_val = open(os.path.join(saveBasePath, 'val.txt'), 'w')

    for i in range(num):
        name = total_seg[i][:-4] + '\n'
        if i in train_val:
            f_train_val.write(name)
            if i in train:
                f_train.write(name)
            else:
                f_val.write(name)
        else:
            f_test.write(name)

    f_train_val.close()
    f_train.close()
    f_val.close()
    f_test.close()
    print("Generate txt in ImageSets done.")
