import web,socket,time

urls = (
    '/', 'index'    
)

class index:
    def GET(self):
        i = web.input()
        ip=web.ctx.get('ip')
        visittime=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        data=''.join(['<ip>',ip,'</ip>',
                      '<time>',visittime,'</time>'
                      '<t>',i.t,'</t>',
                      '<j>',i.j,'</j>'])
        sock_notice.sendto(data,sendmail)
        sock_notice.sendto(data,login)
        return i

if __name__ == "__main__":
    sock_notice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendmail=('127.0.0.1',9876)
    login=('127.0.0.1',9875)
    app = web.application(urls, globals())
    app.run()
        
