from lxml import etree
import random
import requests  # 请求访问网站
import time
import ua_info

#  国际、军事、科技、经济、教育、体育、娱乐
usl_link = [ "https://world.gmw.cn/node_4661","https://mil.gmw.cn/node_8986",
            "https://tech.gmw.cn/node_9671", "https://economy.gmw.cn/node_8971",
            "https://edu.gmw.cn/node_10602", "https://sports.gmw.cn/node_9641",
             "https://e.gmw.cn/node_110454"]
usl_prev = ["https://world.gmw.cn/","https://mil.gmw.cn/","https://tech.gmw.cn/",
            "https://economy.gmw.cn/","https://edu.gmw.cn/","https://sports.gmw.cn/","https://e.gmw.cn/"]
link_path = ["./a/@href","./a/@href","./span/a/@href","./a/@href","./span/a/@href","./a/@href","./a/@href"]


def get_Data_link(url):
    # 降低访问速度
    time.sleep(random.random())
    rsp = requests.get(url, headers=ua_info.header)
    return rsp


def guangming():
    data = []
    link_list = []
    sec = 0
    for usl in usl_link:
        rsp_link = get_Data_link(usl + ".htm")
        link0, page_flag = (ana_Data_link(rsp_link, sec))
        link_list += link0
        for i in range(2, 200):
            rsp_link = get_Data_link(usl + "_"+i.__str__() + ".htm")
            link1, page_flag = (ana_Data_link(rsp_link,sec))
            link_list += link1
            if page_flag == 0:
                break
        for l in link_list:
            if "http" in l:
                rsp_data = get_Data_link(l)
            else:
                rsp_data = get_Data_link(usl_prev[sec] + l)
            data_one = ana_Data_cont(rsp_data,sec)
            data.append(data_one)
        link_list.clear()
        sec+= 1
    while None in data:
        data.remove(None)
    return data


# 返回页面的link链接-people网国际板块
def ana_Data_link(cont, sec):
    link_list = []
    page = 1
    html = etree.HTML(cont.text)
    # 解析当前页面list
    li = html.xpath("//*[@class='channel-newsGroup']/li")
    for ul in li:
        ti = ul.xpath("./*[@class='channel-newsTime']/text()")[0]
        t_M = ti.split('-')[1]
        t_D = ti.split('-')[2]
        if ua_info.tM in t_M and ua_info.tD in t_D:
            link = ul.xpath(link_path[sec])[0]
            link_list.append(link)
            continue
        if ua_info.tY in t_D:
            page = 0
            break
    return link_list, page


# 解析页面数据
def ana_Data_cont(cont,sec):
    cont.encoding = "utf-8"
    html = etree.HTML(cont.text)
    data_one = {}
    try:
        title = html.xpath("//*[@class='u-title']/text()")[0]
        time_t = html.xpath("//*[@class='m-con-time']/text()")[0]
        content = html.xpath("//*[@class='u-mainText']/p[not(@class)]/text()")
        data_one["title"] = title
        t = time_t[0:10]
        data_one["time"] = t
        con = ''.join(content)
        data_one["content"] = con
        data_one["section"] = sec + 1
        return data_one
    except:
        return None
