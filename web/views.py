from repository import models
from utils import pager,visit,tree
from django.db.models import F
from django.shortcuts import render,HttpResponse,redirect
import json
from datetime import datetime

def sign(request):
    if request.method=='GET':
        return render(request,'Sign.html')
    else:
        ret={'status':False,'msg':'用户名或密码错误' }
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            obj = models.userInfo.objects.filter(username=username, password=password).first()
            if obj:
                request.session.flush()
                request.session['username'] = obj.username
                request.session['user_id'] = obj.id
                request.session.set_expiry(60 * 60 * 24 * 30)
                ret['msg']="登录成功"
                ret['status']=True
        except Exception as  e:
            ret['msg']=str(e)
        return HttpResponse(json.dumps(ret))

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            models.userInfo.objects.create(username=username, password=password, email=email)
            """
                传到后台
                ORM
                返回登陆页面
            """
            obj = models.userInfo.objects.filter(username=username, password=password).first()
            request.session['username'] = obj.username
            request.session['user_id'] = obj.id
        except Exception as e:
            return HttpResponse(json.dumps(str(e)))
        return render(request,'success.html')


def jottings(request):
    if request.method=='GET':
        all_count = models.Article.objects.filter(category_id=1).all().count()
        per_page = 15
        max_page = all_count // per_page + 1
        if max_page >= 5:
            max_page = 5
        page_info = pager.Pageinfo(request.GET.get('page'), all_count, base_url='/jottings/', per_page=per_page,
                                   max_pages=max_page)
        start = page_info.start()
        end = page_info.end()
        article_list = models.Article.objects.filter(category_id=1).order_by('-id')[start: end]
        result = {'article_list': article_list, 'page_info': page_info, }
        result = visit.visit(request, result)
        return render(request, 'sharing.html', result)
    else:
        return HttpResponse("404")

def recall(request):
    if request.method=='GET':
        recall_list = models.Article.objects.filter(category_id=2).order_by('-create_time')
        time_table = {}
        for item in recall_list:
            year = item.create_time.strftime('%Y')
            year_month = item.create_time.strftime('%Y-%m')
            if year in time_table.keys():
                pass
            else:
                time_table[year] = {}
            if year_month.split('-')[0] in time_table.keys():
                if year_month.split('-')[1] not in time_table[year_month.split('-')[0]].keys():
                    time_table[year_month.split('-')[0]][year_month.split('-')[1]] = [item]
                else:
                    time_table[year_month.split('-')[0]][year_month.split('-')[1]].append(item)
        return render(request, "recall.html", {'recall_list': time_table})
    else:
        return HttpResponse("404")

def message(request):
    if request.method=='GET':
        comment = models.Message.objects.filter(reply=None).order_by('-id')
        comments_Tree = []
        for item in comment:
            single_tree = tree.preorder(root=item)
            comments_Tree.append(single_tree)
        all_count = len(comments_Tree)
        per_page = 15
        max_page = all_count // per_page + 1
        if max_page >= 5:
            max_page = 5
        page_info = pager.Pageinfo(request.GET.get('page'), all_count, base_url='/message/', per_page=per_page,
                                   max_pages=max_page)
        start = page_info.start()
        end = page_info.end()
        message_list = comments_Tree[start: end]
        user_id = request.session.get('user_id')
        result = {'message_list': message_list, 'page_info': page_info, 'user_id': user_id}
        result = visit.visit(request, result)
        return render(request, 'message.html', result)
    else:
        return HttpResponse("404")


def share(request):
    if request.method=='GET':
        all_count = models.Article.objects.filter(category_id=3).all().count()
        per_page=15
        max_page=all_count//per_page+1
        if max_page>=5:
            max_page=5
        page_info = pager.Pageinfo(request.GET.get('page'), all_count, base_url='/share/', per_page=per_page,max_pages=max_page)
        start = page_info.start()
        end = page_info.end()
        article_list = models.Article.objects.filter(category_id=3).order_by('-id')[start: end]
        result = {'article_list': article_list, 'page_info': page_info, }
        result = visit.visit(request, result)
        return render(request, 'sharing.html', result)
    else:
        return HttpResponse("404")

def about(request):
    if request.method == 'GET':
        return render(request,"about.html")
    else:
        return HttpResponse("404")


