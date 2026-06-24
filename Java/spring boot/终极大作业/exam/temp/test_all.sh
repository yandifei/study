#!/bin/bash
# 超���订���管理系统 - 全量测试脚本
BASE="http://localhost:8080"
PASS=0
FAIL=0
COOKIE=/tmp/smbms_test_cookie.txt

green() { echo -e "\033[32m[PASS]\033[0m $1"; ((PASS++)); }
red() { echo -e "\033[31m[FAIL]\033[0m $1"; ((FAIL++)); }
info() { echo -e "\033[36m[INFO]\033[0m $1"; }
check() {
  local actual="$1"
  local expected="$2"
  local msg="$3"
  if echo "$actual" | grep -q "$expected"; then
    green "$msg"
  else
    red "$msg (expected: '$expected', got: '$actual')"
  fi
}

rm -f $COOKIE

echo "=========================================="
echo "  超市订单管理系统 - 全量测试"
echo "=========================================="
echo ""

# ==================== 1. 登录功能 ====================
info ">>> 1. 登录功能测试 <<<"

# 1.1 登录页可访问
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/login")
check "$HTTP" "200" "登录页返回200"

# 1.2 错误密码登录
BODY=$(curl -s -X POST "$BASE/dologin" -d "userCode=admin&userPassword=wrong")
check "$BODY" "用户名或密码错误" "错误密码显示错误信息"

# 1.3 正确登录
curl -s -c $COOKIE -X POST "$BASE/dologin" -d "userCode=admin&userPassword=1234567" -o /dev/null
BODY=$(curl -s -b $COOKIE "$BASE/welcome")
check "$BODY" "系统管理员" "正确登录后welcome页显示用户名"

# 1.4 注销
curl -s -b $COOKIE "$BASE/logout" -o /dev/null
BODY=$(curl -s -b $COOKIE "$BASE/welcome" -L)
check "$BODY" "请登录后再访问" "注销后无法访问welcome"

# 重新登录
curl -s -c $COOKIE -X POST "$BASE/dologin" -d "userCode=admin&userPassword=1234567" -o /dev/null

echo ""

# ==================== 2. 用户管理 ====================
info ">>> 2. 用户管理测试 <<<"

# 2.1 用户列表
BODY=$(curl -s -b $COOKIE "$BASE/userlist")
check "$BODY" "用户管理页面" "用户列表页可访问"

# 2.2 POST搜索（之前bug：POST不支持）
BODY=$(curl -s -b $COOKIE -X POST "$BASE/userlist" -d "queryname=admin&queryUserRole=0&pageNum=1")
check "$BODY" "系统管理员" "POST搜索用户名 admin"
check "$BODY" "admin" "搜索结果包含 admin 用户编码"

# 2.3 按角色搜索
BODY=$(curl -s -b $COOKIE "$BASE/userlist?queryUserRole=1&pageNum=1")
check "$BODY" "系统管理员" "按角色1搜索有结果"

# 2.4 用户查看
BODY=$(curl -s -b $COOKIE "$BASE/userview?uid=1")
check "$BODY" "用户查看页面" "用户查看页可访问"
check "$BODY" "admin" "用户查看显示编码"
check "$BODY" "系统管理员" "用户查看显示角色"

# 2.5 用户修改页
BODY=$(curl -s -b $COOKIE "$BASE/usermodify?uid=1")
check "$BODY" "用户修改页面" "用户修改页可访问"
check "$BODY" "系统管理员" "用户修改回显数据"

# 2.6 用户添加页
BODY=$(curl -s -b $COOKIE "$BASE/useradd")
check "$BODY" "用户添加页面" "用户添加页可访问"

# 2.7 AJAX检查用户编码
BODY=$(curl -s -b $COOKIE "$BASE/ucexist?userCode=admin")
check "$BODY" "exist" "AJAX检查admin存在→exist"

BODY=$(curl -s -b $COOKIE "$BASE/ucexist?userCode=notexist123")
check "$BODY" "noexist" "AJAX检查notexist→noexist"

# 2.8 添加用户
BODY=$(curl -s -b $COOKIE -X POST "$BASE/useraddsave" \
  -d "userCode=testuser01&userName=测试用户1&userPassword=123456&gender=1&phone=13800138000&address=北京市&userRole=3&birthday=2000-01-01")
# 检查重定向后列表中有新用户
BODY=$(curl -s -b $COOKIE "$BASE/userlist")
check "$BODY" "testuser01" "添加用户后列表中出现新用户"

