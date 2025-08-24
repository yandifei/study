from flask import Flask, render_template, request

app = Flask(__name__)

# 主页面
@app.route("/",methods=["GET"])
def home():
    return "我是主页面"


# 用户注册
@app.route("/register" ,methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 执行注册（post方式）
        # 1.接收用户通过P0ST形式发送过来的数据
        print(f"所有提交的内容：{request.form}")
        user = request.form.get("user_name")
        pwd = request.form.get("password")
        gender = request.form.get("gender")
        hobby_list = request.form.getlist("hobby")
        city = request.form.get("city")
        skill_list = request.form.getlist("skill")
        more = request.form.get("more")
        print(user, pwd, gender, hobby_list, city, skill_list, more)
        # 将用户信息写入文件中实现注册、写入到excel中实现注册、写入数据库中实现注册

        # 2.给用户再返回结果
        return "注册成功"

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        print(request.form)
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        print(user_name, password)
        return "登陆成功"


@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)