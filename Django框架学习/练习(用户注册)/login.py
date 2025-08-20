from flask import Flask, render_template, request

app = Flask(__name__)

# 主页面
@app.route("/",methods=["GET"])
def home():
    return "我是主页面"


# 用户注册
@app.route("/register" ,methods=["GET"])
def register():
    return render_template("register.html")

# 执行注册
@app.route("/do/reg" ,methods=["GET"])
def do_register():
    # 1.接收用户通过GET形式发送过来的数据
    print(request.args)
    # 2.给用户再返回结果
    return "注册成功"

# 执行注册（post方式）
@app.route("/post/reg" ,methods=["POST"])
def post_register():
    # 1.接收用户通过P0ST形式发送过来的数据
    print(request.form)
    # 2.给用户再返回结果
    return "注册成功"


if __name__ == '__main__':
    app.run(debug=True)