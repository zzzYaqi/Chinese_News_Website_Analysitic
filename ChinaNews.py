from lxml import etree
import random
import requests  # 请求访问网站
import time
import ua_info


# "国际", "国内", "财经", "体育", "娱乐", "社会"
def get_Data_link(url):
    # 降低访问速度
    time.sleep(random.random())
    rsp = requests.get(url, headers=ua_info.header)
    return rsp


def chinanews():
    data = []
    usl = "https://www.chinanews.com.cn/scroll-news/news"
    usl_prev = "https://www.chinanews.com.cn/"
    for i in range(1, 200):
        num = 0
        rsp_link = get_Data_link(usl+i.__str__()+".html")
        link_list, sec_list, page_flag = (ana_Data_link(rsp_link))
        for l in link_list:
            rsp_data = get_Data_link(usl_prev + l)
            data_one = ana_Data_cont(rsp_data, sec_list[num] - 1)
            num += 1
            data.append(data_one)
        if page_flag == 0:
            break
    while None in data:
        data.remove(None)
    return data


# 返回页面的link链接-people网国际板块
def ana_Data_link(cont):
    cont.encoding = "utf-8"
    link_list = []
    sec_list = []
    page = 1
    sec = ["国际", "国内", "财经", "体育", "娱乐", "社会"]
    html = etree.HTML(cont.text)
    # 解析当前页面list
    li = html.xpath("//*[@class='content_list']/ul/li")
    for ul in li:
        try:
            ti = ul.xpath("./*[@class='dd_time']/text()")[0]
            ti = str(ti)
            ti = ti.split(' ',1)[0]
            t_M = ti.split('-')[0]
            t_D = ti.split('-')[1]
            if ua_info.tM in t_M and ua_info.tD in t_D:
                s = ul.xpath("./div[1]/a/text()")[0]
                if s in sec:
                    sec_list.append(sec.index(s) + 1)
                    link = ul.xpath("./div[2]/a/@href")[0]
                    link_list.append(link)
        except:
            continue
    return link_list, sec_list, page


# 解析页面数据
def ana_Data_cont(cont, sec):
    cont.encoding = "utf-8"
    html = etree.HTML(cont.text)
    data_one = {}
    try:
        title = html.xpath("//body/div[7]/div[1]/div[2]/h1/text()")[0]
        time_t = html.xpath("//body/div[7]/div[1]/div[2]/div[3]/div/text()")[0]
        content = html.xpath("//*[@class='left_zw']/p/text()")
        t = ''
        data_one["title"] = title
        flag = 0
        for i in time_t:
            if i in '0123456789':
                t += i
                flag += 1
            if flag == 4 or flag == 7:
                t += '/'
                flag += 1
            if flag == 10:
                break
        data_one["time"] = t
        con = ''.join(content)
        data_one["content"] = con
        data_one["section"] = sec + 1
        return data_one
    except:
        return None
