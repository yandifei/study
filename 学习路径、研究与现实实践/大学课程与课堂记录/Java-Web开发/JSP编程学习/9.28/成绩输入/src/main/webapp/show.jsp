<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>成绩信息</title>
  </head>
  
  <body>  
	<div style="width:600px; margin:40px auto; line-height:40px;">
		<h3>&emsp;&emsp;&emsp;&emsp;成绩信息</h3>
		<%
			request.setCharacterEncoding("UTF-8");
			String msg = "";
			
			String number 	= request.getParameter("number");
			String username = request.getParameter("username");
			String score 	= request.getParameter("score");			
			msg 			= request.getParameter("msg");
		%>	
		&emsp;&emsp;<span style="color:red; font-size:small;"><%= msg %></span>
		<br>学号：<%= number %>
		<br>姓名：<%= username %>
		<br>成绩：<%= score %>
		<br><br>&emsp;&emsp;&emsp;&emsp;&emsp;
		<a href="index.jsp">成绩录入</a>	  
	</div>
  </body>
</html>