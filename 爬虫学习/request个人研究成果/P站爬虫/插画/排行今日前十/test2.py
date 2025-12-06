import requests
# 注意：第10行使用了 re 模块，需要在这里导入
import re

url = input('请输入图片链接：')
name = input('请输入图片名称：')
# 'referer': 'https://www.pixiv.net/ranking.php'

headers1={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'cookie': 'first_visit_datetime_pc=2025-11-17%2018%3A37%3A19; p_ab_id=9; p_ab_id_2=6; p_ab_d_id=21178917; yuid_b=OZY2gAg; _ga=GA1.1.15955225.1763372242; _gcl_au=1.1.1695543687.1764916332; device_token=5e82edb2d13c39b7076d7bd783e21c44; c_type=25; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; PHPSESSID=106069815_4dqyRqeltTcqJiApWmfYFGTFVqg7nNrO; _ga_MZ1NL4PHH0=GS2.1.s1764916349$o2$g1$t1764916605$j16$l0$h0; _cfuvid=UA2hfTXdurrPgHCIgcRzkKVbiae5LUhh3ISHONwRIxE-1765005060148-0.0.1.1-604800000; __cf_bm=C829siU368.qaMm4VXvL2ISXGZToNspGHWBGXW.2sIo-1765022034-1.0.1.1-Zb8uqbOerGclVM8fkl6NRBRcL3UMM6CWxgW.ZsEUvfSes04rfRAyT..0SB6GWy1MOPyLhPUFUSS9.U7oPNhgZ0Gmxq9Pkj1R57Oc69_.a2kaOty0Zqsl1dqU8Bos6mc1; cf_clearance=RxMTKqUdNCvNnt2KbKPJhGuGSl3XONxPpP22vbn7zac-1765022457-1.2.1.1-03QhIGYEBjBhSJvJNmM26HpRb4b7Dcczqd0dxAaRtqTzdRuHJTjMX3aubkDTucVhUHWZYZjLF2W7hmmHsb3ayy40Uu70VblnK3NRbYdLtEOhyUvxJr_pCWu90zzXEzZAmliz49lVjHSzotySAOOdwr0U3YXwJnixInpiwS_odmcUkDRO77HNFHqTKDKCrP3ZthFq6O0vB0jfJaE_eb.Dh5OB5dt4_JeZDC_z.9aFBsw; _ga_75BBYNYN9J=GS2.1.s1765022457$o6$g1$t1765022459$j58$l0$h0',
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'
}
headers2={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'first_visit_datetime_pc=2025-11-17%2018%3A37%3A19; p_ab_id=9; p_ab_id_2=6; p_ab_d_id=21178917; yuid_b=OZY2gAg; _ga=GA1.1.15955225.1763372242; _gcl_au=1.1.1695543687.1764916332; device_token=5e82edb2d13c39b7076d7bd783e21c44; c_type=25; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; PHPSESSID=106069815_4dqyRqeltTcqJiApWmfYFGTFVqg7nNrO; _ga_MZ1NL4PHH0=GS2.1.s1764916349$o2$g1$t1764916605$j16$l0$h0; _cfuvid=UA2hfTXdurrPgHCIgcRzkKVbiae5LUhh3ISHONwRIxE-1765005060148-0.0.1.1-604800000; __cf_bm=C829siU368.qaMm4VXvL2ISXGZToNspGHWBGXW.2sIo-1765022034-1.0.1.1-Zb8uqbOerGclVM8fkl6NRBRcL3UMM6CWxgW.ZsEUvfSes04rfRAyT..0SB6GWy1MOPyLhPUFUSS9.U7oPNhgZ0Gmxq9Pkj1R57Oc69_.a2kaOty0Zqsl1dqU8Bos6mc1; cf_clearance=RxMTKqUdNCvNnt2KbKPJhGuGSl3XONxPpP22vbn7zac-1765022457-1.2.1.1-03QhIGYEBjBhSJvJNmM26HpRb4b7Dcczqd0dxAaRtqTzdRuHJTjMX3aubkDTucVhUHWZYZjLF2W7hmmHsb3ayy40Uu70VblnK3NRbYdLtEOhyUvxJr_pCWu90zzXEzZAmliz49lVjHSzotySAOOdwr0U3YXwJnixInpiwS_odmcUkDRO77HNFHqTKDKCrP3ZthFq6O0vB0jfJaE_eb.Dh5OB5dt4_JeZDC_z.9aFBsw; _ga_75BBYNYN9J=GS2.1.s1765022457$o6$g1$t1765022459$j58$l0$h0',
    'referer': 'https://www.pixiv.net/'
}

data = requests.get(url,headers=headers1).text
pixiv_url= re.findall(re.compile('original":"(.+_p0\.jpg)'),data)
DATA = requests.get(pixiv_url[0],headers=headers2).content

with open(f'{name}.jpg','wb') as f:
    f.write(DATA)