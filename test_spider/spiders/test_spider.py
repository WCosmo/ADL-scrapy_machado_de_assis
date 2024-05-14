from pathlib import Path
import csv
import scrapy
import os
import time
import PyPDF2
import codecs

class TestSpider(scrapy.Spider):

    name = 'test'

    start_urls = [
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/23-romance',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/24-conto',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/25-poesia',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/26-cronica',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/27-teatro',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/28-critica',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/29-traducao',
        'https://machado.mec.gov.br/obra-completa-lista/itemlist/category/30-miscelanea',
    ]

    def parse(self, response):
        download_links = response.css('a[title="Download"]::attr(href)').getall()

        for link in download_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        current_dir = os.getcwd()
        path = Path(current_dir) / 'downloads'
        path.mkdir(parents=True, exist_ok=True)

        filename = response.url.split("/")[-1] + '.pdf'
        with open(path / filename, 'wb') as file:
            file.write(response.body)

        self.extract_text_from_pdf(path / filename)

    def extract_text_from_pdf(self, pdf_path):
        pdf_file_obj = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = len(pdf_reader.pages)

        text_file_path = Path(os.getcwd()) / 'my-portuguese-data.txt'
        with codecs.open(text_file_path, 'a', 'ansi') as text_file:
            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                text_file.write(page_obj.extract_text())
