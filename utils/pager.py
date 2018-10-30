class Pageinfo(object):
    def __init__(self,current_page,all_count,per_page,base_url,max_pages=5):
        try:
            self.current_page=int(current_page)
        except Exception as e:
            self.current_page=1
        self.per_page=per_page
        self.all_count=all_count
        self.max_pages=max_pages
        self.base_url=base_url
        a,b=divmod(all_count,per_page)
        if b:
            a+=1
        self.all_pages = a

    def start(self):
        return (self.current_page-1)*self.per_page
    def end(self):
        return self.current_page*self.per_page
    def pager(self):
        urls=[]
        half=int((self.max_pages-1)/2)
        if self.current_page<=half:
            begin=0
            stop=self.max_pages
        elif self.current_page+half>self.all_pages:
            begin=self.all_pages-self.max_pages
            stop=self.all_pages
        else:
            begin=self.current_page-half-1
            stop=self.current_page+half
        if self.current_page==1:
            pre = "<li class='page-item'> <a class='page-link' href='##pagerModel'>上一页</a></li>"
        else:
            pre = "<li class='page-item'> <a class='page-link' href='%s?page=%s#pagerModel'>上一页</a></li>" % (self.base_url,self.current_page - 1)
        urls.append(pre)
        for i in range(begin+1,stop+1):
            if i==self.current_page:
                url= "<li class='page-item active'> <a class='page-link active' href='%s?page=%s#pagerModel'>%s</a></li>"%(self.base_url,i,i)
            else:
                url = "<li class='page-item'> <a class='page-link' href='%s?page=%s#pagerModel'>%s</a></li>" % (self.base_url,i, i)
            urls.append(url)
        if self.current_page==self.all_pages:
            nex = "<li class='page-item'> <a class='page-link' href='##pagerModel'>下一页</a></li>"
        else:
            nex = "<li class='page-item'> <a class='page-link' href='%s?page=%s#pagerModel'>下一页</a></li>" % (self.base_url,self.current_page + 1)
        urls.append(nex)
        return ''.join(urls)