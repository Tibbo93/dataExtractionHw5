import logging

from scrapy.exporters import JsonLinesItemExporter


class DataExtractionHw5Pipeline:

    def __init__(self, file_name):
        self.exporter = None
        self.file_name = file_name
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        output_file_name = crawler.settings.get('OUTPUT_FILE_PATHNAME')
        return cls(output_file_name)

    def open_spider(self, spider):
        logging.info('JsonLines export opened')

        file = open(self.file_name, 'wb')
        self.file_handle = file

        self.exporter = JsonLinesItemExporter(file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        logging.info('JsonLines exporter closed')
        self.exporter.finish_exporting()
        self.file_handle.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
