import string
import uuid
import scrapy

from dataExtractionHw5.items import CMCompanyItem


class CMSpyder(scrapy.Spider):
    name = 'CompaniesMarketcap'
    allowed_domains = ['companiesmarketcap.com']
    start_urls = ['https://companiesmarketcap.com/united-kingdom/largest-companies-in-the-uk-by-market-cap/']

    def __init__(self, num_instances=20):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(".//td[contains(@class, 'name-td')]/div[2]/a/@href").extract()
        url = companies_url[0]
        yield response.follow(url, self.parse_company)

    def parse_company(self, response):
        company = CMCompanyItem()

        # id
        fields = {'id': uuid.uuid4().hex}

        # name
        name = response.xpath(".//div[contains(@class, 'company-title-container')]/div[1]/text()").extract_first()
        fields['name'] = string.capwords(name.strip())

        for key in fields:
            company[key] = fields[key]

        return company
