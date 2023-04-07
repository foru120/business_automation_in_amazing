from pathlib import Path
import os

from crawlers.kcdcode_crawler import KCDCODE_CRAWLER
from crawlers.common.const import CONST


if __name__ == '__main__':
    crawler = KCDCODE_CRAWLER(CONST.URL_KCDCODE)
    crawler.save_path = os.path.join(Path(__file__).parent, 'output', '질병분류코드_20230406.xlsx')
    crawler.start_crawling()
