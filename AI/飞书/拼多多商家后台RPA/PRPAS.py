"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
import json
import pandas as pd
# 三方库
from playwright.sync_api import sync_playwright
# 自己的模块
from logger import logger_manager, info, critical, warning  # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
"""初始化"""
# 是否为开发模式
debug = False
# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=debug)
info("日志模块加载完成，全局异常捕获开启")
# 层叠覆盖原来的配置
config_manager.config_override()  # 层叠覆盖原来的配置
info("层叠覆盖原来的配置完成")
# 协议
PROTOCOL: str = config_manager.config_data.server.protocol
# 主机号
HOST: str = config_manager.config_data.server.host
# 端口号
PORT: int = config_manager.config_data.server.port
info(f"服务器配置，协议：{PROTOCOL}，主机：{HOST}，端口：{PORT}")

df = pd.read_excel(rf"{get_root()}/data.xlsx", sheet_name=0, dtype=str)
df.columns = df.columns.str.strip()
df["原商品编码"] = df["原商品编码"].dropna().str.strip()
df["商品编码（仓库填）"] = df["商品编码（仓库填）"].fillna('').str.strip()
mapping = dict(zip(df["原商品编码"], df["商品编码（仓库填）"]))

with sync_playwright() as p:
    # 通过 channel 名称连接
    browser = p.chromium.connect_over_cdp("chrome")

    # 或者通过 CDP 端点 URL 连接
    # browser = p.chromium.connect_over_cdp("http://localhost:9222")

    # 工作的目标界面
    target_page = None
    # 获取第一个已打开的浏览器
    context = browser.contexts[0]
    # 遍历该 Context 下的界面
    for page in context.pages:
        if page.title() == "拼多多 商家后台":
            target_page = page
            info(f"定位到界面了：{page.title()}")
            break
    else:
        warning("没有找到界面，回车退出该程序：")
        input()
        exit()


    # # 拿到登陆的cookies
    # cookies = context.cookies()
    # # 保存cookies
    # with open("user_data/cookies.json", "w") as f:
    #     json.dump(cookies, f)

    selector_rule = 'td.sku-input:nth-last-child(2) input[data-testid="beast-core-input-htmlInput"]'
    processed_count = 0  # 已处理的元素个数（不包括最后一个触发滚动的元素）

    while True:
        # 获取当前所有匹配的元素
        all_elements = page.locator(selector_rule).all()
        current_total = len(all_elements)

        # 如果有新增元素（且不止一个，因为至少要留一个触发滚动）
        if current_total > processed_count + 1:  # +1 是因为最后一个要留着触发滚动
            # 只处理新增的部分（从 processed_count 到 current_total-2，即跳过最后一个）
            new_elements = all_elements[processed_count: current_total - 1]
            for elem in new_elements:
                original_value = elem.input_value()
                replace_text = mapping.get(original_value,
                                           f"未找到 {original_value} 该数据，请更新“Excel文件”或手动查找")
                elem.fill(replace_text)
                info(f"{original_value} 替换为了 {replace_text}")
                page.wait_for_timeout(500)
            # 更新已处理计数
            processed_count = current_total - 1  # 因为最后一个还未处理（作为触发点）
        elif current_total == processed_count + 1:
            # 只有最后一个未处理，说明可能已到底，但为了保险，仍然尝试滚动
            pass
        else:
            # 理论上不会出现 current_total < processed_count，但以防万一
            break

        # 滚动最后一个元素（触发懒加载）
        last_elem = all_elements[-1]  # 注意：如果 DOM 更新，这个引用可能失效，但 `all_elements` 是旧列表，最好重新获取
        # 更安全：直接使用选择器重新获取最后一个
        page.locator(selector_rule).last.scroll_into_view_if_needed()
        page.wait_for_timeout(2000)  # 等待新数据加载

        # 检查元素总数是否增加
        new_total = len(page.locator(selector_rule).all())
        if new_total == current_total:
            # 没有新元素加载，说明已经到底，填充最后一个元素（即最后剩下的那个）
            # 此时所有元素都已加载完毕，无需再滚动，填充最后一个
            last_element = page.locator(selector_rule).last
            original_value = last_element.input_value()
            replace_text = mapping.get(original_value, f"未找到 {original_value} 该数据，请更新“Excel文件”或手动查找")
            last_element.fill(replace_text)
            info(f"{original_value} 替换为了 {replace_text}")
            # 退出循环
            break
        # 否则继续循环，处理新加载的元素


    # 循环结束后，所有元素都已经在 DOM 中了。不要担心之前没有的会丢失
    info(f"完成{processed_count}个控件填写")
