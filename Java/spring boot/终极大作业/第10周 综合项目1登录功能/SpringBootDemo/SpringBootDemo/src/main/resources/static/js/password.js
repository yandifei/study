var password = null;
var userPassword = null;
var changepassword1 = null;
var addBtn = null;
var backBtn = null;

$(function (){
    password = $("#password")
    userPassword = $("#userPassword")
    changepassword1 = $("#changepassword1")
    addBtn = $("#add");
    backBtn = $("#back");
    password.next().html("*");
    userPassword.next().html("*");
    changepassword1.next().html("*");
    password.on("blur",function (){
        if (password.val() != "" && password.val() != null){
            validateTip(password.next(),{"color":"green"},imgYes,true);
        }
    }).on("focus",function () {
        validateTip(password.next(),{"color":"#666666"},"* 请输入原密码",false);
    }).focus();

    userPassword.bind("focus",function(){
        validateTip(userPassword.next(),{"color":"#666666"},"* 密码长度必须是大于6小于20",false);
    }).bind("blur",function(){
        if(userPassword.val() != null && userPassword.val().length > 6
            && userPassword.val().length < 20 ){
            validateTip(userPassword.next(),{"color":"green"},imgYes,true);
        }else{
            validateTip(userPassword.next(),{"color":"red"},imgNo + " 密码输入不符合规范，请重新输入",false);
        }
    });

    changepassword1.bind("focus",function(){
        validateTip(changepassword1.next(),{"color":"#666666"},"* 请输入与上面一致的密码",false);
    }).bind("blur",function(){
        if(changepassword1.val() != null && changepassword1.val().length > 6
            && changepassword1.val().length < 20 && userPassword.val() == changepassword1.val()){
            validateTip(changepassword1.next(),{"color":"green"},imgYes,true);
        }else{
            validateTip(changepassword1.next(),{"color":"red"},imgNo + " 两次密码输入不一致，请重新输入",false);
        }
    });
    addBtn.on("click",function(){
        if(password.attr("validateStatus") != "true"){
            password.blur();
        }else if(userPassword.attr("validateStatus") != "true"){
            userPassword.blur();
        }else if(changepassword1.attr("validateStatus") != "true"){
            changepassword1.blur();
        }
		else{
            if(confirm("是否确认提交数据")){
                $("#userForm").submit();
            }
        }
    });

    backBtn.on("click",function(){
        if(referer != undefined
            && null != referer
            && "" != referer
            && "null" != referer
            && referer.length > 4){
            window.location.href = referer;
        }else{
            history.back(-1);
        }
    })
})