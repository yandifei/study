# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from utils.redis.redis_utils import get_signcode, delete_signcode
import logging
from .constants import VerifyFailed,VeriCodeError,VeriCodeTimeOut
logger = logging.getLogger(__name__)


@require_GET
def email_notify_new(request):
    """
    邮箱激活通知视图
    请求示例: /auth/email_notify?email=frn1234@163.com&sign=c114b8a0-d708-11f0-9170-749779ac08b2
    """
    # 获取参数
    email = request.GET.get('email', '').strip()
    sign = request.GET.get('sign', '').strip()

    # 参数验证
    if not email or not sign:
        logger.warning(f"邮箱激活参数缺失: email={email}, sign={sign}")
        return render(request, 'err_new.html', {
            'error_code': 4000,
            'error_msg': '激活链接不完整',
            'redirect_url': '/',
            'redirect_time': 5,
        })

    # 验证邮箱格式
    if '@' not in email or '.' not in email:
        logger.warning(f"邮箱格式错误: {email}")
        return render(request, 'err.html', VeriCodeError)

    # 从Redis获取并验证signcode
    try:
        signcode = get_signcode(sign)
        if not signcode:
            logger.warning(f"验证码不存在或已过期: sign={sign}")
            return render(request, 'err.html', VeriCodeTimeOut)

        # 验证邮箱是否匹配
        if email != signcode:
            logger.warning(f"邮箱验证不匹配: 输入={email}, Redis={signcode}")
            return render(request, 'err.html', VeriCodeError)

    except Exception as e:
        logger.error(f"Redis验证失败: {str(e)}")
        return render(request, 'err.html', {
            'error_code': 5001,
            'error_msg': '系统错误，请稍后重试',
            'redirect_url': '/',
            'redirect_time': 5,
        })

    # 查找并激活用户
    try:
        user = User.objects.get(email=email)

        # 检查用户是否已激活
        if user.is_active:
            logger.info(f"用户已激活，直接登录: {email}")

            # 自动登录
            login(request, user)

            # 获取或创建用户资料
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'email': user.email,
                    'user_src': Profile.NORMAL_USER
                }
            )

            # 设置session
            request.session['uid'] = profile.uid
            request.session['username'] = profile.name

            # 删除已使用的验证码
            delete_signcode(sign)

            return render(request, 'web/index.html', {
                'user_info': profile.data if hasattr(profile, 'data') else {},
                'has_login': True,
                'msg': "欢迎回来！您已登录",
            })

        # 激活新用户
        user.is_active = True
        user.is_staff = True  # 注意：赋予staff权限需谨慎
        user.save()

        logger.info(f"用户激活成功: {email}")

        # 自动登录
        login(request, user)

        # 获取或创建用户资料
        profile, created = Profile.objects.select_for_update().get_or_create(
            user=user,
            defaults={
                'name': user.username,
                'email': user.email,
                'user_src': Profile.NORMAL_USER
            }
        )

        # 如果用户资料已存在，更新必要字段
        if not created:
            profile.name = user.username
            profile.email = user.email
            profile.user_src = Profile.NORMAL_USER
            profile.save()

        # 设置session
        request.session['uid'] = profile.uid
        request.session['username'] = profile.name

        # 设置session过期时间（可选）
        request.session.set_expiry(60 * 60 * 24 * 7)  # 7天

        # 删除已使用的验证码
        delete_signcode(sign)

        # 记录激活成功日志
        logger.info(f"用户激活并登录成功: username={user.username}, email={email}")

        # 渲染成功页面
        return render(request, 'web/index.html', {
            'user_info': profile.data if hasattr(profile, 'data') else {},
            'has_login': True,
            'msg': "激活成功！欢迎使用我们的服务",
            'show_welcome': True,  # 可以用于显示欢迎提示
        })

    except User.DoesNotExist:
        logger.error(f"用户不存在: {email}")

        # 可以选择自动创建用户（根据业务需求）
        # return auto_create_user(request, email, sign)

        return render(request, 'err_new.html', VerifyFailed)

    except Exception as e:
        logger.error(f"用户激活过程出错: {str(e)}")
        return render(request, 'err_new.html', {
            'error_code': 5002,
            'error_msg': '激活过程出错，请稍后重试',
            'redirect_url': '/',
            'redirect_time': 5,
        })