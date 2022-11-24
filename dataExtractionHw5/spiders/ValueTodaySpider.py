import uuid
import scrapy
import re

from dataExtractionHw5.items import ValueTodayCompanyItem


class ValueTodaySpider(scrapy.Spider):
    name = 'valueTodaySpider'
    allowed_domains = ['www.value.today']
    base_url = 'https://www.value.today'
    fields_to_extract = \
        ['Headquarters Country', 'Headquarters Sub Region', 'World Rank (Jan-07-2022)', 'Market Value (Jan 1st 2020)',
         'Annual Revenue in USD', 'Annual Net Income in USD', 'Annual Results for Year Ending', 'Total Assets in USD',
         'Total Liabilities in USD', 'Total Equity in USD', 'Headquarters Region / City']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response, **kwargs):
        company_url = response.xpath(".//div[contains(@class, 'field--name-node-title')]/h2/a/@href").extract_first()
        yield scrapy.Request(url=self.base_url + company_url, headers=kwargs.get('headers'),
                             callback=self.parse_company)

    def parse_company(self, response):
        company = ValueTodayCompanyItem()
        fields = {'id': uuid.uuid4().hex}

        name = response.xpath(".//div[contains(@class, 'field--name-node-title')]/h1/a/text()").extract_first()
        fields['name'] = name.strip().lower()

        group_header_fields = response.xpath(
            ".//div[contains(@class, 'node')]/div[contains(@class, 'group-header')]/div[not(contains(@class, "
            "'field--name-node-title')) and not(contains(@class, 'field--name-field-company-logo'))]")

        for field in group_header_fields:
            label = field.xpath(".//div[@class='field--label']/text()").extract_first()

            if label is not None and label.strip() in self.fields_to_extract:
                index = label.find('(')
                if index != -1:
                    label = label[:index]

                label = re.sub('\\s/\\s|\\s', '_', label.strip()).lower()

                item = field.xpath(".//div[@class='field--item']/text()").extract_first()
                if item is None:
                    item = field.xpath(".//div[@class='field--item']/a/text()").extract_first()

                if item is not None:
                    fields[label] = item.strip().lower()

            for key in fields:
                company[key] = fields[key]

        print(company)

        return company
