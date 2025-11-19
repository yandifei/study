<%@page import="java.net.URLDecoder"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>用户功能</title>
  </head>
  
  <body>
	<div style="width:600px; margin:40px auto; line-height:40px;">
		<h3>&emsp;&emsp;&emsp;&emsp;用户功能</h3>
		<%
			request.setCharacterEncoding("UTF-8"); 					//设定编码，否则输入的中文成乱码。须在获取输入值之前设定
			String msg = "";										//存放消息
	
			String username = request.getParameter("username"); 	//获取输入的值。若不是从表单提交而来，则为null
			String password = request.getParameter("password");			
			msg 			= request.getParameter("msg");			//获取URL参数的值
			
			System.out.println("解码之前：" + msg);	
			
			if (msg != null) {
				msg = URLDecoder.decode(msg, "UTF-8"); 				//URL解码。对于URL参数值可省略解码
				System.out.println("解码之后：" + msg);
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
