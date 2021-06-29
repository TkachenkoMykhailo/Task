import scrapy
from ..items import GetproxyItem

class PrxspiderSpider(scrapy.Spider):
    name = 'prxSpider'
    allowed_domains = ['proxyhttp.net']
    start_urls = ['https://proxyhttp.net/']


    def parse(self, response):

        def xor_value(arr_xor, list_const):
            res_xor = 0
            for el_xor in arr_xor:
                # constant or number
                if (list_const.get(el_xor) != None):
                    res_xor ^= list_const.get(el_xor)
                else:
                    res_xor ^= int(el_xor)
            return res_xor

        list_const = {}
        table_const = response.xpath("//div[@id='incontent']/script[@type='text/javascript']").get()
        str_const = table_const[table_const.find('A[')+5:table_const.rfind(';')]
        arr_expr_const = str_const.split(';')
        for element_const in arr_expr_const:
            #get left and right sides expression
            one_expr = element_const.split(' = ')
            #get constants value
            list_const[one_expr[0]] = xor_value(one_expr[1].split('^'), list_const)

        ip_selector = response.xpath("//td[@class='t_ip']/text()")
        port_selector = response.xpath("//td[@class='t_port']")
        for counter in range(len(ip_selector)):
            res_ip = ip_selector[counter].get()
            el_str = port_selector[counter].get()
            el_str = el_str[el_str.find('(') + 1:el_str.find(')')]
            res_port = xor_value(el_str.split('^'), list_const)
            yield GetproxyItem(ip_address=res_ip, port=res_port)
