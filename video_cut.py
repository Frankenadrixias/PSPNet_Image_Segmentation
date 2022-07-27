# --------------------------------------------#
# video_cut.py
# 将视频按一定间隔裁剪为图片并保存
# --------------------------------------------#
import cv2
import os

# 设置视频帧率
rate = 30

global_video_path = 'E:\\Downloads\\青藏高原街景\\主视角\\2020.10沿边'


# 定义视频读取函数
# video_path和save_path分别存储读取与保存的文件路径
def read_video(video_path: str, save_path: str):

    # 读取视频文件
    cap = cv2.VideoCapture(video_path)

    # 正确识别帧
    if cap.isOpened():

        currentFrame = 0        # 从第0帧开始
        error = 0
        while cap.isOpened():

            # 循环读取视频帧，如果是帧率的整数倍则保存
            ret, frame = cap.read()
            if ret:
                error = 0
                if currentFrame % rate == 0:
                    save_image(frame, save_path, currentFrame, rate)
            else:
                error += 1

            if error >= 100:
                break

            # 继续读取下一帧
            currentFrame += 1

        # 视频读取结束
        cap.release()

    cv2.destroyAllWindows()


# 定义保存图片函数
# image：要保存的图片；addr：图片存储路径；num：视频第几帧
def save_image(image, addr, num, frame_rate):

    # 存储为jpg图像的路径与文件名
    local_path = addr + '\\' + str(int(num / frame_rate)) + '.jpg'

    # 将视频当前帧存储为图像
    cv2.imencode('.jpg', image)[1].tofile(local_path)
    print("Creating file... " + local_path)


if __name__ == '__main__':

    for folders in os.listdir(global_video_path):
        print(folders)
        file_path = os.path.join(global_video_path, folders)
        for files in os.listdir(file_path):
            local_video_path = os.path.join(file_path, files)
            local_save_path = os.path.join(file_path, files[:-4])

            # 如果保存路径不存在
            if not os.path.exists(local_save_path):
                # 创建多级文件路径
                os.makedirs(local_save_path)

            # 读取视频并保存为每秒一帧的图像
            read_video(local_video_path, local_save_path)
            print('Video reading finished. ---' + files)

