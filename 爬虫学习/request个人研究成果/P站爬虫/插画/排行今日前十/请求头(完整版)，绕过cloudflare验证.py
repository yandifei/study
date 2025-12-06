
headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-encoding" : "gzip, deflate, br, zstd",    # 加了会乱码
    "accept-encoding" : "gzip, deflate, zstd",
    "accept-language" : "zh-CN,zh;q=0.9",
    "cache-control" : "max-age=0",
    # "cookie" : "",
    # "if-none-match" : "ivlzl36ukd2vyy",

    "priority" : "u=0, i",
    "sec-ch-ua" : '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile" : "?0",
    "sec-ch-ua-platform" : '"Windows"',
    "sec-fetch-dest" : "document",
    "sec-fetch-mode" : "navigate",
    "sec-fetch-site" : "same-origin",
    "sec-fetch-user" : "?1",
    "upgrade-insecure-requests" : "1",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net"
}

download_pic_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '',
    'priority': 'u=1, i',
    'purpose': 'prefetch',
    # 'referer': 'https://www.pixiv.net/artworks/138208295',
    'referer': 'https://www.pixiv.net',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    'x-middleware-prefetch': '1',
    'x-nextjs-data': '1',
}