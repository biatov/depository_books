import re
from scrapy.spiders import SitemapSpider
from ..items import BookdepositItem


class BookSpider(SitemapSpider):
    name = 'deposit_books'
    allowed_domains = ['bookdepository.com']

    def __init__(self, page=1, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.page = page
        self.sitemap_urls = ['https://www.bookdepository.com/sitemaps/item/sitemap%s.xml.gz' % self.page]
        # 671 xml
        self.sitemap_rules = [('.+', 'parse')]
        self._cbs = list()
        for r, c in self.sitemap_rules:
            if isinstance(c, str):
                c = getattr(self, str(c))
            self._cbs.append((re.compile(r), c))
        self._follow = [re.compile(x) for x in self.sitemap_follow]

    def parse(self, response):
        item = BookdepositItem()
        no_data = '-'
        item['BookURL'] = response.url
        try:
            item['ImageURL'] = response.xpath('//img[@class="book-img"]/@src').extract_first().strip()
        except AttributeError:
            item['ImageURL'] = no_data
        back = response.xpath('//label[contains(text(), "Format")]/following-sibling::span/text()').extract_first()
        pages = response.xpath('//label[contains(text(), "Format")]/following-sibling::span/span/text()').extract_first()
        try:
            item['Format'] = ' '.join([' '.join(back.strip().split()), pages if pages else '']).strip()
        except AttributeError:
            item['Format'] = no_data
        try:
            dimensions = response.xpath('//label[contains(text(), "Dimensions")]/following-sibling::span/text()').extract_first().strip().split()
            if '|' in dimensions:
                item['Dimensions'] = ' '.join(dimensions[:-2])
            else:
                item['Dimensions'] = ' '.join(dimensions)
        except (AttributeError, IndexError):
            item['Dimensions'] = no_data
        try:
            weight = response.xpath('//label[contains(text(), "Dimensions")]/following-sibling::span/text()').extract_first().strip().split()
            item['Weight'] = weight[-1] if '|' in weight else no_data
        except (AttributeError, IndexError):
            item['Weight'] = no_data
        try:
            item['Pubdate'] = response.xpath('//label[contains(text(), "Publication date")]/following-sibling::*/text()').extract_first().strip()
        except AttributeError:
            item['Pubdate'] = no_data
        try:
            item['Publisher'] = ', '.join(map(lambda i: i.strip(), response.xpath('//label[contains(text(), "Publisher")]/following-sibling::span/a/text()').extract()))
        except AttributeError:
            item['Publisher'] = no_data
        try:
            item['Language'] = response.xpath('//label[contains(text(), "Language")]/following-sibling::span/text()').extract_first().strip()
        except AttributeError:
            item['Language'] = no_data
        try:
            item['Illustrationsnote'] = response.xpath('//label[contains(text(), "Illustrations note")]/following-sibling::span/text()').extract_first().strip()
        except AttributeError:
            item['Illustrationsnote'] = no_data
        try:
            item['ISBN10'] = response.xpath('//label[contains(text(), "ISBN10")]/following-sibling::span/text()').extract_first().strip()
        except AttributeError:
            item['ISBN10'] = no_data
        try:
            item['ISBN13'] = response.xpath('//label[contains(text(), "ISBN13")]/following-sibling::span/text()').extract_first().strip()
        except AttributeError:
            item['ISBN13'] = no_data
        try:
            item['Bestsellersrank'] = response.xpath('//label[contains(text(), "rank")]/following-sibling::span/text()').extract_first().strip()
        except AttributeError:
            item['Bestsellersrank'] = no_data
        try:
            item['Title'] = response.xpath('//h1[@itemprop="name"]/text()').extract_first().strip()
        except AttributeError:
            item['Title'] = no_data
        try:
            item['FullDesc'] = response.xpath('//div[@itemprop="description"]/text()').extract_first().strip()
        except AttributeError:
            item['FullDesc'] = no_data
        check_stock = response.xpath('//div[@class="availability-text"]/p/span/text()').extract_first()
        if check_stock:
            stock = check_stock
        else:
            stock = response.xpath('//div[@class="item-info-wrap"]/p[@class="red-text bold"]/text()').extract_first()
        try:
            item['stock'] = ' '.join(stock.strip().split())
        except AttributeError:
            item['stock'] = no_data
        try:
            price = response.xpath('//span[@class="sale-price"]/text()').extract_first().strip()
        except AttributeError:
            try:
                price = response.xpath('//p[@class="list-price"]/text()').extract_first().split(':')[1].strip()
            except (IndexError, AttributeError):
                price = no_data
        if price:
            item['Price'] = price
        else:
            item['Price'] = no_data
        author = response.xpath('//div[@class="author-info hidden-md"]/a/text()').extract()
        if author:
            item['Author'] = ', '.join(author)
        else:
            item['Author'] = no_data
        categories = response.xpath('//ol[@class="breadcrumb"]//li[position()>1]/a/text()').extract()
        try:
            item['Category'] = ', '.join(map(lambda i: i.strip(), categories))
        except AttributeError:
            item['Category'] = no_data
        yield item
