import scrapy


class ValueTodayCompanyItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    headquarters_continent = scrapy.Field()
    headquarters_country = scrapy.Field()
    headquarters_sub_region = scrapy.Field()
    headquarters_region_city = scrapy.Field()
    annual_revenue_in_usd = scrapy.Field()
    annual_net_income_in_usd = scrapy.Field()
    annual_results_for_year_ending = scrapy.Field()
    total_assets_in_usd = scrapy.Field()
    total_liabilities_in_usd = scrapy.Field()
    total_equity_in_usd = scrapy.Field()
    company_business = scrapy.Field()
    ipo_year = scrapy.Field()
    ceo = scrapy.Field()
    founders = scrapy.Field()
    founded_year = scrapy.Field()
    number_of_employees = scrapy.Field()
    company_website = scrapy.Field()
    world_rank = scrapy.Field()
    market_value = scrapy.Field()


class CMCompanyItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    # rank = scrapy.Field()
    # market_cap = scrapy.Field()
    # country = scrapy.Field()
    # share_price = scrapy.Field()
    # change_1_day = scrapy.Field()
    # change_1_year = scrapy.Field()
    # categories = scrapy.Field()
