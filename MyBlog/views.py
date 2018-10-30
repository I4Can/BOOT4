from django.shortcuts import render, HttpResponse, redirect
from repository import models
import json
from utils import pager, visit
from django.db.models import Q
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from MyBlog import settings


# Create your views here.
def home(request):
    if request.method == 'GET':
        all_count = models.Article.objects.filter(category_id=3).all().count()
        per_page = 15
        max_page = all_count // per_page + 1
        if max_page >= 5:
            max_page = 5
        page_info = pager.Pageinfo(request.GET.get('page'), all_count, base_url='', per_page=per_page, max_pages=max_page)
        start = page_info.start()
        end = page_info.end()
        article_list = models.Article.objects.filter(Q(category_id=3)|Q(category_id=1)).order_by('-id')[start: end]
        result = {'article_list': article_list, 'page_info': page_info, }
        result = visit.visit(request, result)
        return render(request, 'home.html', result)
    else:
        return HttpResponse("404")

def check_username(requsts):
    ret = {'status': True, 'massage': None}
    username = requsts.POST.get('username')
    obj = models.userInfo.objects.filter(username=username)
    if obj:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def edit_info(request):
    if request.method == 'POST':
        ret = {'status': False, 'msg': '用户名或密码错误'}
        try:
            user_id = request.session.get("user_id")
            nickname = request.POST.get('nickname')
            presentation = request.POST.get('presentation')
            gender = request.POST.get('gender')
            avatar = request.FILES.get('avatar', )
            if (avatar):
                with open(os.path.join(BASE_DIR, 'media', 'avatar', avatar.name), 'wb+') as f:
                    for chunk in avatar.chunks():
                        f.write(chunk)
                models.userInfo.objects.filter(id=user_id).update(nickname=nickname, presentation=presentation,
                                                                  avatar='/media' + '/avatar/' + avatar.name,
                                                                  gender=gender)
            else:
                models.userInfo.objects.filter(id=user_id).update(nickname=nickname, presentation=presentation,
                                                                  gender=gender)
            ret['msg'] = "修改成功"
            ret['status'] = True
        except Exception as  e:
            ret['msg'] = str(e)
        return HttpResponse(json.dumps(ret))
