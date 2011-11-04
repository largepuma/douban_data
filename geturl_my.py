# coding=utf-8
'''
Created on 2011-8-26

@author: liuxh
'''

import HTMLParser
class MyHTMLParser(HTMLParser.HTMLParser):
    """This is my HTMLParser to get the book information of douban"""
    #the mode of get data
    NAME = 0
    VOTES = 1
    AVERAGE = 2
    ISBN = 3
    PRICE = 4
    
    def reset(self):
        self.getdata = 0
        self.mode = None
        self.name = None
        self.votes = -1
        self.average = None
        self.isbn = None
        self.price = None
        HTMLParser.HTMLParser.reset(self)
        
    def handle_starttag(self, tag, attrs):
        if "span" == tag:
            if len(attrs) > 0 and len(attrs[0]) > 0:
                if attrs[0][0] == "property" and attrs[0][1] == "v:itemreviewed":
                    self.getdata = 1
                    self.mode = MyHTMLParser.NAME
                elif attrs[0][0] == "property" and attrs[0][1] == "v:votes":
                    self.getdata = 1
                    self.mode = MyHTMLParser.VOTES
        if "strong" == tag:
            if len(attrs) == 2 and len(attrs[1][0]) > 0:
                if attrs[1][0] == "property" and attrs[1][1] == "v:average":
                    self.getdata = 1
                    self.mode = MyHTMLParser.AVERAGE
                
    def handle_data(self, data):
        if u"定价" in data:
            self.getdata = 1
            self.mode = MyHTMLParser.PRICE
            return
        if u"ISBN:" in data:
            self.getdata = 1
            self.mode = MyHTMLParser.ISBN
            return
        if self.getdata == 1:
            if self.mode == MyHTMLParser.NAME:
                self.name = data
            elif self.mode == MyHTMLParser.VOTES:
                if data != None:
                    self.votes = int(data)
            elif self.mode == MyHTMLParser.AVERAGE:
                if data != None:
                    self.average = data
            elif self.mode == MyHTMLParser.PRICE:
                if data != None:
                    self.price = data
            elif self.mode == MyHTMLParser.ISBN:
                if data != None:
                    self.isbn = data
        self.getdata = 0
            

class MyDataBase():
    """This is used to manage the database"""
    
    def __init__(self):
#        import sqlite3
#        self.conn = sqlite3.connect('bookstore.db')
#        self.c = self.conn.cursor()
        import MySQLdb
        self.conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "112233",
                           db = "douban_data")
        self.cursor = self.conn.cursor ()
        
    
    def init(self):
        # Create table
#        self.c.execute('''create table if not exists books
#            (id integer primary key autoincrement, name text, votes Integer, average text, url text, isbn text, price text)''')
        pass
    
    def insert(self, data):
        # Insert a row of data
        self.cursor.execute(data)
    
    def commit(self):
        self.conn.commit()
        
    def close(self):
#        self.c.close()
        self.cursor.close()
        self.conn.close()


def main():
    import urllib2
    import time
    MAX = 6803421
    prefix = "http://book.douban.com/subject/"
    #index = 1000001
    index = 1039391
    p = MyHTMLParser()
    db = MyDataBase()
    db.init()
    while index < MAX:
        try:
            murl = prefix + str(index) + '/'
            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0'}
            req = urllib2.Request(url = murl,headers = headers)
            sock = urllib2.urlopen(req)
            realUrl = sock.geturl()
            realUrl = realUrl[7:]
            htmlSource = sock.read()
            sock.close()
            p.reset()
            p.feed(htmlSource)
            p.close
            sql = """insert into books values (null,'%s', %d, '%s', '%s', '%s', '%s')""" % (p.name, p.votes, p.average, realUrl, p.isbn, p.price)
            print sql
            db.insert(sql);
            db.commit()
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print "something is error"
        index = index + 1
        time.sleep(1)
    db.close()


if __name__ == '__main__':
    main()
 
    