import string
import uuid
import scrapy
import re

from dataExtractionHw5.items import HitHorizonsCompanyItem


class HitHorizonSpyder(scrapy.Spider):
    name = 'HitHorizons'
    allowed_domains = ['www.hithorizons.com']
    start_urls = ['https://www.hithorizons.com/search?Name=&Address=italy&ShowBranches=false&CompanyTypes=10'
                  '&CompanyTypes=11&CompanyTypes=12&CompanyTypes=160&CompanyTypes=3&CompanyTypes=14&CompanyTypes=102'
                  '&CompanyTypes=120&CompanyTypes=151&CompanyTypes=167&CompanyTypes=13&CompanyTypes=107&CompanyTypes'
                  '=154&CompanyTypes=100&CompanyTypes=0&CompanyTypes=999']

    # fields_to_extract = ['Official Name:', 'Employees:', 'Headquarters:', 'CEO:', 'Founded:']
    # fields_dictionary = {'Official Name:': 'official_name', 'Employees:': 'employees', 'CEO:': 'ceo',
    #                     'Founded:': 'founded'}

    def __init__(self, num_instances=10):
        super().__init__()
        self.num_instances = int(num_instances)

    def parse(self, response):
        companies_url = response.xpath(".//div[contains(@class, 'search-result-title')]/h3/a/@href").extract()
        url = companies_url[0]
        yield response.follow(url, self.parse_company)
        #for url in companies_url:
        #    if self.num_instances <= 0:
        #        return
        #    self.num_instances -= 1
        #    yield response.follow(url, self.parse_company)
        # make request for next page
        # next_page = response.xpath(".//i[contains(text(), 'chevron_right')]/parent::a/@href").extract_first()
        # if next_page is not None:
        #    yield response.follow(next_page, self.parse)

    def parse_company(self, response):
        company = HitHorizonsCompanyItem()
        # Id
        fields = {'id': uuid.uuid4().hex}
        # name
        name = response.xpath(".//ul[contains(@class, 'overview-data-1')]/li/strong[contains(text(), "
                              "'Name')]/following-sibling::span/text()").extract_first()
        fields['name'] = string.capwords(name.strip())
        # address
        address = response.xpath(".//ul[contains(@class, 'overview-data-1')]/li/strong[contains(text(), "
                                 "'Address')]/following-sibling::span/text()").extract_first()
        fields['address'] = address.strip()
        # nation
        nation = response.xpath(".//ul[contains(@class, 'overview-data-1')]/li/strong[contains(text(), 'National "
                                "ID')]/following-sibling::span/text()").extract_first()
        fields['nation'] = nation.strip()
        # hithorizons id
        hhid = response.xpath(".//ul[contains(@class, 'overview-data-1')]/li/strong[contains(text(), 'HitHorizons "
                              "ID')]/following-sibling::span/text()").extract_first()
        fields['hhid'] = hhid.strip()
        # industry
        industry = response.xpath(".//ul[contains(@class, 'overview-data-2')]/li/strong[contains(text(), "
                                  "'Industry')]/following-sibling::span/text()[2]").extract_first()
        fields['industry'] = industry.strip()
        # sic code
        sic_code = response.xpath(".//ul[contains(@class, 'overview-data-2')]/li/strong[contains(text(), "
                                  "'SIC Code')]/following-sibling::span/text()[2]").extract_first()
        fields['sic_code'] = sic_code.strip()
        # type
        type = response.xpath(".//ul[contains(@class, 'overview-data-2')]/li/strong[contains(text(), "
                              "'Type')]/following-sibling::span/text()").extract_first()
        fields['type'] = type.strip()
        # est. of ownership
        est_of_ownership = response.xpath(".//ul[contains(@class, 'overview-data-2')]/li/strong[contains(text(), "
                                          "'Est. of Ownership')]/following-sibling::span/text()").extract_first()
        fields['est_of_ownership'] = est_of_ownership.strip()

        for key in fields:
            company[key] = fields[key]

        return company
