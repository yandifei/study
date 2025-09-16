<%@page import="java.text.SimpleDateFormat"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html lang="zh">
  <head>
	<title>当前日期时间</title>
  </head>

  <body>
	<div style="width:600px; margin:20px auto; line-height:40px;">
		<h3>当前日期时间</h3>
		<%
			Date date = new Date(); 					//当前时间
			out.println("时间1A：" + date); 				//输出到网页
			System.out.println("时间1：" + date); 		//输出到控制台console
		%>
		<br>时间1B：<% out.println(date); %>
		<br>时间1C：<%= date %>
		<%
			String date2A = String.format("%tF %tT", date, date); 		//时间格式化
			String date2B = String.format("%tF %<tT", date); 			//与上一行等效。第2个t调用第1个t的值

			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS，位于今年第w周，本月第W周，本周E");
			String date3 = sdf.format(date); 							//时间格式化
		%>
		<br>时间2A：<%= date2A %>
		<br>时间2B：<%= date2B %>
		<br>时间3：<%= date3 %>

		<!-- <br>时间4：<%= date %> 这是显示注释，在浏览器网页的源代码中会显示出来 -->
		<%-- <br>时间5：<%= date %> 这是隐式注释，不会发送到网页 --%>
		<%
			//out.println("时间6：" + date);				//这是隐式单行注释，这行代码不会运行
			/*
			out.println("时间7：" + date);				//这是隐式多行注释，这2行代码都不会运行
			out.println("时间8：" + date);
			*/
		%>
		<br><br>距离2030年元旦还有<%= interval("2030-1-1") %>天 			<!-- 调用函数 -->
		<br>距离北京2022年冬奥会闭幕已有<%= interval("2022-2-20") %>天
		<%!																//JSP声明。注意有感叹号“!”
			String interval(String dateInput) {
				String str = "";
				Date now = new Date();
				Date date = null;
				SimpleDateFormat sdf2 = new SimpleDateFormat("yyyy-MM-dd");

				try {
					date = sdf2.parse(dateInput);						//将字符串转换为日期类型
				} catch (Exception e) {
					return "输入错误";
				}

				long seconds = (date.getTime() - now.getTime()) / 1000;	//间隔秒数。用getTime()获得毫秒数
				seconds = Math.abs(seconds);							//求绝对值
				long days = seconds / (60 * 60 * 24);					//天数
				str = days + "";										//转换为字符串

				return str;
			}
		%>
	</div>
  </body>
</html>
