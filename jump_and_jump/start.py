import math
import os
import random
import time
import cv2
import numpy as np


# 截图保存到电脑，并获取图片对象
def screen_shot():
    # adb截图命令
    cmd_screen_shot = "adb shell /system/bin/screencap -p /sdcard/screenshot.png"
    os.system(cmd_screen_shot)
    # adb pull命令
    cmd_save = "adb pull /sdcard/screenshot.png screenshot.png"
    os.system(cmd_save)


# 测试用，加载本地图片
def test_check(image_origin, top_left, bottom_right):
    cv2.rectangle(image_origin, top_left, bottom_right, (0, 0, 255), 2)
    cv2.namedWindow("result", flags=0)
    cv2.imshow("result", image_origin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 取平台中心点
def find_box_location(origin_path, qizi_range):
    image_origin = cv2.imread(origin_path)
    h, w = image_origin.shape[:-1]
    image_edge = cv2.GaussianBlur(image_origin, (5, 5), 0)
    image_edge = cv2.Canny(image_edge, 1, 10)
    for k in range(qizi_range[0], qizi_range[2]):
        for b in range(qizi_range[1], qizi_range[3]):
            image_edge[b][k] = 0
    y_top = np.nonzero([max(row) for row in image_edge[400:]])[0][0] + 400
    x_top = int(np.mean(np.nonzero(image_edge[y_top])))

    max_y = y_top+5
    check_result = False
    for x in range(x_top+10, w):
        for y in range(y_top, h):
            if image_edge[y][x] != 0:
                if (y - max_y) < 3:
                    max_y = y
                    check_result = False
                    break
                else:
                    check_result = True
                    break
            else:
                continue
        if check_result:
            break

    box_x, box_y = x_top, max_y-5
    return box_x, box_y


# 寻找棋子的位置
def find_qi_location(qizi_path, origin_path):
    h, w = cv2.imread(qizi_path).shape[:-1]
    image_origin = cv2.imread(origin_path)
    image_qizi = cv2.imread(qizi_path)
    res = cv2.matchTemplate(image_origin, image_qizi, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    qizi_x = int((top_left[0]+bottom_right[0])/2)
    qizi_y = bottom_right[1]
    return qizi_x, qizi_y, top_left, bottom_right


def find_yuandian_location(yuandian_path, origin_path):
    h, w = cv2.imread(yuandian_path).shape[:-1]
    image_origin = cv2.imread(origin_path)
    image_yuandian = cv2.imread(yuandian_path)
    res = cv2.matchTemplate(image_origin, image_yuandian, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    # test_check(image_origin, top_left, bottom_right)
    print("圆点检测系数：", max_val)
    yuandian_x = int((top_left[0] + bottom_right[0]) / 2)
    yuandian_y = int((top_left[1]+bottom_right[1])/2)
    return max_val, yuandian_x, yuandian_y


def game_over(jieshu_path, origin_path):
    image_jieshu = cv2.imread(jieshu_path)
    image_origin = cv2.imread(origin_path)
    res = cv2.matchTemplate(image_origin, image_jieshu, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.6:
        return True


# adb swip操作，模拟长按
def jump(distance):
    # 固定常数，多次测试所得
    k = 1.37
    press_time = int(distance * k)
    # adb命令
    first_x = random.randint(100, 500)
    first_y = random.randint(200, 1000)
    cmd = "adb shell input swipe {0} {1} {2} {3} {4}".format(first_x, first_y, first_x, first_y, press_time)
    os.system(cmd)


def main():
    image_origin = "screenshot.png"
    image_qizi = "qizi.png"
    image_yuandian = "yuandian.png"
    image_jieshu = "jieshu.png"

    # 循环操作
    while True:
        screen_shot()
        if game_over(image_jieshu, image_origin):
            print("失败了！")
            break
        else:
            qizi = find_qi_location(image_qizi, image_origin)
            qizi_location = (qizi[0], qizi[1])
            yuandian = find_yuandian_location(image_yuandian, image_origin)
            if yuandian[0] > 0.8:
                box_location = (yuandian[1], yuandian[2])
                print("圆点定位！")
            else:
                top_l = list(qizi[2])
                bot_r = list(qizi[3])
                top_l.extend(bot_r)
                print(top_l)
                box_location = find_box_location(image_origin, top_l)
                print("边缘定位！")
            print("平台位置：", box_location)
            print("棋子位置：", qizi_location)
            distance = int(math.sqrt(
                math.pow(abs(box_location[0] - qizi_location[0]), 2) + math.pow(abs(box_location[1] - qizi_location[1]), 2)))
            print(distance)
            jump(distance)
            time.sleep(random.random()+1)


if __name__ == "__main__":
    main()