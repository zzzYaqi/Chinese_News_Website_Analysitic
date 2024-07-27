from lxml import etree
import random
import requests  # 请求访问网站
import time
import ua_info

# 国际 军事 财经 产经 科技 汽车
usl_link = [ "https://www.guancha.cn/GuoJi%C2%B7ZhanLue/list_","https://www.guancha.cn/JunShi/list_",
            "https://www.guancha.cn/CaiJing/list_", "https://www.guancha.cn/ChanJing/list_",
            "https://www.guancha.cn/GongYe%C2%B7KeJi/list_", "https://www.guancha.cn/qiche/list_"]
link_path = ["./a/@href","./a/@href","./span/a/@href","./a/@href","./span/a/@href","./a/@href","./a/@href"]


def get_Data_link(url):
    time.sleep(random.random())  # 降低访问速度
    rsp = requests.get(url, headers=ua_info.header)
    return rsp

def guanchazhe():
    data = []
    link_list = []
    sec = 0
    usl_prev = "https://www.guancha.cn/"
    for usl in usl_link:
        for i in range(1, 150):
            rsp_link = get_Data_link(usl + i.__str__() + ".shtml")
            link1, page_flag = (ana_Data_link(rsp_link,sec))
            link_list += link1
            if page_flag == 0:
                break
        for l in link_list:
            rsp_data = get_Data_link(usl_prev + l)
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
    li = html.xpath("//*[@class='column-list fix']/li")
    for ul in li:
        ti = ul.xpath("./div/span/text()")[0]
        t_M = ti.split('-')[1]
        t_D = ti.split('-')[2]
        t_D = t_D[0:2]
        if ua_info.tM in t_M and ua_info.tD in t_D:
            link = ul.xpath("./h4/a/@href")[0]
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
        title = html.xpath("//*[@class='left left-main']/h3/text()")[0]
        time_t = html.xpath("//*[@class='time fix']/span/text()")[0]
        content = html.xpath("//*[@class='content all-txt']/p[not(@class)]/text()")
        data_one["title"] = title
        time_t = time_t[0:10]
        data_one["time"] = time_t
        con = ''.join(content)
        data_one["content"] = con
        data_one["section"] = sec + 1
        return data_one
    except:
        return None
