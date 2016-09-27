# -*- coding:gbk -*-
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='i://myapp.log',
                filemode='a')

#����һ��StreamHandler����INFO�������ߵ���־��Ϣ��ӡ����׼���󣬲�������ӵ���ǰ����־�������#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')