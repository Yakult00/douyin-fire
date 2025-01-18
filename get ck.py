from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import re


def save_cookies(driver, index):
    """保存Cookies到文件"""
    cookies = driver.get_cookies()
    with open(f'cookies_{index}.txt', 'w') as f:
        f.write(json.dumps(cookies, ensure_ascii=True))


def load_cookies(driver, index):
    """从文件加载Cookies"""
    if os.path.exists(f'cookies_{index}.txt'):
        with open(f'cookies_{index}.txt', 'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_next_index():
    """获取下一个用户的索引"""
    cookies_files = [f for f in os.listdir() if re.match(r'cookies_\d+\.txt', f)]
    if not cookies_files:
        return 1
    indices = sorted([int(re.findall(r'\d+', f)[0]) for f in cookies_files])
    return indices[-1] + 1


# 设置Chrome选项，避免每次都要手动关闭通知弹窗
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

# 打开浏览器
driver = webdriver.Chrome(options=chrome_options)

# 访问对应地址
driver.get("https://douyin.com/")

# 获取下一个用户的索引
user_index = get_next_index()

# 尝试加载用户Cookies
load_cookies(driver, user_index)

# 刷新页面以应用Cookies
driver.refresh()

# 等待用户登录或确认已登录
input("请登录并确认已完成登录，然后按回车键继续...")

# 保存用户Cookies
save_cookies(driver, user_index)

# 关闭浏览器
driver.quit()

#https://blog.csdn.net/qq_40184254/article/details/140834879