from multiprocessing import Pool
import random
import requests
import time, datetime
from pyquery import PyQuery
import os, csv, json
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException
from selenium.webdriver import ActionChains
from urllib import parse
from model import create_all
import math, re

url = 'www.qichacha.com'
headers = {
    "Connection": "keep-alive",
    "Host": "www.qichacha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

storage_ship = [
    "TYCID=2a0403d0d78111e99804e59d2a3844cf; undefined=2a0403d0d78111e99804e59d2a3844cf; ssuid=8056998828; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568528539; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568530369; _ga=GA1.2.1465036504.1568528539; _gid=GA1.2.1393168162.1568528539; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522zzas%2522%252C%2522integrity%2522%253A%252214%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODUyODU2OCwiZXhwIjoxNjAwMDY0NTY4fQ.2zpz1j7AyKVSnXe-TYYTG4vmNKnr22ylrWEHtlCGWghKwPtzKmb4EABlZnai4O97irDRl0CHsBhnXp4B3kAZRA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213502571647%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODUyODU2OCwiZXhwIjoxNjAwMDY0NTY4fQ.2zpz1j7AyKVSnXe-TYYTG4vmNKnr22ylrWEHtlCGWghKwPtzKmb4EABlZnai4O97irDRl0CHsBhnXp4B3kAZRA; RTYCID=3c1c0812ef8a4e1a9b26305e2bd4b90f; CT_TYCID=3cbc15c5ac9c4ca586da27c93ae78b05; cloud_token=146edfd12b6846ebb869228727e8a116; _gat_gtag_UA_123487620_1=1"]
# cookie = "jsid=SEM-BAIDU-PZ1907-SY-000100; TYCID=7c336120d63a11e98afab7d0efc933dc; undefined=7c336120d63a11e98afab7d0efc933dc; ssuid=5047837311; _ga=GA1.2.1112942777.1568388228; _gid=GA1.2.1772276711.1568388228; RTYCID=3458f9f2865e46d7965c1735566be63d; CT_TYCID=e3d02897d29f4c40b30606019bc854e0; aliyungf_tc=AQAAAPZK/hcAcwcAEMEhO3NnHow+WPEB; csrfToken=n1vX-rtUEHYfU6x1531uR2f_; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%25B3%2595%25E7%25B1%25B3%25E5%2585%258B%25C2%25B7%25E8%25A9%25B9%25E6%25A3%25AE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODM5MzE1MSwiZXhwIjoxNTk5OTI5MTUxfQ.CtGIrRcSTJfw18XehIDC_BrubHcbhEQRfuLs5_x3u86kjRC0MJucGi5Wj2TPg4yX-oydZzQb3_pFn89eyfAMfw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213059551109%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODM5MzE1MSwiZXhwIjoxNTk5OTI5MTUxfQ.CtGIrRcSTJfw18XehIDC_BrubHcbhEQRfuLs5_x3u86kjRC0MJucGi5Wj2TPg4yX-oydZzQb3_pFn89eyfAMfw; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568388228,1568393135,1568423352,1568511245; cloud_token=26f67e422ed84c49966a5e1946701f1c; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568511303; bannerFlag=true"
cookie = "QCCSESSID=csb0md62ha6vhiim8l4c390q04; UM_distinctid=16d1fb70247240-08b2c06aeb5191-7373e61-2a3000-16d1fb702488d3; _uab_collina=156819515061093531026689; acw_tc=b7f0d81615681951514382151eecbb97cf3adfd30dfb42bdfdf6ba931e; zg_did=%7B%22did%22%3A%20%2216d1fb703a334a-010890d039fa5e-7373e61-2a3000-16d1fb703a470e%22%7D; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568629280,1568630152,1568683106,1568704617; CNZZDATA1254842228=1401409538-1568191378-https%253A%252F%252Fsp0.baidu.com%252F%7C1568704664; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201568704616720%2C%22updated%22%3A%201568705427453%2C%22info%22%3A%201568195150763%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22sp0.baidu.com%22%2C%22cuid%22%3A%20%22a240b361c35797710baddf45be188ad5%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1568705427"

storage_ship.append(cookie)


class DatabaseOperation:

    def connect(self):
        pass

    def create(self):
        pass

    def update(self):
        pass


def fetch_data(url, header) -> str or None:
    res = requests.get(url, headers=header)

    if res.status_code in (200, 201):
        text = res.text
        file = open(time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()
        print('success')
    else:
        print('fail')
        text = None
    return text


def xiechen(html: str):
    jq = PyQuery(html)
    hotel_list = jq("#hotel_list").children()
    total_num = jq('#txtpage').attr('data-pagecount')
    print(total_num)
    for k, i in enumerate(hotel_list):
        print(i)


def find_html() -> list:
    file = open('test.txt', 'r', encoding='utf-8')

    read = file.read()

    file.close()

    jq = PyQuery(read)

    sv_search_container = jq("div.header-block-container .sv-search-container")

    all_element = sv_search_container.children()

    stogre_list: list = []

    for k, element in enumerate(all_element.items()):
        content_div = element.find('.content')
        header_div = content_div.find('.header')
        company_name = header_div.find('a').text()
        status_quo = header_div.find('div').text()
        info_row = content_div.find('.info.row.text-ellipsis').children()
        legal_representative = info_row.eq(0).find('a').text()
        registered_capital = info_row.eq(1).find('span').text()
        date_of_establishment = info_row.eq(2).find('span').text()
        contact_info = content_div.find('.contact.row')

        phone, email = ('', '')
        if contact_info:
            str_list = contact_info.children()
            try:
                for key, j in enumerate(str_list.items()):
                    script = j.find('script').text()
                    # common_list = eval(script)
                    if script:
                        script = eval(script)
                        script = ','.join(script)
                    if key > 0:
                        email = script
                        # email = ','.join(common_list)
                    else:
                        phone = script
                        # phone = ','.join(common_list)
            except Exception as e:
                print(e)

        match_address_info = content_div.find('.match.row.text-ellipsis').children()
        register_address = ''
        if match_address_info:
            register_address = match_address_info.eq(2).text()
        stogre_list.append({
            "company_name": company_name,
            "status_quo": status_quo,
            "legal_representative": legal_representative,
            "registered_capital": registered_capital,
            "date_of_establishment": date_of_establishment,
            "phone": phone,
            "email": email,
            "register_address": register_address
        })
    return stogre_list


def parse_html(html: str = '', keyword: str = ''):
    if not html:
        with open('test1.txt', 'r', encoding='utf-8') as f:
            html = f.read()
    jq = PyQuery(html)
    company_name, phone, status_quo, legal_representative, registered_capital, register_address, email, date_of_establishment = (
                                                                                                                                    '',) * 8
    fetch_result_search = "https://www.qichacha.com/search_index"
    define_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.qichacha.com",
        "X-Requested-With": "XMLHttpRequest"
    }
    request_param = {
        "key": keyword,  # 搜索关键字
        "ajaxflag": 1,  # 未知含义
        "p": 1,  # 请求页码
    }
    data: list = []
    tr: list = []
    search_result = jq("#search-result")
    if search_result:
        ul_tag = jq("ul.pagination.pagination-md").children()
        tr_tag = search_result.children()
        tr.append(tr_tag)
        if ul_tag:
            len_val = ul_tag.__len__()
            if len_val > 7:
                last_two = ul_tag.eq(-2)
                fetch_last_content = last_two.find('a').text()
                total_page_num = re.search(r"\d+", fetch_last_content).group()  # 总页码
            else:
                total_page_num = len_val

            for i in range(total_page_num):
                page_num = i + 1
                request_param['p'] = page_num
                result_request = requests.get(fetch_result_search, params=request_param, timeout=5,
                                              headers=define_headers)
                time.sleep(round(random.uniform(1, 6), 2))
                request_param['p'] = 1
                if result_request.status_code in (200, 201):
                    text = PyQuery(result_request.text())
                    tr_all = text("#search-result").children()
                    tr.append(tr_all)

        for i in tr:
            for j in i.items():
                data.append(qichacha_search_result(j))

        with open('qichacha.txt', 'w') as f:
            f.write(json.dumps(data))
        print('success')
    else:
        alert = jq("div.noresult.no-search").text().split('-')
        print(alert)


def qichacha_search_result(j: PyQuery) -> dict:
    j = j.children()
    td_row = j.eq(2)
    company_name = td_row.children('a').text()
    p_first = td_row.children('p').eq(0)
    legal_representative = p_first.children('a').text()
    span_m_l = p_first("span:first").text().split('：')
    registered_capital = span_m_l[-1].strip('-')
    span_m_ls = p_first('span:last').text().split('：')
    date_of_establishment = span_m_ls[-1]
    p_two = td_row('p').eq(-3)
    p_obj = p_two.clone()
    p_obj.children().remove()
    email = p_obj.text().split('：')[-1].strip('-')
    phone = p_two.find('span').text().split('：')[-1].strip(' ').strip('-')
    register_address = td_row.find('p').eq(2).text().split('：')[-1]
    return dict(
        company_name=company_name, legal_representative=legal_representative, registered_capital=registered_capital,
        date_of_establishment=date_of_establishment, email=email, phone=phone, register_address=register_address
    )


def cookie_pools() -> list:
    global headers
    cookies = []
    headers[
        'Cookie'] = "QCCSESSID=csb0md62ha6vhiim8l4c390q04; UM_distinctid=16d1fb70247240-08b2c06aeb5191-7373e61-2a3000-16d1fb702488d3; _uab_collina=156819515061093531026689; acw_tc=b7f0d81615681951514382151eecbb97cf3adfd30dfb42bdfdf6ba931e; zg_did=%7B%22did%22%3A%20%2216d1fb703a334a-010890d039fa5e-7373e61-2a3000-16d1fb703a470e%22%7D; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568683106,1568704617,1568776151,1568790492; CNZZDATA1254842228=1401409538-1568191378-https%253A%252F%252Fsp0.baidu.com%252F%7C1568796478; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201568793269562%2C%22updated%22%3A%201568797118332%2C%22info%22%3A%201568195150763%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22a240b361c35797710baddf45be188ad5%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1568797118"
    headers[
        'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    cookies.append(headers)
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers[
        'Cookie'] = "QCCSESSID=4ntaav4ld45ba7n41p883i60s4; UM_distinctid=16d1fce710129b-03f99ca449408a-4c312373-2a3000-16d1fce71022ea; CNZZDATA1254842228=1899939659-1568191378-https%253A%252F%252Fsp0.baidu.com%252F%7C1568796478; zg_did=%7B%22did%22%3A%20%2216d1fce71461b8-0d12045cb17be4-4c312373-2a3000-16d1fce7147440%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201568797314212%2C%22updated%22%3A%201568797314217%2C%22info%22%3A%201568196686156%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%222548f9ef0f2d55f89c36b786bb37af80%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568196686,1568797314; _uab_collina=156819668675323725971416; acw_tc=b7f0d83715681966876446230e9b7dc05aea2176296c3d86eb375e30b7; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1568797314; hasShow=1"
    cookies.append(headers)
    return cookies


"""
携程 数据分析
"""


def request_info(url, header):
    data = dict(__VIEWSTATEGENERATOR="DB1FBB6D", cityName="%25E5%25B9%25BF%25E5%25B7%259E", StartTime="2019-09-17",
                DepTime="2019-09-18", RoomGuestCount="1%2C1%2C0", txtkeyword="", Resource="", Room="", Paymentterm="",
                BRev="", Minstate="", PromoteType="", PromoteDate="", operationtype="NEWHOTELORDER",
                PromoteStartDate="", PromoteEndDate="", OrderID="", RoomNum="", IsOnlyAirHotel="F", cityId="32",
                cityPY="guangzhou", cityCode="020", cityLat="23.143407", cityLng="113.331577", positionArea="",
                positionId="", hotelposition="", keyword="", hotelId="", htlPageView="0", hotelType="F",
                hasPKGHotel="F", requestTravelMoney="F", isusergiftcard="F", useFG="F", HotelEquipment="",
                priceRange="-2", hotelBrandId="", promotion="F", prepay="F", IsCanReserve="F", OrderBy="99",
                OrderType="", k1="", k2="", CorpPayType="", viewType="", checkIn="2019-09-18", checkOut="2019-09-19",
                DealSale="", ulogin="", hidTestLat="0%257C0",
                AllHotelIds="30006545%252C371132%252C41795425%252C36157197%252C31319111%252C15735567%252C6547745%252C9242646%252C40249873%252C23154067%252C471422%252C449125%252C1691740%252C28671205%252C932263%252C23763896%252C6994649%252C1431478%252C21133978%252C23806577%252C457918%252C35958899%252C19846595%252C6449516%252C21160909",
                psid="", isfromlist="T", ubt_price_key="htl_search_result_promotion", showwindow="", defaultcoupon="",
                isHuaZhu="False", hotelPriceLow="", unBookHotelTraceCode="", showTipFlg="",
                traceAdContextId="H4sIAAAAAAAAAD2OO04DQRBENRIBESImRETII0139WfaKRIiJCAiWXlW65gDcSsO4MQncOAYdmeXtF71q779Pp2vP%252Fk%252BPVwSsVTTYfwaB1KHqvlAe%252FCOVCNiAeIkzGtsAGOJGW6oYSsIoVJ7Xz2orvHc8e6nUiI2T4Vr6XX8kXlr3Z21C4BBilTaLiTQH%252BIwNmX6X3aWBSgodBO5q%252FaHgBIV1D99vBteXj9AEAS70POTTE1xjCm3SVsWBuc4NMo4MLU6Ng1DSW%252FpPX3ezIZfAAY8VkABAAA%253D",
                allianceid="0", sid="0", pyramidHotels="15735567_6%257C471422_11%257C23763896_16%257C457918_21",
                hotelIds="30006545_1_1%2C371132_2_1%2C41795425_3_1%2C36157197_4_1%2C31319111_5_1%2C15735567_6_1%2C6547745_7_1%2C9242646_8_1%2C40249873_9_1%2C23154067_10_1%2C471422_11_1%2C449125_12_1%2C1691740_13_1%2C28671205_14_1%2C932263_15_1%2C23763896_16_1%2C6994649_17_1%2C1431478_18_1%2C21133978_19_1%2C23806577_20_1%2C457918_21_1%2C35958899_22_1%2C19846595_23_1%2C6449516_24_1%2C21160909_25_1",
                markType="0", zone="", location="", type="", brand="", group="", feature="", equip="", bed="",
                breakfast="", other="", star="", sl="", s="", l="", price="", a="0", keywordLat="", keywordLon="",
                contrast="0", PaymentType="", CtripService="", promotionf="", allpoint="", page="3",
                page_id_forlog="102002", contyped="0", productcode="", eleven="")
    now_time = datetime.datetime.now()
    tomorrow = now_time + datetime.timedelta(days=1)
    checkIn = now_time.strftime('%Y-%m-%d')
    checkOut = tomorrow.strftime('%Y-%m-%d')
    data['checkIn'] = checkIn
    data['checkOut'] = checkOut
    res = requests.post(url=url, headers=header, data=data)
    if res.status_code == 200:
        print(res.json())


def fetch_rand_value(storage_list: list = []) -> str:
    ls_len = storage_list.__len__()

    values = random.randint(1, ls_len)

    return storage_list[values - 1]


def xie_chen():
    cookie = "_abtest_userid=ed666efa-17b3-4aae-896e-bc25467f0ea5; _RSG=bKqP4sJxoq7huUCJ1nBzXB; _RDG=28127258e870a22f002801cfa74ad6200c; _RGUID=7d32ed3d-8467-4525-b87d-2f105331ee2b; magicid=vWH5g91Nl2C2L2fya5p4KFd/Xp5jpLxuNC1S2ngL+VvBaLSQv4yIN4/TI76Mhhde; _ga=GA1.2.1554219393.1568712046; _gid=GA1.2.791826445.1568712046; MKT_Pagesource=PC; ASP.NET_SessionId=fcu24qhty4hbbxbqzme23rfr; clientid=51482032410545903758; hoteluuid=mcqFuNgoU9Q1CAT0; _HGUID=W%04SR%05%04S%04MXTVWMTURUM%02XW%04MR%06QPUSSQ%05%05R%02; OID_ForOnlineHotel=1568712040804d221j1568712286979102003; HotelDomesticVisitedHotels1=428208=0,0,3.9,379,/200s080000002zy2o0AD4.jpg,&6509939=0,0,4.5,2390,/20010f0000007e9tz15E4.jpg,; Union=AllianceID=1881&SID=2209&OUID=310396AB5F0D2BDAE6032916085B9E99%7C100.1030.00.000.00; Session=SmartLinkCode=U2209&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; cticket=740586AC780AD71B45CD2D42AF7065951C2F0C0E321AC32DA6B4E423AAA168A6; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj6+wM9x+nQXxD2o8vRhcogr2Ngc689nDxy7UGQjq9t8YjnzYzUCyBKE47IS8PDy7O/2WZdlz6J2b+cMia34+joolVUNKmyBvUsAYZCuNGefKb5neLd2Xu5FPv0AKJJWZzKgopKkR6MkRRhwrVNjX1nFeF2dOp3+3mIwd+srfyrETdAMrXFVZJwpyhhkBtNjRd0g9zrWAIkagN2ADCIcRva5x9N92uDBvNq4QYbcuFUfVvnz+JsNswUC25neVwd4wNbtDHiW53HjE=; DUID=u=2720C02B89FD3237E1789DD4182F42CA&v=0; IsNonUser=F; UUID=7C60D8DAC7594AD183ED6FD0F67C3812; IsPersonalizedLogin=F; hoteluuidkeys=ctzinTKcBen8Eb4WkYzYofYtFEsYBY5kebHEdMjcTWNYlYtsjZ5itQv5nxBYPYOnKkfwNkK3twHYFYckj4drM4wtfjpYaYDSKdDY7XJa1j50yo6eXhYphjPkyZYkYhdvTXv85i0mrtDj8se5SizgY7YsY1YLYp9v5oebtYtPiFXYBY5YLY3Yf0EGLK1QwkXi51RtXjfrOXYXMJFHyqrDdYogW6XvfdxFpeqGYGnx0TxMUYBXihfwghjqoEXAJU9WDsjXrmOJ7Gimowo3vG7RBcjXBYBAjBrgZyXniPqwSqR0OEMgjD9xzAxBXE50EmhEb1W78eq6wXPET1jnkeqdiQkY4Nrfge01eLpx53iSziHhxZhWD7jQGezBws3KNSwAoi10RmTjLdeFUEf9ynAv34ihMEobygQvSBKHsEdsK65wZ5ikfRT3jPrkAY8QJt7yLrdhjM3eX3j4zKADjpzwDtxO6xN0xLTx7mEdXEp5ENqW9PeFAwdGElXjL4e4Gi39YABrd5ELUy5Xv47iB9E7lymgv8tK9LW7dEsOjFsez9xkcjOrgnEZHWgPekDjSfYB3jhoxX0xLHxkQxk8EmAEOdEHbWAzeF0w5LEBUj4HefZiHkYFOrfUehQeOzYDoEdqwFgW8UiLLKlgEo9EHpETaW9ce68w5pEocjpMe50ilqYf8rALen4efnEh0Y4lEhPwFZWOziFYSYFSYpSi3Tik7ihpj1YLYNUYcDwdBEfdjPUyhsjscY97E6YmY5kR63JSfwd6jn6y6GRS1YDTwX7jsXYzFim9YsOwXYlY0kRZLwAQJ9by7QvQZWbQx9likFyB4vmziPHRgDEPqYZhwPkWOY5Y0tRahJdNwQaj6PyS8RM3YaAWA9E94WlQjDXW9p; fcerror=136550417; _zQdjfing=1336fa5fa4cc275ad0d5c086d5c0864ea084186ad91336fa3165bb; __utma=1.1554219393.1568712046.1568715968.1568715968.1; __utmc=1; __utmz=1.1568715968.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=1.1.10.1568715968; HotelCityID=32split%E5%B9%BF%E5%B7%9EsplitGuangzhousplit2019-09-17split2019-09-18split0; _RF1=223.74.69.155; _jzqco=%7C%7C%7C%7C1568712046372%7C1.23373815.1568712046110.1568716287773.1568716370631.1568716287773.1568716370631.undefined.0.0.19.19; __zpspc=9.2.1568715982.1568716370.4%234%7C%7C%7C%7C%7C%23; appFloatCnt=22; _bfi=p1%3D102002%26p2%3D102002%26v1%3D45%26v2%3D44; hotelhst=687119302; _bfa=1.1568712040804.d221j.1.1568712040804.1568712040804.1.46; _bfs=1.46"
    headers['Host'] = 'hotels.ctrip.com'
    headers['Cookie'] = cookie
    headers['origin'] = 'https://hotels.ctrip.com'
    headers['referer'] = 'https://hotels.ctrip.com/hotel/guangzhou32'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-origin'
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['content-length'] = '2266'
    headers['cache-control'] = 'max-age=0'
    intact_url = 'https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
    request_info(intact_url, headers)


def qichacha_auto_search(ks: list = []):
    browse = webdriver.Chrome(options=Options())
    url = 'https://www.qichacha.com/user_login?back=%2F'
    browse.get(url)
    WebDriverWait(browse, 4)
    browse.find_element_by_id('normalLogin').click()
    browse.find_element_by_id('nameNormal').send_keys('15918750018')
    browse.find_element_by_id('pwdNormal').send_keys('a123456789')
    span = browse.find_element_by_id('dom_id_one').find_elements_by_class_name('btn_slide')
    action = ActionChains(browse)
    action.click_and_hold(span[0]).perform()  # perform()用来执行ActionChains中存储的行为 nc_wrapper nc_scale
    action.reset_actions()
    action.move_by_offset(308, 0).perform()  # 移动滑块
    user_login_normal = browse.find_element_by_id('user_login_normal')
    user_login_normal.find_element(By.TAG_NAME, 'button').click()
    cookie_json = browse.get_cookies()
    cookie_json = json.dumps(cookie_json)
    with open('cookie_set.json', 'w') as f:
        f.write(cookie_json)

    time.sleep(3)
    browse.close()


def GBK2312():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


if __name__ == '__main__':
    dis_list = ['公司', '食品', '美妆', '日化', '科技', '商行', '洗护']
    search_default = '东莞'
    combination = [search_default + i for i in dis_list]
    # combination = [parse.quote(search_default + i) for i in dis_list]
    qichacha_auto_search()

    # search_key = combination[0]
    # cookie = "_abtest_userid=ed666efa-17b3-4aae-896e-bc25467f0ea5; _RF1=223.74.69.155; _RSG=bKqP4sJxoq7huUCJ1nBzXB; _RDG=28127258e870a22f002801cfa74ad6200c; _RGUID=7d32ed3d-8467-4525-b87d-2f105331ee2b; magicid=vWH5g91Nl2C2L2fya5p4KFd/Xp5jpLxuNC1S2ngL+VvBaLSQv4yIN4/TI76Mhhde; _ga=GA1.2.1554219393.1568712046; _gid=GA1.2.791826445.1568712046; MKT_Pagesource=PC; ASP.NET_SessionId=fcu24qhty4hbbxbqzme23rfr; clientid=51482032410545903758; hoteluuid=mcqFuNgoU9Q1CAT0; _HGUID=W%04SR%05%04S%04MXTVWMTURUM%02XW%04MR%06QPUSSQ%05%05R%02; OID_ForOnlineHotel=1568712040804d221j1568712286979102003; HotelDomesticVisitedHotels1=428208=0,0,3.9,379,/200s080000002zy2o0AD4.jpg,&6509939=0,0,4.5,2390,/20010f0000007e9tz15E4.jpg,; Union=AllianceID=1881&SID=2209&OUID=310396AB5F0D2BDAE6032916085B9E99%7C100.1030.00.000.00; Session=SmartLinkCode=U2209&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; cticket=740586AC780AD71B45CD2D42AF7065951C2F0C0E321AC32DA6B4E423AAA168A6; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj6+wM9x+nQXxD2o8vRhcogr2Ngc689nDxy7UGQjq9t8YjnzYzUCyBKE47IS8PDy7O/2WZdlz6J2b+cMia34+joolVUNKmyBvUsAYZCuNGefKb5neLd2Xu5FPv0AKJJWZzKgopKkR6MkRRhwrVNjX1nFeF2dOp3+3mIwd+srfyrETdAMrXFVZJwpyhhkBtNjRd0g9zrWAIkagN2ADCIcRva5x9N92uDBvNq4QYbcuFUfVvnz+JsNswUC25neVwd4wNbtDHiW53HjE=; DUID=u=2720C02B89FD3237E1789DD4182F42CA&v=0; IsNonUser=F; UUID=7C60D8DAC7594AD183ED6FD0F67C3812; IsPersonalizedLogin=F; DomesticHotelCityID=undefinedsplitundefinedsplitundefinedsplit2019-9-17split2019-9-18splitundefined; hoteluuidkeys=ctzinTKcBen8Eb4WkYzYofYtFEsYBY5kebHEdMjcTWNYlYtsjZ5itQv5nxBYPYOnKkfwNkK3twHYFYckj4drM4wtfjpYaYDSKdDY7XJa1j50yo6eXhYphjPkyZYkYhdvTXv85i0mrtDj8se5SizgY7YsY1YLYp9v5oebtYtPiFXYBY5YLY3Yf0EGLK1QwkXi51RtXjfrOXYXMJFHyqrDdYogW6XvfdxFpeqGYGnx0TxMUYBXihfwghjqoEXAJU9WDsjXrmOJ7Gimowo3vG7RBcjXBYBAjBrgZyXniPqwSqR0OEMgjD9xzAxBXE50EmhEb1W78eq6wXPET1jnkeqdiQkY4Nrfge01eLpx53iSziHhxZhWD7jQGezBws3KNSwAoi10RmTjLdeFUEf9ynAv34ihMEobygQvSBKHsEdsK65wZ5ikfRT3jPrkAY8QJt7yLrdhjM3eX3j4zKADjpzwDtxO6xN0xLTx7mEdXEp5ENqW9PeFAwdGElXjL4e4Gi39YABrd5ELUy5Xv47iB9E7lymgv8tK9LW7dEsOjFsez9xkcjOrgnEZHWgPekDjSfYB3jhoxX0xLHxkQxk8EmAEOdEHbWAzeF0w5LEBUj4HefZiHkYFOrfUehQeOzYDoEdqwFgW8UiLLKlgEo9EHpETaW9ce68w5pEocjpMe50ilqYf8rALen4efnEh0Y4lEhPwFZWOziFYSYFSYpSi3Tik7ihpj1YLYNUYcDwdBEfdjPUyhsjscY97E6YmY5kR63JSfwd6jn6y6GRS1YDTwX7jsXYzFim9YsOwXYlY0kRZLwAQJ9by7QvQZWbQx9likFyB4vmziPHRgDEPqYZhwPkWOY5Y0tRahJdNwQaj6PyS8RM3YaAWA9E94WlQjDXW9p; fcerror=136550417; _zQdjfing=1336fa5fa4cc275ad0d5c086d5c0864ea084186ad91336fa3165bb; _gat=1; _jzqco=%7C%7C%7C%7C1568712046372%7C1.23373815.1568712046110.1568713671825.1568713706368.1568713671825.1568713706368.undefined.0.0.15.15; __zpspc=9.1.1568712046.1568713706.15%234%7C%7C%7C%7C%7C%23; hotelhst=1001161454; _bfa=1.1568712040804.d221j.1.1568712040804.1568712040804.1.25; _bfs=1.25; appFloatCnt=15; _bfi=p1%3D102002%26p2%3D600001375%26v1%3D25%26v2%3D24"
    # headers['Cookie'] = cookie
    # intact_url = "https://" + url + "/search?key=" + search_key
    # fetch_data(intact_url, headers)
