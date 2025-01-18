import time

from playwright.sync_api import sync_playwright
import json
import os
import re
from one import wenan
import logging


def setup_logging():
    log_file = 'exception_log.txt'
    logging.basicConfig(filename=log_file, level=logging.ERROR, encoding='utf-8',
                        format='%(asctime)s - %(levelname)s - %(message)s')


def log_exception(exception):
    logging.error(f"异常信息：{str(exception)}")


def run(playwright):
    setup_logging()

    cookie_file = 'ck.txt'
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_exception(f"读取或解析cookie文件时出错：{e}")
        return

    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://douyin.com/")

        context.clear_cookies()
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie["expiry"]
            context.add_cookies([cookie])

        page.reload()

        try:
            page.locator("div").filter(has_text=re.compile(r"^私信$")).locator("svg").click()
        except Exception as e:
            log_exception(f"点击私信按钮时出错：{e}")
            # browser.close()  # 注释掉此处，以便继续执行后续代码
            # return  # 注释掉此处，以便继续执行后续代码

        name = ["name1", "name2","name3","name4","name5","name6"]
        first_click_success = 0
        text = wenan()
        for i in range(len(name)):
            try:
                page.get_by_text(f"{name[i]}").click()
                page.locator("#douyin-header-menuCt").get_by_role("textbox").locator("div").nth(2).click()
                page.locator("#douyin-header-menuCt").get_by_role("textbox").fill(f"{text}")
                page.locator(".PygT7Ced > svg > path:nth-child(2)").click()
                first_click_success += 1
                if first_click_success == 1:
                    page.locator(".FNb7nM4O > svg").click()
            except Exception as e:
                log_exception(f"操作 {name[i]} 时出错：{e}")
                # 添加 continue 语句，出现异常时跳过当前循环，继续执行下一次循环
                continue
            time.sleep(0.7)

        # time.sleep(5)  # 可根据需要取消或减少延迟

        current_cookies = context.cookies()
        # print(current_cookies)

    except Exception as e:
        log_exception(f"执行过程中出现异常：{e}")
    finally:
        browser.close()


with sync_playwright() as playwright:
    run(playwright)
