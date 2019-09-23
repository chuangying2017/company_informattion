import requests
import time
import re
from urllib import parse
from pyquery import PyQuery
import random
import json
from multiprocessing import Pool as pool


class Mobile:
    assign_num: int = 10

    request_url: str = ''

    search_url: str = 'https://www.qichacha.com/search'

    search_key: dict = {'key': '', 'ajaxflag': 1, 'p': 1}

    request_header: dict = {
        "Connection": "keep-alive",
        "Host": "www.qichacha.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    def __init__(self):
        pass

    def request(self, keyword: str = ''):
        keyword = parse.quote(keyword)
        res = requests.get(self.search_url, params={'key': keyword})
        print(res.status_code, res.url)
        if res.status_code in (200, 201):
            html = res.text
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
                        data.append(self.parse_html(j))

                with open(time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.json', 'w') as f:
                    f.write(json.dumps(data))
                result = 'success'
            else:
                result = jq("div.noresult.no-search").text().split('-')
            html = result
        else:
            print('获取状态失败')
            html = False

        return html

    def parse_html(self, j: PyQuery) -> dict:
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

    def data_save(self):
        pass

    def num_assign(self, mobile: int = 130):
        ls: list = []
        i = 100000000
        while i > 1:
            i -= 1
            mobiles = str(mobile) + str(i)
            result = self.request(mobiles)
            ls.append(result)
            time.sleep(random.randint(2, 6))
        return ls

    def thread_assign(self):
        mobile = 130
        ls: list = []
        for i in range(10):
            ls.append(mobile+i)
        p = pool(processes=self.assign_num)
        ls1 = p.map(self.num_assign, ls)
        p.close()
        p.join()
        print(ls1)

    def run(self):
        self.thread_assign()


if __name__ == '__main__':
    mobile = Mobile()
    mobile.run()
