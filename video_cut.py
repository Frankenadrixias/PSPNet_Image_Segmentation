# --------------------------------------------#
# video_cut.py
# 将视频按一定间隔裁剪为图片并保存
# --------------------------------------------#
import cv2


# 定义保存图片函数
# image：要保存的图片名字；addr：图片存储路径；num：视频第几帧
def save_image(image, addr, num, frame_rate):
    local_path = addr + str(int(num / frame_rate)) + '.jpg'
    cv2.imwrite(local_path, image)
    print("Creating file... " + local_path)


if __name__ == '__main__':

    # 读取视频文件
    cap = cv2.VideoCapture("video/GH020280.MP4")

    # 设置视频帧率
    rate = 24

    # 正确识别帧
    if cap.isOpened():

        # 从第0帧开始
        currentFrame = 0
        while cap.isOpened():

            # 循环读取视频帧
            ret, frame = cap.read()

            # 如果是帧率的整数倍则保存
            if ret & (currentFrame % rate == 0):
                save_image(frame, 'imgdir/', currentFrame, rate)

            # 继续读取下一帧
            currentFrame += 1

        # 视频读取结束
        cap.release()

    cv2.destroyAllWindows()
