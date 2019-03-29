from bs4 import BeautifulSoup
import re
import logging

import open_url
import login_selenium

import os


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")


def config_log():
    logging.basicConfig(filename="log.log",
                        format=r'%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s',
                        datefmt=r'%Y-%m-%d %H:%M:%S %p',
                        level=10)


def get_page():
    str = login_selenium.login()
    # f = open("test.html", "r", encoding="utf-8")
    # str = f.read()
    return str


if __name__ == '__main__':
    config_log()

    logging.log(10, "begin anylize")

    str = get_page()

    logging.log(10, "begin souping")
    soup = BeautifulSoup(str, "html5lib")
    logging.log(10, "end souping")

    logging.log(10, "finding class list")
    classes_list = soup.findAll("ul", attrs={"class": "courseDetail-weekList-chapterUl"})
    logging.log(10, "found %d class list, class=courseDetail-weekList-chapterUl", len(classes_list))

    cl_li = classes_list[0].findAll("li", attrs={"class":
                                     re.compile(
                                         "courseDetail-weekList-chapterLi show courseDetail-weekList-level. active")})
    print(len(cl_li))

    result = []
    for item in cl_li:
        item_a = item.findAll("a")[0]
        item_a_imformation = dict(item_a.attrs)

        item_a_imformation.pop("href", "not found")
        item_a_imformation.pop("class", "not found")
        item_a_imformation.pop("data-checked", "not found")
        result.append(item_a_imformation)
        print(item_a_imformation)

        if item_a_imformation['data-istasks'] == 'true':
            item_ul = item.findAll("ul")[0]
            item_ul_li = item_ul.findAll("li")
            for (i, li) in enumerate(item_ul_li):
                li_a = li.findAll("a")[0]
                li_a_attrs_dict = li_a.attrs

                item_detail_information = dict()
                item_detail_information['data-node'] = '%s-%d' % (item_a_imformation['data-node'], i)
                item_detail_information['data-istasks'] = 'video'
                item_detail_information['data-level'] = "%d" % (int(item_a_imformation['data-level']) + 1)
                item_detail_information['title'] = li_a_attrs_dict['title']
                item_detail_information["link"] = li_a_attrs_dict['link']
                result.append(item_detail_information)
                print(item_detail_information)

    for item in result:
        if item['data-istasks'] == "video":
            url = "https://elearning.zbgedu.com/" + item['link']
            print(url)
            open_url.open_url(url)
            exit()

    # http://xiaohuang.cc/post/544.html

    # http://passport.flvcd.com/my/multi.php