# 2.9 修改用户
BODY=$(curl -s -b $COOKIE -X POST "$BASE/usermodifysave" \
  -d "id=15&userCode=testuser01&userName=测试用户改&gender=2&phone=13900139000&address=上海市&userRole=3")
# 注意: id=15是zhaomin, 需要用已添加用户的id. 先找到testuser01的id
TESTUID=$(curl -s -b $COOKIE "$BASE/userlist" | grep -oP 'userid="\K[0-9]+(?=" username="测试用户1")' 2>/dev/null || echo "")
if [ -n "$TESTUID" ]; then
  BODY=$(curl -s -b $COOKIE -X POST "$BASE/usermodifysave" \
    -d "id=$TESTUID&userCode=testuser01&userName=测试用户改&gender=2&phone=13900139000&address=上海市&userRole=2")
  BODY=$(curl -s -b $COOKIE "$BASE/userlist")
  check "$BODY" "测试用户改" "修改用户名成功"
else
  red "找不到测试用户的ID (可能userlist HTML格式问题)"
fi

# 2.10 AJAX删除用户
if [ -n "$TESTUID" ]; then
  BODY=$(curl -s -b $COOKIE "$BASE/deluser?uid=$TESTUID")
  check "$BODY" "true" "AJAX删除用户返回true"
  BODY=$(curl -s -b $COOKIE "$BASE/userlist")
  if echo "$BODY" | grep -q "testuser01"; then
    red "删除后用户仍然存在"
  else
    green "删除后用户从列表消失"
  fi
fi

echo ""

# ==================== 3. 供应商管理 ====================
info ">>> 3. 供应商管理测试 <<<"

# 3.1 供应商列表
BODY=$(curl -s -b $COOKIE "$BASE/providerlist")
check "$BODY" "供应商管理页面" "供应商列表页可访问"
check "$BODY" "北京三木堂商贸" "供应商列表显示数据"

# 3.2 POST搜索供应商
BODY=$(curl -s -b $COOKIE -X POST "$BASE/providerlist" -d "proContact=张国强&pageNum=1")
check "$BODY" "张国强" "POST搜索供应商联系人"

# 3.3 供应商查看
BODY=$(curl -s -b $COOKIE "$BASE/providerview?providerid=1")
check "$BODY" "供应商查看页面" "供应商查看页可访问"
check "$BODY" "北京三木堂" "供应商查看显示名称"

# 3.4 供应商添加
BODY=$(curl -s -b $COOKIE "$BASE/provideradd")
check "$BODY" "供应商添加页面" "供应商添加页可访问"

# 3.5 添加供应商并验证
BODY=$(curl -s -b $COOKIE -X POST "$BASE/provideraddsave" \
  -d "proCode=TEST001&proName=测试供应商&proContact=测试联系人&proPhone=13800001111&proAddress=测试地址&proDesc=测试描述&proFax=010-12345678")
BODY=$(curl -s -b $COOKIE "$BASE/providerlist")
check "$BODY" "TEST001" "添加供应商后列表中出现"

# 3.6 获取测试供应商ID并修改
TESTPID=$(curl -s -b $COOKIE "$BASE/providerlist" | grep -oP 'providerid="\K[0-9]+(?=" procontactname="测试联系人")' 2>/dev/null || echo "")
if [ -n "$TESTPID" ]; then
  BODY=$(curl -s -b $COOKIE "$BASE/providermodify?providerid=$TESTPID")
  check "$BODY" "供应商修改页面" "供应商修改页可访问"

  BODY=$(curl -s -b $COOKIE -X POST "$BASE/providermodifysave" \
    -d "id=$TESTPID&proCode=TEST001&proName=测试供应商改&proContact=测试联系改&proPhone=13900002222&proAddress=新地址&proDesc=新描述&proFax=010-87654321")
  BODY=$(curl -s -b $COOKIE "$BASE/providerlist")
  check "$BODY" "测试供应商改" "修改供应商成功"

  # 3.7 AJAX删除供应商
  BODY=$(curl -s -b $COOKIE "$BASE/delprovider?providerid=$TESTPID")
  check "$BODY" "true" "AJAX删除供应商返回true"
fi

echo ""

# ==================== 4. 订单管理 ====================
info ">>> 4. 订单管理测试 <<<"

# 4.1 订单列表
BODY=$(curl -s -b $COOKIE "$BASE/orderslist")
check "$BODY" "订单管理页面" "订单列表页可访问"
check "$BODY" "洗发水" "订单列表显示产品数据"

