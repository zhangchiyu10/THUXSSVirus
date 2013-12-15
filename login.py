# -*- coding: utf-8 -*- 
import urllib2, urllib, cookielib,re,sys,time,socket
from bs4 import BeautifulSoup
def post_machine(t,j):
    pre='learn.tsinghua.edu.cn	FALSE	/	FALSE		'
    f=open('cookies.txt','wb')
    f.write('# Netscape HTTP Cookie File')
    f.write(''.join([pre,'JSESSIONID','\t',j,'\n']))
    f.write(''.join([pre,'THNSV2COOKIE','\t',t,'\n']))
    f.close()               
                  
    cjar = cookielib.MozillaCookieJar()
    cjar.load('cookies.txt',ignore_discard=True, ignore_expires=True)
    #print cjar
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)
    domain='http://learn.tsinghua.edu.cn'
    login_page = "".join([domain,'/MultiLanguage/lesson/teacher/loginteacher.jsp'])
    userName="zhangchiyu10"
    password="jp071337"
    page=opener.open(login_page,urllib.urlencode({'userid':userName, 'userpass':password}))#POST
    cjar.save('cookies.txt',ignore_discard=True, ignore_expires=True)
    print cjar
    try:
        #get list of courses
        page=opener.open("".join([domain,'/MultiLanguage/lesson/student/MyCourse.jsp?typepage=2']))
        soup = BeautifulSoup(page.read())
        course=[soup.findAll(attrs={'class':'info_tr'}),soup.findAll(attrs={'class':'info_tr2'})]
        bbs_url='http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/bbs_talk_submit.jsp?post_par_id=0000&post_up_url=talk_list_student.jsp&post_cate_id=1'
        post_title='Americans%20attack%20Tsinghua%20network%3F'
        post_detail='Yes%2C%20we%20scan%21'
        bbs_url="".join([bbs_url,'&post_title=',post_title,'&post_detail=',post_detail])
        count=0       
        for c in course:
            course_id=c[0].td.a['href'][58:]
            #get post_bbs_id
            page=opener.open(''.join([domain,'/MultiLanguage/public/bbs/gettalkid_student.jsp?course_id=',course_id]))
            soup = BeautifulSoup(page.read())
            new_url=soup.find(attrs={'id':'new_url'})['href']
            post_bbs_id=new_url[52:new_url.find('&',52)]
            POST_url="".join([bbs_url,'&course_id=',course_id,'&post_bbs_id=',post_bbs_id])
            #post bbs
            opener.open(POST_url)
            print course_id,"done!"
            count=count+1
            if count>2:
                break
    except Exception,e:
        print str(e)

if __name__ == '__main__':
    sock_notice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_notice.bind(('127.0.0.1',9875))
while True:
    data, addr = sock_notice.recvfrom(2048)
    message=BeautifulSoup(data)
    print message
    j=message.j.contents[0]
    t=message.t.contents[0]
    #post_machine(t,j)
    break
    
