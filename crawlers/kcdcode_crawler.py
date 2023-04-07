import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime

from crawlers.common.const import CONST
from crawlers.dto.tag import Tag
from excel.write import Writer


class KCDCODE_CRAWLER:

    def __init__(self, def_url):
        self.init_driver(def_url)
        self.init_variable()

    def init_driver(self, def_url):
        options = uc.ChromeOptions()
        options.add_argument("headless")
        self.driver = uc.Chrome(options=options)
        self.driver.get(def_url)

    def init_variable(self):
        self.__save_path = ""
        self.level = 0
        self.div_tag_name = "kcdf_cleft"
        self.ul_tag_name = "kcdf_cname"
        self.def_xpath = '//div[@id="{}"]/ul[@class="{}"]/li'
        self.data = []

    @property
    def save_path(self):
        return self.__save_path

    @save_path.setter
    def save_path(self, value):
        self.__save_path = value

    def start_crawling(self):
        if self.save_path == "":
            print("데이터 저장 경로가 설정되지 않았습니다.")
            print("=> save_path 를 설정해주세요.")
        else:
            print("데이터 크롤링을 시작합니다.")
            start = time.time()
            self.recursive_crawling(None)
            end = time.time()
            sec = (end - start)
            result_list = str(datetime.timedelta(seconds=sec)).split(".")
            print("데이터 크롤링이 완료되었습니다. 소요 시간(s): {}".format(result_list[0]))

            print("데이터를 저장합니다.")
            self.save_data()
            print("데이터 저장이 완료되었습니다.")

    def recursive_crawling(self, top_code):
        li_tag_list = self.driver.find_elements(
            By.XPATH, self.def_xpath.format(self.div_tag_name if top_code is None else self.div_tag_name + str(self.level),
                                            self.ul_tag_name))
        num = 1

        for li_tag in li_tag_list:
            a_tag = self.get_a_tag(li_tag)
            code = self.get_code(top_code, num)
            self.add_data(Tag(code, top_code, a_tag.text))
            self.spread_tag(a_tag)
            self.recursive_crawling(code)
            num += 1

        self.level -= 1

    def get_a_tag(self, tag):
        return tag.find_element(By.XPATH, './a')

    def add_data(self, tag):
        self.data.append(tag)

    def get_code(self, top_code, num):
        if top_code is None:
            code = list("000000000000000000")
        else:
            code = list(top_code)

        code[self.level*3:(self.level+1)*3] = str(num).zfill(3)
        return "".join(code)

    def spread_tag(self, tag):
        # tag.click()
        tag.send_keys(Keys.ENTER)
        time.sleep(0.1)
        self.level += 1

    def save_data(self):
        excel_writer = Writer()
        excel_writer.write_excel_data(
            self.save_path,
            CONST.CODE_DISEASE_CLASSIFICATION,
            ["질병분류코드", "질병분류상위코드", "코드명"],
            self.data
        )


if __name__ == "__main__":
    crawler = KCDCODE_CRAWLER(CONST.URL_KCDCODE)
    crawler.recursive_crawling(None)