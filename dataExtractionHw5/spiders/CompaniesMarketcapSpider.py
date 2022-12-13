import string
import uuid
import scrapy

from dataExtractionHw5.items import CMCompanyItem


class CMSpyder(scrapy.Spider):
    name = 'companiesMarketCap'
    allowed_domains = ['companiesmarketcap.com']
    start_urls = ['https://companiesmarketcap.com/']

    def __init__(self, num_instances=1000):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(".//td[contains(@class, 'name-td')]/div[2]/a/@href").extract()

        for url in companies_url:
            if self.num_instances <= 0:
                return
            self.num_instances -= 1
            yield response.follow(url, self.parse_company)

        # make request for next page
        next_page = response.xpath(".//nav/ul[contains(@class, 'pagination')]/li/a[last()]/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        company = CMCompanyItem()
        # id
        fields = {'id': uuid.uuid4().hex}

        # name
        name = response.xpath(".//div[contains(@class, 'company-title-container')]/div[1]/text()").extract_first()
        if name is not None:
            fields['name'] = string.capwords(name.strip())

        # rank
        rank = response.xpath(".//div[contains(text(), 'Rank')]/preceding-sibling::div/text()").extract_first()
        if rank is not None:
            rank = rank[1:]
            fields['rank'] = rank.strip()

        # marketcap
        market_cap = response.xpath(".//div[contains(text(), 'Marketcap')]/preceding-sibling::div/text()").extract_first()
        if market_cap is not None:
            fields['market_cap'] = market_cap.strip()

        # country
        country = response.xpath(".//div[contains(text(), 'Country')]/preceding-sibling::div/a/span/text()").extract_first()
        if country is not None:
            fields['country'] = country.strip()

        # share_price
        share_price = response.xpath(".//div[contains(text(), 'Share price')]/preceding-sibling::div/text()").extract_first()
        if share_price is not None:
            fields['share_price'] = share_price.strip()

        # change_1_day
        change_1_day = response.xpath(".//div[contains(text(), 'Change (1 day)')]/preceding-sibling::div/span/text()").extract_first()
        if change_1_day is not None:
            fields['change_1_day'] = change_1_day.strip()

        # change_1_year
        change_1_year = response.xpath(".//div[contains(text(), 'Change (1 year)')]/preceding-sibling::div/span/text()").extract_first()
        if change_1_year is not None:
            fields['change_1_year'] = change_1_year.strip()

        # Categories
        categories = response.xpath(
            "//div[contains(text(), 'Categories')]/preceding-sibling::div/a/text()").extract()
        categories_cleaned = []
        for category in categories:
            categories_cleaned.append(category.encode('ascii', 'ignore').decode('utf-8').strip())
        if len(categories_cleaned) > 0:
            fields['categories'] = categories_cleaned

        for key in fields:
            company[key] = fields[key]

        return company
