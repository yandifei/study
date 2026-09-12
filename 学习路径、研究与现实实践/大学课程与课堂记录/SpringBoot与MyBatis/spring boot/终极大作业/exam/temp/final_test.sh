#!/bin/bash
# Final comprehensive test - 超市订单管理系统
BASE="http://localhost:8080"
PASS=0; FAIL=0
COOKIE=/tmp/smbms_final_cookie.txt

green() { echo -e "\033[32m[PASS]\033[0m $1"; ((PASS++)); }
red() { echo -e "\033[31m[FAIL]\033[0m $1"; ((FAIL++)); }
info() { echo -e "\033[36m[INFO]\033[0m $1"; }
check() {
  if echo "$1" | grep -q "$2"; then green "$3"; else red "$3"; fi
}

rm -f $COOKIE

echo "=========================================="
echo "  超市订单管理系统 - 最终全量测试"
echo "=========================================="
info ">>> 1. 登录功能 <<<"
# 1.1 Login page
check "$(curl -s -o /dev/null -w '%{http_code}' $BASE/login)" "200" "登录页可访问(200)"
# 1.2 Wrong password
check "$(curl -s -X POST $BASE/dologin -d 'userCode=admin&userPassword=wrong')" "用户名或密码错误" "错误密码提示正确"
# 1.3 Correct login
curl -s -c $COOKIE -X POST "$BASE/dologin" -d 'userCode=admin&userPassword=1234567' -o /dev/null
check "$(curl -s -b $COOKIE $BASE/welcome)" "系统管理员" "正确登录显示用户名"
# 1.4 Logout
curl -s -b $COOKIE $BASE/logout -o /dev/null
check "$(curl -s -b $COOKIE $BASE/welcome -L)" "请登录后再访问" "注销后无法访问welcome"
curl -s -c $COOKIE -X POST "$BASE/dologin" -d 'userCode=admin&userPassword=1234567' -o /dev/null

info ">>> 2. 防跳转测试 <<<"
rm -f $COOKIE
check "$(curl -s $BASE/welcome -L)" "请登录后再访问" "未登录→welcome被拦截"
check "$(curl -s $BASE/userlist -L)" "请登录后再访问" "未登录→userlist被拦截"
check "$(curl -s $BASE/providerlist -L)" "请登录后再访问" "未登录→providerlist被拦截"
check "$(curl -s $BASE/orderslist -L)" "请登录后再访问" "未登录→orderslist被拦截"
curl -s -c $COOKIE -X POST "$BASE/dologin" -d 'userCode=admin&userPassword=1234567' -o /dev/null

info ">>> 3. 用户管理 <<<"
# 3.1 List
check "$(curl -s -b $COOKIE $BASE/userlist)" "用户管理页面" "用户列表页可访问"
# 3.2 POST search (URL-encoded Chinese)
BODY=$(curl -s -b $COOKIE -X POST "$BASE/userlist" -d 'queryname=%E7%B3%BB%E7%BB%9F&queryUserRole=0&pageNum=1')
check "$BODY" "系统管理员" "POST搜索→系统管理员"
# 3.3 Role filter
check "$(curl -s -b $COOKIE '$BASE/userlist?queryUserRole=1&pageNum=1')" "系统管理员" "角色筛选(管理员)"
# 3.4 View
check "$(curl -s -b $COOKIE $BASE/userview?uid=1)" "用户查看页面" "用户查看页可访问"
check "$(curl -s -b $COOKIE $BASE/userview?uid=1)" "admin" "用户查看显示编码"
# 3.5 Modify page
check "$(curl -s -b $COOKIE $BASE/usermodify?uid=1)" "用户修改页面" "用户修改页可访问"
# 3.6 Add page
check "$(curl -s -b $COOKIE $BASE/useradd)" "用户添加页面" "用户添加页可访问"
# 3.7 AJAX check user code
check "$(curl -s -b $COOKIE $BASE/ucexist?userCode=admin)" "exist" "AJAX→admin已存在"
check "$(curl -s -b $COOKIE '$BASE/ucexist?userCode=nobody123')" "noexist" "AJAX→nobody123不存在"

