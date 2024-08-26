# web/app.py
import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask import render_template

app = Flask(__name__, static_folder='static', template_folder='templates')  # 设置静态文件夹和模板文件夹
CORS(app)


# 在根目录下提供服务
@app.route('/')
def serve_index():
    # send_from_directory函数用于发送指定目录下的文件
    # 将应用的静态资源目录下的web301.html返回给客户端
    return app.send_static_file('web301.html')


@app.route('/get_artist_info', methods=['POST'])
# 上面这句话的'/get_artist_info'是什么意思？
# 回答：'/get_artist_info'是应用中定义的路由，用于处理通过POST请求访问'/get_artist_info'路径的请求。
# 回答：POST是一种HTTP请求方法，用于向服务器发送数据，通常用于提交表单数据。
def get_artist_info():
    # 从请求的表单数据中获取名称
    artist_name = request.form.get('question')

    # 构建查询艺术家信息的URL
    url = f"https://zh.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"

    # 发送HTTP GET请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'lxml')

        # 初始化结果字典
        result = {}

        # 查找音乐类型
        music_type = soup.find('th', string='音乐类型')
        if music_type:
            music_type = music_type.find_next_sibling('td')
            if music_type:
                result['音乐类型'] = music_type.get_text(strip=True)

        # 查找出道地点
        debut_location = soup.find('th', string='出道地点')
        if debut_location:
            debut_location = debut_location.find_next_sibling('td')
            if debut_location:
                result['出道地点'] = debut_location.get_text(strip=True)

    #         TODO
    return jsonify(result)  # 返回JSON数据


if __name__ == '__main__':
    app.run(debug=True)
