import string
import uuid
import scrapy

from dataExtractionHw5.items import CMCompanyItem


class CMSpyder(scrapy.Spider):
    name = 'CompaniesMarketcap'
    allowed_domains = ['companiesmarketcap.com']
    start_urls = ['https://companiesmarketcap.com/united-kingdom/largest-companies-in-the-uk-by-market-cap/']

    def __init__(self):
        super().__init__()

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

        # rank
        rank = response.xpath(".//div[contains(text(), 'Rank')]/preceding-sibling::div/text()").extract_first()
        rank = rank[1:]
        fields['rank'] = rank.strip()

        # marketcap
        market_cap = response.xpath(".//div[contains(text(), 'Marketcap')]/preceding-sibling::div/text()").extract_first()
        fields['market_cap'] = market_cap.strip()

        # country
        country = response.xpath(".//div[contains(text(), 'Country')]/preceding-sibling::div/a/span/text()").extract_first()
        fields['country'] = country.strip()

        # share_price
        share_price = response.xpath(".//div[contains(text(), 'Share price')]/preceding-sibling::div/text()").extract_first()
        fields['share_price'] = share_price.strip()

        # change_1_day
        change_1_day = response.xpath(".//div[contains(text(), 'Change (1 day)')]/preceding-sibling::div/span/text()").extract_first()
        fields['change_1_day'] = change_1_day.strip()

        # change_1_year
        change_1_year = response.xpath(".//div[contains(text(), 'Change (1 year)')]/preceding-sibling::div/span/text()").extract_first()
        fields['change_1_year'] = change_1_year.strip()

        for key in fields:
            company[key] = fields[key]

        return company
