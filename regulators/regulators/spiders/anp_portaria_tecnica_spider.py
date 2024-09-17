import scrapy

class AnpPortariaTecnicaSpider(scrapy.Spider):
    name = 'anp_portaria_tecnica_spider'
    # Starting from the initial page (145)
    start_urls = ['https://atosoficiais.com.br/anp?q=&types=198&page=145']  # Update with correct URL for "Portaria Técnica"

    def parse(self, response, **kwargs):
        # Select all the links on the current page
        items = response.xpath('//*[@id="content"]/div/div[2]/div/section/div/div/a')
        for item in items:
            link = item.xpath('./@href').get()  # Get the link for each item
            if link:
                yield response.follow(url=link, callback=self.parse_item)

        # Extract the current page number to continue crawling backward
        current_page = int(response.url.split('&page=')[-1])
        if current_page > 1:
            previous_page_url = f'https://atosoficiais.com.br/anp?q=&types=198&page={current_page - 1}'  # Adjust the type if needed
            yield response.follow(url=previous_page_url, callback=self.parse)

    def parse_item(self, response):
        # Extract the data from the detail page
        title = response.xpath('//*[@id="lei"]/div[3]/center/text()').get()
        portaria_tecnica = response.xpath('//*[@id="lei"]/h2/text()').get()  # Changed to portaria_tecnica
        norm_text = response.xpath(
            '//*[@id="conteudo-principal"]//text()').getall()  # Get all the text, including child elements
        norm_text = ' '.join(norm_text).strip()  # Join the texts and remove extra spaces

        yield {
            'title': title.strip() if title else 'No Title',
            'portaria_tecnica': portaria_tecnica.strip() if portaria_tecnica else 'No Portaria Técnica',
            'norm_text': norm_text.strip() if norm_text else 'No Norm Text'
        }
