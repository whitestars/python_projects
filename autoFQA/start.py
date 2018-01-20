import os
# import pytesseract
from PIL import Image
from aip import AipOcr
import webbrowser


def get_screenshot():
    cmd_screenshot = "adb shell /system/bin/screencap -p /sdcard/screenshot.png"
    cmd_pulltopc = "adb pull /sdcard/screenshot.png F:/PycharmProjects/autoFQA/screenshot.png"
    os.system(cmd_screenshot)
    os.system(cmd_pulltopc)


def handle_pic(pic_path):
    image = Image.open(pic_path)
    question_range = (0, 600, 1080, 880)
    answer_range = (200, 900, 900, 1800)
    question_pic = image.crop(question_range)
    answer_pic = image.crop(answer_range)
    question_pic.save("question_pic.png")
    answer_pic.save("answer_pic.png")


# def analyze_pic(pic_path):
#     image = Image.open(pic_path, "r")
#     text = pytesseract.image_to_string(image, lang="eng")
#     print(text)


def annlyze_pic_baidu(pic_path):
    App_ID = "10711384"
    API_Key = "QjpyKPAIaSdHrdBiu0RC82NH"
    Secret_Key = "5dZBW8wA49Bze4Ia3sXMS1pIhGI7kXc2"
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    baidu_acr = AipOcr(App_ID, API_Key, Secret_Key)
    with open(pic_path, "rb") as f:
        image = f.read()
    result = baidu_acr.basicAccurate(image, options)
    # print(result["words_result"])
    return result["words_result"]


def show_result(pic_path):
    handle_pic(pic_path)
    try:
        for i in annlyze_pic_baidu("question_pic.png"):
            question = i["words"]
    except:
        print("百度识别问题失败，请重试！")
    answers = []
    try:
        for i in annlyze_pic_baidu("answer_pic.png"):
            answers.append(i["words"])
    except:
        print("百度识别答案失败，请重试！")
    answer = " ".join(answers)
    return question, answer


def search_result(question):
    browser_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    webbrowser.register("chrom", None, webbrowser.BackgroundBrowser(browser_path))
    webbrowser.get("chrom").open("http://www.baidu.com/s?wd={}".format(question), new=1)


if __name__ == "__main__":
    pic_path = "screenshot.png"
    question, answer = show_result(pic_path)
    print(question, "\n", answer)
    search_result(question)
