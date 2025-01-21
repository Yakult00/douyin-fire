import time
import json
import logging
from playwright.sync_api import sync_playwright
from one import wenan

# 配置日志记录
def setup_logging():
    log_file = 'exception_log.txt'
    logging.basicConfig(filename=log_file, level=logging.ERROR, encoding='utf-8',
                        format='%(asctime)s - %(levelname)s - %(message)s')

# 记录异常信息
def log_exception(exception, message=None):
    if message:
        logging.error(message)
    logging.exception(exception)

# 加载cookies
def load_cookies(cookie_file):
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_exception(e, f"读取或解析cookie文件时出错：{e}")
        return None

# 发送消息
def send_message(page, name, text):
    try:
        print(f"正在发送消息给 {name}...")
        page.get_by_text(name).click()
        page.locator("#douyin-header-menuCt").get_by_role("textbox").locator("div").nth(2).click()
        page.locator("#douyin-header-menuCt").get_by_role("textbox").fill(text)
        page.locator(".PygT7Ced > svg > path:nth-child(2)").click()
        print(f"消息发送给 {name} 成功")
        return True
    except Exception as e:
        log_exception(e, f"操作 {name} 时出错：{e}")
        return False

# 尝试点击私信按钮
def click_private_message_button(page):
    max_attempts = 3  # 最大尝试次数
    for attempt in range(max_attempts):
        try:
            print(f"尝试点击私信按钮（第 {attempt + 1} 次）...")
            # 等待私信按钮出现
            page.wait_for_selector("text=私信", timeout=10000)
            # 检查是否找到私信按钮
            count = page.locator("text=私信").count()
            print(f"找到 {count} 个私信按钮")
            if count > 0:
                # 使用更精确的选择器点击私信按钮
                page.get_by_text("私信").click()
                print("私信按钮点击成功")
                return True
            else:
                print("未找到私信按钮")
        except Exception as e:
            log_exception(e, f"点击私信按钮时出错（第 {attempt + 1} 次）：{e}")
        time.sleep(1)  # 每次尝试后等待 1 秒
    return False

# 主逻辑
def run(playwright):
    setup_logging()

    cookie_file = 'ck.txt'
    cookies = load_cookies(cookie_file)
    if not cookies:
        print("未加载到有效的 cookies，程序退出")
        return

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        print("正在访问抖音首页...")
        page.goto("https://douyin.com/")
        context.clear_cookies()
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie["expiry"]
            context.add_cookies([cookie])

        print("重新加载页面...")
        page.reload()

        # 尝试点击私信按钮
        if not click_private_message_button(page):
            print("私信按钮点击失败，程序退出")
            return

        names = ["name1", "name2", "name3", "name4"]
        first_click_success = 0
        text = wenan()

        if not text:
            print("文案为空，无法发送消息")
            return

        for name in names:
            if send_message(page, name, text):
                first_click_success += 1
                if first_click_success == 1:
                    print("首次发送成功，点击侧边栏")
                    page.locator(".FNb7nM4O > svg").click()
            time.sleep(0.7)

        current_cookies = context.cookies()
        print("当前 cookies:", current_cookies)

    except Exception as e:
        log_exception(e, "执行过程中出现异常：{e}")
    finally:
        print("关闭浏览器...")
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
