import string
import uuid
import scrapy
import re

from dataExtractionHw5.items import DisfoldCompanyItem


class DisfoldSpyder(scrapy.Spider):
    name = 'disfold'
    allowed_domains = ['disfold.com']
    start_urls = ['https://disfold.com/world/companies/']
    fields_to_extract = ['Official Name:', 'Employees:', 'Headquarters:', 'CEO:', 'Founded:']
    fields_dictionary = {'Official Name:': 'official_name', 'Employees:': 'employees', 'CEO:': 'ceo',
                         'Founded:': 'founded'}

    def __init__(self, num_instances=1100):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(
            ".//table[contains(@class, 'striped responsive-table')]/tbody/tr/td[2]/a/@href").extract()
        for url in companies_url:
            if self.num_instances <= 0:
                return
            self.num_instances -= 1
            yield response.follow(url, self.parse_company)
        # make request for next page
        next_page = response.xpath(".//i[contains(text(), 'chevron_right')]/parent::a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        company = DisfoldCompanyItem()
        # Id
        fields = {'id': uuid.uuid4().hex}
        # name
        name = response.xpath(".//div[contains(@class, 'card-content cyan darken-4')]/h1/text()").extract_first()
        fields['name'] = string.capwords(name.strip())
        # CARD COMPANY
        card_company = response.xpath(".//div[contains(@class, 'company')]/div[1]/div[2]/div/div/p/text()").extract()
        for row in card_company:
            for label in self.fields_to_extract:
                ss = str(row)
                if ss.find(str(label)) != -1:
                    if label == 'Headquarters:':
                        country_continent = row[14:].split(',')
                        fields['headquarters_country'] = str(re.sub(r'\s+', '', country_continent[0]))
                        fields['headquarters_continent'] = str(re.sub(r'\s+', '', country_continent[1]))
                    else:
                        fields[str(self.fields_dictionary[label])] = row[len(label) + 1:]
        # CARD MARKET CAP
        market_cap = response.xpath(".//p[contains(@class, 'mcap')]/text()").extract_first()
        fields['market_cap'] = str(market_cap).strip()
        card_market_cap = \
            response.xpath(".//div[contains(@class, 'card-content green darken-3 white-text')]/p/text()").extract()
        for row in card_market_cap:
            if row.find('US$') != -1:
                fields['gbp'] = row.strip()[2:]
        # Categories
        categories = response.xpath(
            "//div[contains(@class, 'comp-categs')]/div[contains(@class, 'card-content')]/a/text()[2]").extract()
        fields['categories'] = []
        for category in categories:
            fields['categories'].append(re.sub(r'\s+', '', category))

        for key in fields:
            if not isinstance(fields[key], list):
                company[key] = fields[key].encode('ascii', 'ignore').decode('utf-8')
            else:
                company[key] = fields[key]

        return company
