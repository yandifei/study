from  flask import Flask, render_template

# html在templates、图片在static（图片必须创建目录，不然没法识别）
app = Flask(__name__)   # html可以在声明的时候改


#创建了网址/show/info和函数index的对应关系
#以后用户在浏览器上访问/show/info，网站自动执行index
@app.route("/show/info")
# @app.route
def index():
    # with open("./resource/爱丽丝.png",'w', encoding="utf8") as png:
    #     return png
    # return "./resource/爱丽丝.png"
    # return"中<h1>国</h1><spanstyle='color:red;'>联通</span>"
    # FLask内部会自动打开这个文件，并读取内容，将内容给用户返回。

    # 默认：去当前项目目录的templates文件夹中找。
    return render_template("index.html")


@app.route("/get/news")
def get_news():
    return render_template("get_news.html")

# 用户列表
@app.route("/user/list")
def user_list():
    return render_template("user_list.html")

# 用户注册
@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)