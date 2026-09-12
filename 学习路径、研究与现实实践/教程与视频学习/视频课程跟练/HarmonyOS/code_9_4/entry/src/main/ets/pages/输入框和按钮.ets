/*输入框与按钮
需求：实现登录或注册的排版→输入框和按钮组件
输入框
TextInput(参数对象)
  .属性方法()
1.参数对象：placeholder提示文本
2.属性方法：.type(InputType.xxx)设置输入框type类型
type值       解释说明
Normal      基本输入模式，无特殊限制
Password    密码输入模式
按钮
Button("按钮文本")
组件间距
控制组件间的距离，可以给comn设置{space：间隙大小}
 */

@Entry
@Component
struct Index {
  @State message: string = "雁低飞";
  // 构建 -> 界面
  build() {
    //Column参数传入对象，使用的space是控件(组件)之间的空格
    Column({ space: 15}) {
      TextInput({
        placeholder: "请输入用户名" // 占位符(提示用户输入)
      })
      TextInput({
        placeholder: "请输入密码"
      }).type(InputType.Password)
      Button("登陆")
        .width(200) //设置按钮的宽度
    }
  }
}