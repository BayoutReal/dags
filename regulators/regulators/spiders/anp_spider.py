import scrapy


class AnpSpider(scrapy.Spider):
    name = 'anp_spider'
    # Começando pela primeira página (1)
    start_urls = ['https://atosoficiais.com.br/anp?q=&types=151&page=1']

    def parse(self, response, **kwargs):
        # Seleciona todos os links da página atual
        items = response.xpath('//*[@id="content"]/div/div[2]/div/section/div/div/a')
        for item in items:
            link = item.xpath('./@href').get()  # Obtém o link para cada item
            if link:
                yield response.follow(url=link, callback=self.parse_item)

        # Extrai o número da página atual para continuar avançando
        current_page = int(response.url.split('&page=')[-1])
        last_page = 1718  # Substitua com o número da última página se souber
        if current_page < last_page:
            next_page_url = f'https://atosoficiais.com.br/anp?q=&types=151&page={current_page + 1}'
            yield response.follow(url=next_page_url, callback=self.parse)

    def parse_item(self, response):
        # Extrai os dados da página de detalhe
        title = response.xpath('//*[@id="lei"]/div[3]/center/text()').get()
        authorization = response.xpath('//*[@id="lei"]/h2/text()').get()
        norm_text = response.xpath(
            '//*[@id="conteudo-principal"]//text()').getall()  # Pega todo o texto, incluindo elementos filhos
        norm_text = ' '.join(norm_text).strip()  # Junta os textos e remove espaços extras

        yield {
            'title': title.strip() if title else 'No Title',
            'authorization': authorization.strip() if authorization else 'No Authorization',
            'norm_text': norm_text.strip() if norm_text else 'No Norm Text'
        }
