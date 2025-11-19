<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>用户登录</title>
  </head>
  
  <body>
	<div style="width:600px; margin:40px auto; line-height:40px;">
		<h3>&emsp;&emsp;&emsp;&emsp;用户登录</h3>
		
		<form action="loginCheck.jsp" method="post">
			用户名：<input type="text" name="username">&ensp;tom或张三
			<br>
			密&emsp;码：<input type="password" name="password">&ensp;1
			<br>&emsp;&emsp;&emsp;&emsp;&emsp;
			<input type="submit" value="提交">
		</form>		
	</div>
  </body>
</html>
