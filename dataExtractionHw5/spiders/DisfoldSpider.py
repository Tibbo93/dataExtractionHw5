import string
import uuid
import scrapy
import re

from dataExtractionHw5.items import DisfoldCompanyItem


class DisfoldSpyder(scrapy.Spider):
    name = 'Disfold'
    allowed_domains = ['disfold.com']
    start_urls = ['https://disfold.com/united-kingdom/companies/']
    fields_to_extract = ['Name', 'Official Name', 'Headquarters Continent', 'Headquarters Country', 'Employees', 'CEO', 'Market Cap',
                         'GBP as of April 1, 2022', 'Categories @@ DA FARE']

    def __init__(self, num_instances=20):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(".//table[contains(@class, 'striped responsive-table')]/tbody/tr/td[2]/a/@href").extract()
        #url = companies_url[0]
        #yield response.follow(url, self.parse_company)
        for url in companies_url:
            if self.num_instances <= 0:
                return
            self.num_instances -= 1
            yield response.follow(url, self.parse_company)
        # yield response.follow(url, self.parse_company)

        # make request for next page
        next_page = response.xpath(".//ul[contains(@class, 'pagination')]/li[2]/a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        company = DisfoldCompanyItem()

        # Id
        fields = {'id': uuid.uuid4().hex}

        # Name
        name = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/h1/text()").extract_first()
        fields['name'] = string.capwords(name.strip())

        # Official Name
        official_name = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/p[2]/text()").extract_first()
        official_name = official_name[15:]
        fields['official_name'] = official_name.strip()

        # Headquarters Continent & Headquarters Country
        headquarters = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/p[3]/text()").extract_first()
        headquarters = headquarters[14:]
        list = headquarters.split(',')
        # headquarters_country = re.sub(r'\s+', '', list[0])
        # headquarters_continent = re.sub(r'\s+', '', list[1])
        fields['headquarters_country'] = re.sub(r'\s+', '', list[0])
        fields['headquarters_continent'] = re.sub(r'\s+', '', list[1])

        # Employees
        employees = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/p[4]/text()").extract_first();
        employees = employees[11:]
        fields['employees'] = employees.strip()

        # Ceo
        ceo = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/p[5]/text()").extract_first()
        ceo = ceo[5:]
        fields['ceo'] = ceo.strip()

        # Market Cap
        market_cap = response.xpath(".//p[contains(@class,'mcap')]/text()").extract_first()
        fields['market_cap'] = market_cap.strip()

        # GBP as of April 1, 2022
        gbp = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[3]/div/div/p[3]/text()").extract_first()
        fields['gbp'] = gbp.strip()[2:]

        for key in fields:
            company[key] = fields[key]

        return company
