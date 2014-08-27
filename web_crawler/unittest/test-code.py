import sys
if '../' not in sys.path:
        sys.path.append('../')

# from utils.dbhelper import DBHelper
# dbhelper = DBHelper('c:\\tmp.db')
# sql = "Drop table if exists `student`"
# dbhelper.execute(sql)
# dbhelper.commit()

create_table_sql = '''CREATE TABLE if not exists `student` (
                          `id` int(11) NOT NULL,
                          `name` varchar(20) NOT NULL,
                          `gender` varchar(4) DEFAULT NULL,
                          `age` int(11) DEFAULT NULL,
                          `address` varchar(200) DEFAULT NULL,
                          `phone` varchar(20) DEFAULT NULL,
                           PRIMARY KEY (`id`)
                        )'''
# dbhelper.execute(create_table_sql)
# dbhelper.commit()
# sql = "insert into student(id, name,age,phone) values(1,'ali',12,12345)"
# dbhelper.execute(sql)
# dbhelper.commit()
# sql = "select * from student"
# print(dbhelper.select(sql))
#import logging
#logger = logging.getLogger(__name__)
#logger.setLevel(10)
#formatter = logging.Formatter('%(name)-6s %(asctime)s %(levelname)-4s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
#file_handler = logging.FileHandler("test.log")  
#file_handler.setFormatter(formatter)  
#stream_handler = logging.StreamHandler(sys.stderr)  
#logger.addHandler(file_handler)  
#logger.addHandler(stream_handler)
#logger.debug('debug')
#logger.error('error')

import multiprocessing
from multiprocessing import freeze_support
freeze_support()

class MyProcess(multiprocessing.Process):
    def run(self):
        while True:
            time.sleep(1)
            print('process')

p = MyProcess()
p.start()
