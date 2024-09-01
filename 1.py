import cv2
import numpy as np
from google.colab.widgets import Image
from IPython.display import display, clear_output


def take_photo(filename='photo.jpg', msg='Hello!'):
    """获取摄像头的一帧图像，并保存为文件"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return
    ret, frame = cap.read()
    if not ret:
        return
    # 释放摄像头资源
    cap.release()
    # 将BGR图像转换为RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 保存图像
    cv2.imwrite(filename, frame)
    print("{}: photo taken, saved at {}".format(msg, filename))
    # 使用matplotlib显示图像
    import matplotlib.pyplot as plt
    plt.imshow(frame)
    plt.show()

# 调用函数
take_photo()