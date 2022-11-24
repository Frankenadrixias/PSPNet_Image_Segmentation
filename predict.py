# -------------------------------------#
# predict.py
# 对单张图片、视频或文件夹进行预测
# -------------------------------------#
import os
import time
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import defaults
from tqdm import tqdm
from PIL import Image
from pspnet import PspNet

#设置警告等级阈值
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


# 展示图像中各类别像素的占比
def show_data(array):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(len(defaults.classes))
    ax.barh(x, array, tick_label=defaults.classes)
    ax.invert_yaxis()
    ax.set_title("Proportion of Pixels in Different Categories", fontsize=14)
    plt.show()


if __name__ == "__main__":

    # 实例化PSPNet对象
    psp_net = PspNet()

    # mode用于指定测试的模式
    mode = "dir_predict"

    # 以下三个设置仅在video模式时有效，只有ctrl+c退出或运行到最后一帧才会完成保存。
    # video_path指定视频的路径，当video_path = 0时表示检测摄像头
    video_path = ''
    # video_save_path表示视频保存的路径
    video_save_path = "video/test.mp4"
    # video_fps用于保存的视频的fps
    video_fps = 24.0

    # test_interval用于指定测量fps的时候图片检测的次数，该值越大fps越准确。
    test_interval = 100

    # 以下两个设置仅在dir_predict模式时有效
    # dir_origin_path指定了用于检测的图片的文件夹路径
    dir_origin_path = r'E:\Downloads\青藏高原街景\2022.07青海\20220721-杂多县\侧方\杂多县'
    # dir_save_path指定了检测完图片的保存路径
    dir_save_path = "imgdir_out/"
    # csv_save_path指定了图片类别数据的保存路径
    csv_save_path = "imgdir_out/result.csv"

    # predict模式：对单张图片进行预测
    if mode == "predict":

        img_path = ''
        while img_path != "exit":
            try:
                img_path = input('Input image filename:')
                image = Image.open(img_path)
            except IOError:
                print('Open Error! Try again!')
                continue
            else:
                r_image, count = psp_net.detect_image(image)
                show_data(count)

                # 如果想要保存，利用r_image.save("img.jpg")即可保存。
                r_image.show()

    # video模式：视频检测，可调用摄像头或者读取视频进行检测
    elif mode == "video":

        if video_save_path != "":
            capture = cv2.VideoCapture(video_path)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            output = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

            ref, frame = capture.read()
            if not ref:
                raise ValueError("Failed to read the camera (video) correctly, "
                                 "please check whether the camera (video path) is correct.")

            fps = 0.0
            while True:
                t1 = time.time()
                # 读取某一帧
                ref, frame = capture.read()
                if not ref:
                    break
                # 格式转变，BGRtoRGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 转变成Image
                frame = Image.fromarray(np.uint8(frame))
                # 进行检测
                frame = np.array(psp_net.detect_image(frame))
                # RGBtoBGR满足opencv显示格式
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                fps = (fps + (1. / (time.time() - t1))) / 2
                print("fps= %.2f" % fps)
                frame = cv2.putText(frame, "fps= %.2f" % fps, (0, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("video", frame)

                # 保留时间的最后8位
                c = cv2.waitKey(1) & 0xff
                if video_save_path != "":
                    output.write(frame)

                # esc键的ASCII码为27，按下说明终止预测
                if c == 27:
                    capture.release()
                    break

            print("Video Detection Done!")
            capture.release()

            print("Save processed video to the path :" + video_save_path)
            output.release()

        else:
            raise ValueError("Do not have correct video save path.")

        cv2.destroyAllWindows()

    # fps模式：测试预测视频时的fps，使用的图片是img里面的street.jpg
    elif mode == "fps":
        img = Image.open('img/street.jpg')
        tact_time = psp_net.get_FPS(img, test_interval)
        print(str(tact_time) + ' seconds, ' + str(1 / tact_time) + 'FPS, @batch_size 1')

    # dir_predict模式：遍历文件夹进行检测并保存，默认遍历imgdir文件夹，保存imgdir_out文件夹
    elif mode == "dir_predict":
        img_names = os.listdir(dir_origin_path)

        # 定义空列表
        img_data = []

        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                image_path = os.path.join(dir_origin_path, img_name)
                image = Image.open(image_path)
                r_image, count = psp_net.detect_image(image)
                img_data.append(count)

                # 保存图像
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name))

            else:
                print('Open Error! Try again!')
                break

        # 保存图像分割信息到csv文件
        img_array = pd.DataFrame(img_data, columns=defaults.classes)
        img_array.to_csv(csv_save_path, sep=',')

    # 所选择的模式不在规定范围内
    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
