import requests

# 设置接口URL
url = 'https://api.xygeng.cn/one'
def wenan():
    # 发送GET请求
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()

        # 提取origin、name和content字段
        origin = data['data']['origin']
        name = data['data']['name']
        content = data['data']['content']

        # 创建一个变量来存储格式化后的字符串
        formatted_output = f"{content}\n{origin.rjust(30)}"

        # 输出变量
        return formatted_output
    else:
        print('请求失败，状态码：', response.status_code)
        return 0