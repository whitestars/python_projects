import requests

page = requests.get("http://www.baidu.com/s?wd=123")
# print(page.text)
i = int(page.text.index("百度为您找到相关结果约"))
start = i +10
end = i + 25
print(page.text[start:end])
