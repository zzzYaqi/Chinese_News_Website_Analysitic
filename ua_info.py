import time

newsid = 0

sec = 0

header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "wdcid=3daf0b5a407196d9; sso_c=0; sfr=1; _ma_tk=9yx2myxnb122d0w19qp0q4ouwhrn3udb; _ma_starttm=1647420981468; _ma_is_new_u=0; wdses=2e5141eda93bb48f; wdlast=1648011286",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36"
    }
header2 = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"newsList=c__ps_50_tl__tp__ar_60_ah_false; newsListHelp=0; UOR=,tech.sina.com.cn,; ULV=1648893271367:1:1:1::; SINAGLOBAL=111.197.255.24_1648893303.399064; Apache=111.197.255.24_1648893303.399065",
"Host":"tech.sina.com.cn",
"If-None-Match":'"5c3dbf1e-1e8f"V=5965C31',
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"cross-site",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}