info ">>> 4. 用户CRUD操作 <<<"
# 4.1 Add user
HTTP=$(curl -s -w "%{http_code}" -b $COOKIE -X POST "$BASE/useraddsave" \
  -d 'userCode=zzztest99&userName=CRUD测试&userPassword=123456&gender=1&phone=13800000001&address=北京市&userRole=3&birthday=2000-01-01' -o /dev/null)
check "$HTTP" "302" "添加用户→302重定向"
# Find user across all pages
FOUND=0; for p in 1 2 3 4 5; do
  if curl -s -b $COOKIE "$BASE/userlist?pageNum=$p" | grep -q "zzztest99"; then
    FOUND=1; break
  fi
done
[ $FOUND -eq 1 ] && green "添加用户在列表中找到" || red "添加用户在列表中未找到"

# 4.2 Modify user
MYUID=$(curl -s -b $COOKIE "$BASE/userlist?pageNum=$p" | grep -oP 'userid="\K[0-9]+(?=" username="CRUD测试")' 2>/dev/null)
if [ -n "$MYUID" ]; then
  HTTP=$(curl -s -w "%{http_code}" -b $COOKIE -X POST "$BASE/usermodifysave" \
    -d "id=$MYUID&userCode=zzztest99&userName=CRUD修改&gender=2&phone=13900000002&address=上海市&userRole=2" -o /dev/null)
  check "$HTTP" "302" "修改用户→302重定向"
  # Verify modification
  BODY=$(curl -s -b $COOKIE "$BASE/userlist?pageNum=$p")
  check "$BODY" "CRUD修改" "用户名已修改为CRUD修改"
else
  red "找不到测试用户ID"
fi

# 4.3 Delete user (AJAX)
if [ -n "$MYUID" ]; then
  RESULT=$(curl -s -b $COOKIE "$BASE/deluser?uid=$MYUID")
  check "$RESULT" "true" "AJAX删除用户返回true"
else
  red "无法删除(无ID)"
fi

info ">>> 5. 供应商管理 <<<"
check "$(curl -s -b $COOKIE $BASE/providerlist)" "供应商管理页面" "供应商列表页可访问"
check "$(curl -s -b $COOKIE $BASE/providerlist)" "北京三木堂" "列表显示供应商数据"
check "$(curl -s -b $COOKIE $BASE/providerview?providerid=1)" "供应商查看页面" "供应商查看页可访问"
check "$(curl -s -b $COOKIE $BASE/providermodify?providerid=1)" "供应商修改页面" "供应商修改页可访问"
check "$(curl -s -b $COOKIE $BASE/provideradd)" "供应商添加页面" "供应商添加页可访问"

info ">>> 6. 订单管理 <<<"
check "$(curl -s -b $COOKIE $BASE/orderslist)" "订单管理页面" "订单列表页可访问"
check "$(curl -s -b $COOKIE $BASE/orderslist)" "洗发水" "列表显示订单数据"
check "$(curl -s -b $COOKIE $BASE/ordersview?billid=1)" "订单查看页面" "订单查看页可访问"
check "$(curl -s -b $COOKIE $BASE/ordersmodify?billid=1)" "订单修改页面" "订单修改页可访问"
check "$(curl -s -b $COOKIE $BASE/ordersadd)" "订单添加页面" "订单添加页可访问"

info ">>> 7. 密码修改 <<<"
check "$(curl -s -b $COOKIE $BASE/changepassword)" "修改密码页面" "密码修改页可访问"
check "$(curl -s -b $COOKIE '$BASE/jsp/user.do?method=pwdmodify&oldpassword=1234567')" "true" "AJAX验证旧密码正确"
check "$(curl -s -b $COOKIE '$BASE/jsp/user.do?method=pwdmodify&oldpassword=wrong')" "false" "AJAX验证旧密码错误"

info ">>> 8. 分页功能 <<<"
BODY=$(curl -s -b $COOKIE $BASE/userlist)
check "$BODY" "首页" "分页:首页按钮"
check "$BODY" "上一页" "分页:上一页按钮"
check "$BODY" "下一页" "分页:下一页按钮"
check "$BODY" "尾页" "分页:尾页按钮"
check "$(curl -s -b $COOKIE '$BASE/userlist?pageNum=2')" "用户管理页面" "分页第2页可访问"

echo ""
echo "=========================================="
echo "  最终测试结果: $PASS 通过, $FAIL 失败"
echo "=========================================="