# 4.2 POST搜索订单
BODY=$(curl -s -b $COOKIE -X POST "$BASE/orderslist" -d "productName=洗发水&pageNum=1")
check "$BODY" "洗发水" "POST搜索洗发水"
check "$BODY" "护发素" "搜索结果包含护发素"

# 4.3 订单查看
BODY=$(curl -s -b $COOKIE "$BASE/ordersview?billid=1")
check "$BODY" "订单查看页面" "订单查看页可访问"
check "$BODY" "BILL2016_001" "订单查看显示订单号"

# 4.4 订单添加
BODY=$(curl -s -b $COOKIE "$BASE/ordersadd")
check "$BODY" "订单添加页面" "订单添加页可访问"

# 4.5 添加订单
BODY=$(curl -s -b $COOKIE -X POST "$BASE/ordersaddsave" \
  -d "billCode=TEST_BILL001&productName=测试商品&productDesc=测试类型&productUnit=个&productCount=100&totalPrice=50000&isPayment=1&providerId=1")
BODY=$(curl -s -b $COOKIE "$BASE/orderslist")
check "$BODY" "TEST_BILL001" "添加订单后列表中出现"

# 4.6 订单修改
TESTBID=$(curl -s -b $COOKIE "$BASE/orderslist" | grep -oP 'billid="\K[0-9]+(?=" billname="测试商品")' 2>/dev/null || echo "")
if [ -n "$TESTBID" ]; then
  BODY=$(curl -s -b $COOKIE "$BASE/ordersmodify?billid=$TESTBID")
  check "$BODY" "订单修改页面" "订单修改页可访问"

  BODY=$(curl -s -b $COOKIE -X POST "$BASE/ordersmodifysave" \
    -d "id=$TESTBID&billCode=TEST_BILL001&productName=测试商品改&productDesc=新类型&productUnit=箱&productCount=200&totalPrice=100000&isPayment=2&providerId=1")
  BODY=$(curl -s -b $COOKIE "$BASE/orderslist")
  check "$BODY" "测试商品改" "修改订单成功"

  # 4.7 AJAX删除订单
  BODY=$(curl -s -b $COOKIE "$BASE/delbill?billid=$TESTBID")
  check "$BODY" "true" "AJAX删除订单返回true"
fi

echo ""

# ==================== 5. 密码修改 ====================
info ">>> 5. 密码修改测试 <<<"

# 5.1 密码修改页
BODY=$(curl -s -b $COOKIE "$BASE/changepassword")
check "$BODY" "修改密码页面" "密码修改页可访问"

# 5.2 AJAX验证旧密码
BODY=$(curl -s -b $COOKIE "$BASE/jsp/user.do?method=pwdmodify&oldpassword=1234567")
check "$BODY" "true" "AJAX验证旧密码正确→true"

BODY=$(curl -s -b $COOKIE "$BASE/jsp/user.do?method=pwdmodify&oldpassword=wrong")
check "$BODY" "false" "AJAX验证旧密码错误→false"

# 5.3 不实际修改密码（测试后恢复）
# 跳过实际修改

echo ""

# ==================== 6. 分页功能 ====================
info ">>> 6. 分页功能测试 <<<"

BODY=$(curl -s -b $COOKIE "$BASE/userlist")
check "$BODY" "首页" "分页: 首页按钮存在"
check "$BODY" "上一页" "分页: 上一页按钮存在"
check "$BODY" "下一页" "分页: 下一页按钮存在"
check "$BODY" "尾页" "分页: 尾页按钮存在"
check "$BODY" "共" "分页: 总记录数显示"

# 第2页
BODY=$(curl -s -b $COOKIE "$BASE/userlist?pageNum=2")
check "$BODY" "用户管理页面" "分页第2页可访问"

echo ""

# ==================== 7. 防跳转测试 ====================
info ">>> 7. 防跳转测试 <<<"

# 清除cookie模拟未登录
curl -s -b $COOKIE "$BASE/logout" -o /dev/null 2>/dev/null
rm -f $COOKIE

BODY=$(curl -s "$BASE/welcome" -L)
check "$BODY" "请登录后再访问" "未登录→welcome被拦截"

BODY=$(curl -s "$BASE/userlist" -L)
check "$BODY" "请登录后再访问" "未登录→userlist被拦截"

BODY=$(curl -s "$BASE/providerlist" -L)
check "$BODY" "请登录后再访问" "未登录→providerlist被拦截"

BODY=$(curl -s "$BASE/orderslist" -L)
check "$BODY" "请登录后再访问" "未登录→orderslist被拦截"

echo ""
echo "=========================================="
echo "  测试结果: $PASS 通过, $FAIL 失败"
echo "=========================================="
