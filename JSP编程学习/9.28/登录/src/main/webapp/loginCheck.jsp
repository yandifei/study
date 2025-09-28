<%@page import="java.net.URLEncoder"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>登录验证</title>
  </head>
  
  <body>
	<div style="width:600px; margin:40px auto; line-height:40px;">
		<h3>&emsp;&emsp;&emsp;&emsp;登录验证</h3>
		<%
			request.setCharacterEncoding("UTF-8"); 					//设定编码，否则输入的中文成乱码。须在获取输入值之前设定
			String msg = "";										//存放消息
			
			String username = request.getParameter("username"); 	//获取输入的值									
			String password = request.getParameter("password");
	
			for (int f = 0; f < 1; f++) {							//为了方便随时退出循环去执行本循环后面的语句
				if (username == null || password == null) {			//若控件名错误，或不是从表单提交而来，则为null
					msg = "未正确提交表单！";
					break;											//不符合要求，退出循环
				}
				username = username.trim();							//去除首尾空格
				
				if ((username.equals("tom") == false || password.equals("1") == false) 
						&& (username.equals("张三") == false || password.equals("1") == false)) {
					msg = "用户名或密码错误！";						//用户名或密码错误，两套条件都不满足
					break;
				}
				
				msg = username + "登录成功！";
				System.out.println("编码之前：" + msg);				//输出到控制台Console
				
				msg = URLEncoder.encode(msg, "UTF-8");				//URL转码。对于URL中的参数值
				System.out.println("编码之后：" + msg);
				
				String url = "main.jsp?msg="+ msg;					//URL参数msg的值是变量msg的值
				
				if (username.equals("tom")) {
					response.sendRedirect(url);						//重定向（通过浏览器重新发起跳转请求）
					System.out.println("编码：" + response.getCharacterEncoding());
					return;											//结束当前页面，不再继续执行本页的代码
				}
				
				if (username.equals("张三")) {						//转发。在服务器端直接跳转并转发request和response
					request.getRequestDispatcher(url).forward(request, response);											
					return;
				}
			}
		%>
		&emsp;&emsp;<span style="color:red; font-size:small;"><%= msg %></span>
		<br>用户名：<%= username %>
		<br>密　码：<%= password %>
		<br><br>&emsp;&emsp;&emsp;&emsp;&emsp;
		<a href="index.jsp">用户登录</a>	
	</div>
  </body>
</html>

