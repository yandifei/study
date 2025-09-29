/*综合实战-华为登陆
构建界面思路：
1、排版（分析布局）
2、内容（基础组件）
3、美化（属性方法）
 */

//去华为官网掏的logo
const huaweiLogo: string = "https://res-static.hc-cdn.cn/cloudbu-site/china/zh-cn/hdhomeportal/logonew.png"

//华为官方图标
// https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/

@Entry
@Component
struct Index {
  @State message: string = "雁低飞";
  // 构建 -> 界面
  build() {
    //Column参数传入对象，使用的space是控件(组件)之间的空格
    Column({ space: 15 }) {
      Image(huaweiLogo)
        .width(150)
      TextInput({
        placeholder: "请输入用户名"
      })
      TextInput({
        placeholder: "请输入密码"
      }).type(InputType.Password)
      Button("登陆")
        .width("100%")
      Row({ space: 15}) {
        Text("前往注册")
        Text("忘记密码")
      }
    }
    .width("100%")
    .padding(20) //内边距20（不要让所有组件挤一挤）
  }
}