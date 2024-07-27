from lxml import etree
import random
import requests  # 请求访问网站
import time
import ua_info

# 时事 思想 生活 财经
usl_link = ['https://www.thepaper.cn/channel_25950', 'https://www.thepaper.cn/channel_25951',
            'https://www.thepaper.cn/channel_25952', 'https://www.thepaper.cn/channel_25953']
usl1 = "https://www.thepaper.cn/load_index.jsp?nodeids="
usl2 = [
    '25462,25488,97924,25489,25490,25423,25426,25424,25463,25491,25428,68750,27604,25464,25425,25429,25481,25430,25678,25427,25422,25487,25634,25635,25600,&channelID=25950&topCids=,17373686,17379748,17378335,17376231,17378131,17378162,17377949,17378348,17379639&pageidx=',
    '25434,25436,25433,25438,25435,25437,27234,25485,25432,37978,&channelID=25951&topCids=,17346486,17226047,17341783,17346320&pageidx=',
    '25444,27224,26525,26878,25483,25457,25574,25455,26937,25450,25482,25445,25456,26915,25446,25536,26506,97313,103076,&channelID=25952&topCids=,17052254&pageidx=',
    '25448,26609,25942,26015,25599,25842,80623,26862,25769,25990,26173,26202,26404,26490,115327,&channelID=25953&topCids=,17337969,17337534,17338021&pageidx=']
usl3 = '&lastTime=1650682203851'
usl_prev = "https://www.thepaper.cn/"


def get_Data_link(url):
    time.sleep(random.random())
    rsp = requests.get(url, headers=ua_info.header)
    return rsp


def pengpai():
    data = []
    link_list = []
    sec = 0
    for usl in usl_link:
        rsp_link = get_Data_link(usl)
        link0, page_flag = (ana_Data_link(rsp_link, sec))
        link_list += link0
        for i in range(2, 200):
            try:
                rsp_link = get_Data_link(usl1 + usl2[sec] + i.__str__() + usl3)
                link1, page_flag = (ana_Data_link(rsp_link, sec))
                link_list += link1
                if page_flag == 1:
                    break
            except:
                continue
        for l in link_list:
            try:
                rsp_data = get_Data_link(usl_prev + l)
                data_one = ana_Data_cont(rsp_data, sec)
                data.append(data_one)
            except:
                continue
        link_list.clear()
        sec += 1
    while None in data:
        data.remove(None)
    return data


# 返回页面的link链接-people网国际板块
def ana_Data_link(cont, sec):
    # t = time.strftime("%Y-%m-%d", time.localtime())
    cont.encoding = "utf-8"
    link_list = []
    page = 0
    recom_flag = 0
    html = etree.HTML(cont.text)
    # 解析当前页面list
    try:
        li = html.xpath("//*[@class = 'news_li' and starts-with(@id,'cont')]")
        for ul in li:
            ti = ul.xpath("./*[@class = 'pdtt_trbs']/span[not(@class)]/text()")[0]
            if recom_flag == 0:
                recom = ul.xpath("./*[@class = 'pdtt_trbs']/*[@class = 'trbstxt']/text()")
                if recom:
                    continue
            recom_flag = 1
            # if "小时" in ti or "分钟" in ti:
            if "小时" in ti or "分钟" in ti and "天" not in ti:
            # if "3天前" in ti:
                link = ul.xpath("./h2/a/@href")[0]
                link_list.append(link)
                continue
            if "1天前" in ti:
                page = 1
                break
            else:
                continue
    except:
        return None
    return link_list, page


# 解析页面数据
def ana_Data_cont(cont, sec):
    cont.encoding = "utf-8"
    html = etree.HTML(cont.text)
    data_one = {}
    try:
        time_t = str(html.xpath("//*[@class='news_about']/p[2]/text()")[0])
        t_M = time_t.split('-')[1]
        t_D = time_t.split('-')[2]
        if ua_info.tM in t_M and ua_info.tD in t_D:
            title = html.xpath("//*[@class='news_title']/text()")[0]
            content = html.xpath("//*[@class='news_txt']/text()")
            time_t = time_t.replace(" ", '')
            time_t = time_t.replace("\n", '')
            time_t = time_t[0:10]
            data_one["title"] = title
            data_one["time"] = time_t
            con = ''.join(content)
            con = con.replace(" ", '')
            data_one["content"] = con
            data_one["section"] = sec + 1
            return data_one
        else:
            return None
    except:
        return None
