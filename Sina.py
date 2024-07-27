import json
from lxml import etree
from datetime import datetime
import requests
import random
import time
import ua_info

# 军事 科技 国际 社会 娱乐 体育
mil_link = ["https://mil.news.sina.com.cn/roll/index.d.html?cid=57918&page=",
            "https://mil.news.sina.com.cn/roll/index.d.html?cid=57919&page="]
usl_base = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}"
#各个页面的id
id_list = ["2514","2515","2511","2669","2513","2512"]


def get_Data_link(url):
    # 降低访问速度
    time.sleep(random.random())
    rsp = requests.get(url, headers=ua_info.header)
    return rsp


def sina():
    sec = 0
    data = []
    for id in id_list:
        for p in range(1, 200):
            r = random.random()
            rsp = get_Data_link(usl_base.format(id,p,r))
            data0, page_flag = (ana_Data(rsp,sec))
            data += data0
            if page_flag == 0:  # 不再翻页
                break
        sec += 1
    while None in data:
        data.remove(None)
    return data


# 返回页面的link链接
def ana_Data(cont,sec):
    re = []
    page = 1
    result = json.loads(cont.text)
    data_list = result.get('result').get('data')
    for d in data_list:
        ti = datetime.fromtimestamp(int(d.get('ctime')))
        ti = datetime.strftime(ti, '%Y-%m-%d')
        t_M = ti.split('-')[1]
        t_D = ti.split('-')[2]
        t_D = t_D[0:2]
        if ua_info.tM in t_M and ua_info.tD in t_D:
            li = d.get('wapurl')
            re_one = ana_Data_cont(li,ti,sec)
            re.append(re_one)
        if ua_info.tY in t_D:
            page = 0
            break
    return re, page


def ana_Data_cont(link,ti,sec):
    try:
        re = {}
        rsp = get_Data_link(link)
        rsp.encoding = "utf-8"
        html = etree.HTML(rsp.text)
        title = html.xpath("//h1/text()")[0]
        content = html.xpath("//p/text()")
        con = ''.join(content)
        re["section"] = sec + 1
        re['time'] = ti
        re["title"] = title
        re["content"] = con
        return re
    except:
        return None
