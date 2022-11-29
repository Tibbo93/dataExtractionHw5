import uuid
import scrapy
import re
import string

from dataExtractionHw5.items import ValueTodayCompanyItem


class ValueTodaySpider(scrapy.Spider):
    name = 'valueToday'
    allowed_domains = ['www.value.today']
    start_urls = ['https://www.value.today/']
    fields_to_extract = \
        ['Headquarters Country', 'Headquarters Sub Region', 'World Rank (Jan-07-2022)', 'Market Value (Jan-07-2022)',
         'Annual Revenue in USD', 'Annual Net Income in USD', 'Annual Results for Year Ending', 'Total Assets in USD',
         'Total Liabilities in USD', 'Total Equity in USD', 'Headquarters Region / City', 'Company Business',
         'Number of Employees', 'Headquarters Continent', 'IPO Year', 'CEO:', 'Founders', 'Founded Year',
         'Company Website:']

    def __init__(self, num_instances=20):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(".//div[contains(@class, 'field--name-node-title')]/h2/a/@href").extract()
        for url in companies_url:
            if self.num_instances <= 0:
                return
            self.num_instances -= 1
            yield response.follow(url, self.parse_company)

        # make request for next page
        next_page = response.xpath(".//ul[contains(@class, 'pagination')]/li[contains(@class, "
                                   "'pager__item--next')]/a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        company = ValueTodayCompanyItem()
        fields = {'id': uuid.uuid4().hex}

        name = response.xpath(".//div[contains(@class, 'field--name-node-title')]/h1/a/text()").extract_first()
        fields['name'] = string.capwords(name.strip())

        fields_node = response.xpath(".//div[contains(@class, 'group-header') or contains(@class, 'group-left') or "
                                     "contains(@class, 'group-right')  ]/div[not(contains(@class, 'field--item'))]")

        for field in fields_node:
            label = field.xpath(".//div[@class='field--label']/text()").extract_first()

            if label is not None and label.strip() in self.fields_to_extract:

                if label == 'Company Website:':
                    item = field.xpath(".//div[@class='field--item']/a/@href").extract_first()
                    label = re.sub('\\s/\\s|\\s', '_', label.strip().replace(':', '')).lower()
                    fields[label] = item
                    continue

                index = label.find('(')
                if index != -1:
                    label = label[:index]

                label = re.sub('\\s/\\s|\\s', '_', label.strip().replace(':', '')).lower()

                item = field.xpath(".//div[@class='field--item']/text()").extract_first()
                if item is None:
                    item = field.xpath(".//div[@class='field--item']/a/text()").extract()
                    item = [str.encode('ascii', 'ignore').decode('utf-8') for str in item]
                    if len(item) == 1:
                        item = item.pop()

                if item is not None:
                    fields[label] = item

        for key in fields:
            company[key] = fields[key]

        return company
