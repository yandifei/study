<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>成绩录入</title>
  </head>
  
  <body>
	<div style="width:600px; margin:40px auto; line-height:40px;">
		<h3>&emsp;&emsp;&emsp;&emsp;成绩录入</h3>
	
		<form action="scoreCheck.jsp" method="post">
			学号：<input type="text" name="number">
			<br>
			姓名：<input type="text" name="username">
			<br>
			成绩：<input type="text" name="score">
			<br>&emsp;&emsp;&emsp;&emsp;&emsp;
			<input type="submit" value="提交">
		</form>
	</div>
  </body>
</html>