def like(request):
    if request.method=='POST':
        try:
            user_id = request.session.get('user_id')
            if user_id:
                article_id = request.POST.get('article_id').split('_')[1]
                path= request.POST.get('path')
                if path=='message':
                    current=models.UserMsg.objects.filter(article_id=article_id, user_id=user_id).first()
                    if current:
                        current.delete()
                    else:
                        models.UserMsg.objects.create(article_id=article_id, user_id=user_id)
                    obj = models.Message.objects.filter(id=article_id)
                    num= obj.first().userinfo_set.all().count()
                    obj.update(like=num)
                elif path=='blog':
                    current=models.UserComment.objects.filter(article_id=article_id, user_id=user_id).first()
                    if current:
                        current.delete()
                    else:
                        models.UserComment.objects.create(article_id=article_id, user_id=user_id)
                    obj = models.Comment.objects.filter(id=article_id)
                    num = obj.first().userinfo_set.all().count()
                    obj.update(like=num)

                else:
                    current=models.UserArticle.objects.filter(article_id=article_id, user_id=user_id).first()
                    if current:
                        current.delete()
                    else:
                        models.UserArticle.objects.create(article_id=article_id, user_id=user_id)
                    obj = models.Article.objects.filter(id=article_id)
                    num = obj.first().userinfo_set.all().count()
                    obj.update(like=num)
            else:
                return HttpResponse("未登录")
        except Exception as e:
            return HttpResponse(json.dumps(str(e)))
        return HttpResponse(json.dumps({'like':num}))
    else:
        return HttpResponse("404")

def receive_comment(request):
    if request.method=='POST':
        try:
            article_id = request.POST.get('article_id')
            reply_id = request.POST.get('reply_id')
            if reply_id:
                reply_id = reply_id.split('_')[1]
            content = request.POST.get('content')
            user_id = request.session.get('user_id')
            if (article_id):
                models.Comment.objects.create(content=content, user_id=user_id, reply_id=reply_id, article_id=article_id)
                models.Article.objects.filter(id=article_id).update(comment=F('comment') + 1)
                return redirect('/blog/'+article_id+'.html#pagerModel')
            else:
                obj=models.Message.objects.create(content=content, user_id=user_id, reply_id=reply_id)
            id=obj.id
            create_time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
            nickname=obj.user.nickname
            if obj.reply:
                reply_nickname=obj.reply.user.nickname
                result={'id':id, 'nickname':nickname,'create_time':create_time,'reply_nickname':reply_nickname}
            else:
                result={'id':id, 'nickname':nickname,'create_time':create_time,}
        except Exception as e:
            return HttpResponse(json.dumps(str(e)))
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse("404")

def show_article(request,article_id):
    if request.method=='GET':
        try:
            models.Article.objects.filter(id=article_id).update(browse=F('browse')+1)
            article_info=models.Article.objects.filter(id=article_id).exclude(category_id=2).first()
            if not article_info:
                return HttpResponse("找不到啦")
            # nex_article = article_info.get_next_in_order()
            # pre_article = article_info.get_previous_in_order()
            # category_id=article_info.category_id
            comment = models.Comment.objects.filter(article_id=article_id).filter(reply=None).order_by('-id')
            comments_Tree = []
            for item in comment:
                single_tree = tree.preorder(root=item)
                comments_Tree.append(single_tree)
            all_count = len(comments_Tree)
            per_page = 15
            max_page = all_count // per_page + 1
            if max_page >= 5:
                max_page = 5
            page_info = pager.Pageinfo(request.GET.get('page'), all_count, base_url='/message/', per_page=per_page,
                                       max_pages=max_page)
            start = page_info.start()
            end = page_info.end()
            message_list = comments_Tree[start: end]
            user_id=request.session.get('user_id')

            result = {'message_list': message_list, 'page_info': page_info, 'article_info':article_info,'user_id':user_id,}
            result = visit.visit(request, result)
        except Exception as e:
            return HttpResponse(str(e))
        return render(request,'show_article.html',result)
    else:
        return HttpResponse("404")


def status(request):
    if request.method=='GET':
        ret = {'login': True}
        if not request.session.get('username'):
            ret['login'] = False
        return HttpResponse(json.dumps(ret))
    else:
        request.session.flush()
        return HttpResponse('OK')