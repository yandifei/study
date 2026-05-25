"""qrcode_manager.py
二维码管理器
"""
# 内置库
import io
import socket
import base64
import os
from typing import Optional
# 第三方库
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 尝试连接局域网内可能存在的地址，强制走物理网卡
        # 即使地址不存在，只要路由表正确，getsockname 也能拿到物理 IP
        s.connect(("192.168.1.255", 9))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class QRCodeManager:
    def __init__(self,
                 version: int = 1,
                 error_correction: int = qrcode.constants.ERROR_CORRECT_L,
                 box_size: int = 10,
                 border: int = 4):
        """初始化二维码管理器

        Args:
            version (int): 二维码版本，1-40，版本越高存储信息越多
            error_correction (int): 纠错级别
                ERROR_CORRECT_L: 7%的错误可以被纠正
                ERROR_CORRECT_M: 15%的错误可以被纠正
                ERROR_CORRECT_Q: 25%的错误可以被纠正
                ERROR_CORRECT_H: 30%的错误可以被纠正
            box_size (int): 每个小格子包含的像素数
            border (int): 边框包含的格子数
        """
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border

    def create_qrcode(self, data: str) -> None:
        """创建二维码并输出到控制台

        Args:
            data (str): 需要编码到二维码中的数据
        """
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

    def create_qrcode_image(self,
                           data: str,
                           output_path: Optional[str] = None,
                           fill_color: str = "black",
                           back_color: str = "white") -> Image.Image:
        """创建二维码图像

        Args:
            data (str): 需要编码到二维码中的数据
            output_path (str, optional): 输出文件路径，如果为None则不保存
            fill_color (str): 二维码颜色
            back_color (str): 背景颜色

        Returns:
            PIL.Image.Image: 二维码图像对象
        """
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        if output_path:
            img.save(output_path)
            print(f"二维码已保存到: {output_path}")

        return img

    def create_styled_qrcode(self,
                            data: str,
                            output_path: Optional[str] = None,
                            style: str = "rounded",
                            gradient_style: str = "radial",
                            center_color: str = "#000000",
                            edge_color: str = "#FFFFFF") -> Image.Image:
        """创建带样式的二维码

        Args:
            data (str): 需要编码到二维码中的数据
            output_path (str, optional): 输出文件路径
            style (str): 样式类型，可选 "rounded" (圆角) 或 "gapped" (间隙)
            gradient_style (str): 渐变样式，可选 "radial" (径向) 或 "square" (方形)
            center_color (str): 中心颜色 (16进制)
            edge_color (str): 边缘颜色 (16进制)

        Returns:
            PIL.Image.Image: 二维码图像对象
        """
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )
        qr.add_data(data)
        qr.make(fit=True)

        # 选择模块绘制器
        if style == "rounded":
            module_drawer = RoundedModuleDrawer()
        else:  # "gapped"
            module_drawer = GappedSquareModuleDrawer()

        # 选择颜色遮罩
        if gradient_style == "radial":
            color_mask = RadialGradiantColorMask(
                center_color=center_color,
                edge_color=edge_color
            )
        else:  # "square"
            color_mask = SquareGradiantColorMask(
                center_color=center_color,
                edge_color=edge_color
            )

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )

        if output_path:
            img.save(output_path)
            print(f"样式二维码已保存到: {output_path}")

        return img

    def create_logo_qrcode(self,
                          data: str,
                          logo_path: str,
                          output_path: Optional[str] = None,
                          logo_size_ratio: float = 0.2) -> Image.Image:
        """创建带Logo的二维码

        Args:
            data (str): 需要编码到二维码中的数据
            logo_path (str): Logo图片路径
            output_path (str, optional): 输出文件路径
            logo_size_ratio (float): Logo相对于二维码的大小比例 (0-1)

        Returns:
            PIL.Image.Image: 二维码图像对象
        """
        # 创建基本二维码
        qr_img = self.create_qrcode_image(data)

        # 打开并调整Logo大小
        logo = Image.open(logo_path)
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * logo_size_ratio)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # 将Logo粘贴到二维码中心
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, logo_pos, mask=logo if logo.mode == 'RGBA' else None)

        if output_path:
            qr_img.save(output_path)
            print(f"带Logo二维码已保存到: {output_path}")

        return qr_img

    def create_qrcode_with_text(self,
                               data: str,
                               text: str,
                               output_path: Optional[str] = None,
                               text_position: str = "bottom",
                               text_color: str = "black",
                               font_size: int = 20) -> Image.Image:
        """创建带文本描述的二维码

        Args:
            data (str): 需要编码到二维码中的数据
            text (str): 要添加的文本
            output_path (str, optional): 输出文件路径
            text_position (str): 文本位置，"top" 或 "bottom"
            text_color (str): 文本颜色
            font_size (int): 字体大小

        Returns:
            PIL.Image.Image: 二维码图像对象
        """
        # 创建基本二维码
        qr_img = self.create_qrcode_image(data)
        qr_width, qr_height = qr_img.size

        # 计算画布大小
        padding = 20
        text_height = font_size + 20

        if text_position in ["top", "bottom"]:
            canvas_height = qr_height + text_height + padding
            canvas_width = qr_width
            canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

            # 计算文本和二维码位置
            if text_position == "top":
                text_y = padding // 2
                qr_y = text_height + padding
            else:  # bottom
                qr_y = padding // 2
                text_y = qr_height + padding

            # 粘贴二维码
            canvas.paste(qr_img, (0, qr_y))
        else:
            raise ValueError("text_position 必须是 'top' 或 'bottom'")

        # 添加文本
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # 计算文本宽度并居中
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (canvas_width - text_width) // 2

        draw.text((text_x, text_y), text, fill=text_color, font=font)

        if output_path:
            canvas.save(output_path)
            print(f"带文本二维码已保存到: {output_path}")

        return canvas

    def get_qrcode_base64(self, data: str, format: str = "PNG") -> str:
        """获取二维码的Base64编码字符串

        Args:
            data (str): 需要编码到二维码中的数据
            format (str): 图像格式，如 "PNG", "JPEG"

        Returns:
            str: Base64编码的二维码图像
        """
        qr_img = self.create_qrcode_image(data)

        # 将图像转换为字节流
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format=format)
        img_byte_arr.seek(0)

        # 转换为Base64
        base64_str = base64.b64encode(img_byte_arr.read()).decode('utf-8')
        return f"data:image/{format.lower()};base64,{base64_str}"

    def batch_create_qrcodes(self,
                            data_list: list,
                            output_dir: str,
                            prefix: str = "qrcode") -> list:
        """批量创建二维码

        Args:
            data_list (list): 数据列表
            output_dir (str): 输出目录
            prefix (str): 文件名前缀

        Returns:
            list: 生成的文件路径列表
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_paths = []

        for i, data in enumerate(data_list):
            output_path = os.path.join(output_dir, f"{prefix}_{i+1:03d}.png")
            self.create_qrcode_image(data, output_path)
            file_paths.append(output_path)

        print(f"批量生成完成，共生成 {len(file_paths)} 个二维码")
        return file_paths

    def analyze_qrcode_capacity(self, data: str) -> dict:
        """分析二维码数据容量

        Args:
            data (str): 要分析的数据

        Returns:
            dict: 容量分析结果
        """
        data_length = len(data.encode('utf-8'))

        # 不同纠错级别的数据容量 (版本1)
        capacities = {
            'L': 152,  # 低纠错
            'M': 128,  # 中纠错
            'Q': 104,  # 四分纠错
            'H': 72    # 高纠错
        }

        error_level_map = {
            qrcode.constants.ERROR_CORRECT_L: 'L',
            qrcode.constants.ERROR_CORRECT_M: 'M',
            qrcode.constants.ERROR_CORRECT_Q: 'Q',
            qrcode.constants.ERROR_CORRECT_H: 'H'
        }

        current_level = error_level_map.get(self.error_correction, 'L')
        current_capacity = capacities[current_level]

        # 计算所需的最小版本
        required_version = 1
        for version in range(1, 41):
            # 简单估算，实际容量更复杂
            estimated_capacity = capacities[current_level] * version
            if data_length <= estimated_capacity:
                required_version = version
                break

        return {
            'data_length': data_length,
            'current_error_correction': current_level,
            'current_capacity': current_capacity,
            'required_minimum_version': required_version,
            'is_within_capacity': data_length <= current_capacity * self.version
        }


# 使用示例
if __name__ == "__main__":
    # 创建二维码管理器实例
    manager = QRCodeManager(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4
    )

    # 示例数据
    test_data = "https://github.com/yourusername/yourproject"

    # 1. 创建基本二维码
    print("1. 创建基本二维码:")
    manager.create_qrcode(test_data)

    # 2. 保存为图片文件
    print("\n2. 保存为图片文件:")
    manager.create_qrcode_image(test_data, "basic_qrcode.png")

    # 3. 创建带样式的二维码
    print("\n3. 创建带样式的二维码:")
    manager.create_styled_qrcode(
        test_data,
        "styled_qrcode.png",
        style="rounded",
        gradient_style="radial",
        center_color="#FF0000",
        edge_color="#0000FF"
    )

    # 4. 获取Base64编码
    print("\n4. 获取Base64编码:")
    base64_str = manager.get_qrcode_base64(test_data)
    print(f"Base64 长度: {len(base64_str)} 字符")

    # 5. 分析容量
    print("\n5. 分析二维码容量:")
    analysis = manager.analyze_qrcode_capacity(test_data)
    for key, value in analysis.items():
        print(f"{key}: {value}")

    # 6. 批量生成示例
    print("\n6. 批量生成示例:")
    test_data_list = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    manager.batch_create_qrcodes(test_data_list, "batch_qrcodes", "test")

    print("\n所有操作完成！")