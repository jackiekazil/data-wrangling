import scrapy
from scrapyspider.items import PythonPackageItem


class PackageSpider(scrapy.Spider):
    name = 'package_test'
    allowed_domains = ['pypi.python.org']
    start_urls = [
        'https://pypi.python.org/pypi/scrapely/0.12.0',
        'https://pypi.python.org/pypi/dc-campaign-finance-scrapers/0.5.1',
    ]

    def parse(self, response):
        item = PythonPackageItem()
        item['package_page'] = response.url
        item['package_name'] = response.xpath(
            '//div[@class="section"]/h1/text()').extract()
        item['package_short_description'] = response.xpath(
            '//meta[@name="description"]/@content').extract()
        item['home_page'] = response.xpath(
            '//li[contains(strong, "Home Page:")]/a/@href').extract()
        item['python_versions'] = []
        versions = response.xpath(
            '//li/a[contains(text(), ":: Python ::")]/text()').extract()
        for v in versions:
            version_number = v.split("::")[-1]
            item['python_versions'].append(version_number.strip())
        item['last_month_downloads'] = response.xpath(
            '//li/text()[contains(., "month")]/../span/text()').extract()
        item['package_downloads'] = response.xpath(
            '//table/tr/td/span/a[contains(@href,"pypi.python.org")]/@href'
        ).extract()
        return item
