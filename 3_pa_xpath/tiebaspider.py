#-*-coding:utf8-*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
# 审查元素要直接审查返回的内容，防止执行js改变结构，
reload(sys)

sys.setdefaultencoding('utf-8')

'''重新运行之前请删除content.txt，因为文件操作使用追加方式，会导致内容太多。'''

def towrite(contentdict):
    f.writelines(u'回帖时间:' + str(contentdict['topic_reply_time']) + '\n')
    f.writelines(u'回帖内容:' + unicode(contentdict['topic_reply_content']) + '\n')
    f.writelines(u'回帖人:' + contentdict['user_name'] + '\n\n')

def spider(url):
    html = requests.get(url)
    print url


    #print html.text
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')#l_post j_l_post l_post_bright
    #content_field = selector.xpath('//div[@class="core_title_wrap core_title_wrap_bright"]')  # l_post j_l_post l_post_bright



    #print content_field

    #print content_field[0].xpath('string(.)')
    item = {}
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot',''))
        author = reply_info['author']['user_name']
        content = each.xpath('div[@class="d_post_content_main"]/div/cc/div/text()')[0]
        reply_time = reply_info['content']['date']
        # print content
        # print reply_time
        # print author
        item['user_name'] = author
        item['topic_reply_content'] = content
        item['topic_reply_time'] = reply_time
        towrite(item)

if __name__ == '__main__':
    pool = ThreadPool(5)
    f = open('content.txt','a')
    page = []
    for i in range(1,11):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)

    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()