# utils/email_service.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def send_activation_email(user_email, sign=None, username=None):
    """发送激活邮件"""
    try:
        # 确保 email 是字符串
        if not isinstance(user_email, str):
            logger.error(f"邮箱参数类型错误: {type(user_email)}")
            return False

        # 清理邮箱地址
        user_email = user_email.strip()

        # 如果没有提供用户名，尝试从数据库获取
        if not username:
            try:
                user = User.objects.get(email=user_email)
                username = user.username
            except User.DoesNotExist:
                # 如果用户不存在，使用邮箱前缀作为用户名
                username = user_email.split('@')[0]
                logger.warning(f"用户不存在，使用邮箱前缀作为用户名: {user_email}")

        # 生成激活令牌
        activation_token = str(uuid.uuid4())

        # 构建激活链接
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')

        if sign:
            # 使用sign参数的方式
            activation_link = f"{site_url}/auth/email_notify?email={user_email}&sign={sign}"
        else:
            # 使用token的方式
            activation_link = f"{site_url}/auth/activate?email={user_email}&token={activation_token}"

        # 准备邮件内容
        context = {
            'username': username,
            'email': user_email,
            'activation_link': activation_link,
            'site_name': getattr(settings, 'SITE_NAME', 'Quizz.cn'),
            'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@quizz.cn'),
            'current_year': datetime.now().year,
        }

        # 渲染模板
        try:
            html_content = render_to_string('emails/activation.html', context)
            text_content = render_to_string('emails/activation.txt', context)
        except Exception as e:
            logger.error(f"渲染模板失败: {str(e)}")
            # 使用简单模板
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <h1>欢迎加入 {context['site_name']}！</h1>
                <p>请点击链接激活账户：</p>
                <p><a href="{context['activation_link']}">{context['activation_link']}</a></p>
            </body>
            </html>
            """
            text_content = f"请点击链接激活账户：{context['activation_link']}"

        # 创建并发送邮件
        subject = f"激活您的{context['site_name']}账户"

        # 关键修复：确保 to 参数是列表
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],  # ← 必须是列表
        )
        email_msg.attach_alternative(html_content, "text/html")

        email_msg.send()

        logger.info(f"激活邮件发送成功: {user_email}")
        return True

    except Exception as e:
        logger.error(f"发送激活邮件失败: {str(e)}", exc_info=True)
        return False