<%@page import="java.net.URLEncoder"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>成绩验证</title>
  </head>
  
  <body>
	<div style="width:600px; margin:40px auto; line-height:40px;">
  		<h3>&emsp;&emsp;&emsp;&emsp;成绩验证</h3>
	    <%
			request.setCharacterEncoding("UTF-8");
			String msg = "";
			
			String number 	= request.getParameter("number");
			String username = request.getParameter("username");
			String score 	= request.getParameter("score");	
			
			for (int f = 0; f < 1; /*f++*/) {
				if(number == null || username == null || score == null) {
					msg = "输入有误。";
					break;
				}
				number 		= number.trim();				//去除首尾空格
				username 	= username.trim();
				score		= score.trim();
				
				if(number.length() == 0 || username.length() == 0 || score.equals("")) {
					msg = "请将信息填写完整。";
					break;
				}
				
				if(number.length() < 2) {
					msg = "学号至少为2个字符";
					msg = URLEncoder.encode(msg, "UTF-8");	//进行URL编码
					String url = "show.jsp?msg=" + msg;
					response.sendRedirect(url);				//重定向，由浏览器完成转向
					return;					
				}

				msg = "恭喜，成绩录入成功！";
				String url = "show.jsp?msg=" + msg;
				// 必须适配版本，在课室的电脑IDEA中此方法不兼容
				request.getRequestDispatcher(url).forward(request, response);

				/*尝试直接重定向用类处理
				response.sendRedirect(url);
				建立继承HTTP接口的类
				*/
				return;					
			}
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
