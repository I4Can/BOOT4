from django.shortcuts import HttpResponse, render
from repository import models
import json
import re
import os
from MyBlog import settings
from utils import tree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def backend(request):
    if request.session.get('user_id') == 1:
        article_list = models.Article.objects.order_by('-id')
        category = models.Category.objects.all()
        return render(request, 'backend.html', {'article_list': article_list, 'category': category})


def sort_Article(request):
    if request.session.get('user_id') == 1:
        category_id = request.POST.get('category_id')
        category_id = int(category_id)
        sort = request.POST.get('sort')
        sort_way = request.POST.get('sort-way')
        if category_id != 0:
            obj = models.Article.objects.filter(category_id=category_id)
            article_list = obj.order_by('-id')
        else:
            article_list = models.Article.objects.order_by('-id')
        condition = sort.split('-')[0]
        if 'up' in sort_way:
            article_list = article_list.order_by(condition)
        elif 'down' in sort_way:
            article_list = article_list.order_by('-' + condition)
        category = models.Category.objects.all()
        if sort_way:
            sortWay = sort_way.split()[1]
        else:
            sortWay = None
        return render(request, 'backend.html',
                      {'article_list': article_list, 'category': category, 'category_id': category_id, 'sort': sort,
                       'sort_way': sort_way, 'sortWay': sortWay})


def delArticle(request):
    if request.session.get('user_id') == 1:
        ret = {'status': True, 'msg': None}
        if request.method == 'POST':
            try:
                ids = request.POST.get('id').split('/')[:-1]
                ret['ids'] = ids
                table = request.POST.get('type')
                for id in ids:
                    if 'edit_article' in table:                        
                        models.Comment.objects.filter(id=id).first().delete()
                    elif 'message' in table:
                        models.Message.objects.filter(id=id).first().delete()
                    else:
                        try:
                            pre_video = models.Article.objects.values('video').filter(id=id)[0]['video']
                            if pre_video!='':
                                pre_video_path = pre_video.split('#')
                                for video_path in pre_video_path:
                                        os.remove(video_path[1:])
                            pre_illustration = models.Article.objects.values('illustration').filter(id=id)[0]['illustration']
                            if pre_illustration != '':
                                pre_illustration_path = pre_illustration.split('#')
                                for illustration_path in pre_illustration_path:
                                    os.remove(illustration_path[1:])
                        except Exception as e:
                            print(str(e))
                        models.Article.objects.filter(id=id).first().delete()
            except Exception as e:
                ret['status'] = False
                ret['msg'] = str(e)
            return HttpResponse(json.dumps(ret))

def add_article(request):
    if request.session.get('user_id') == 1:
        if request.method == 'GET':
            category = models.Category.objects.all()
            return render(request, 'add_article.html', {'category': category})
        else:
            ret = {'status': True, 'msg': None}
            try:
                title = request.POST.get('title')
                content = request.POST.get('content')
                category_id = request.POST.get('category_id')
                brief = request.POST.get('brief')

                images = re.findall(r'<img src="([^"]*)?', content)
                for i in range(len(images)):
                    images[i] = images[i].split('"')[0]
                images_path = '#'.join(images)
                videos = re.findall(r'<video src="([^"]*)?', content)
                for i in range(len(videos)):
                    videos[i] = videos[i].split('"')[0]
                videos_path = '#'.join(videos)
                article = models.Article.objects.create(title=title, brief=brief, category_id=category_id,
                                                        illustration=images_path, video=videos_path)
                models.Article_detail.objects.create(content=content, art=article)

            except Exception as e:
                ret['status'] = False
                ret['msg'] = str(e)
            return HttpResponse(json.dumps(ret))

def edit_article(request):
    if request.session.get('user_id') == 1:
        if request.method == 'GET':
            id = request.GET.get('id')
            category_id = request.GET.get('cid')
            article_info = models.Article.objects.filter(id=id, category_id=category_id).first()
            comment = models.Comment.objects.filter(article_id=id).filter(reply=None).order_by('-id')
            comments_Tree = []
            for item in comment:
                single_tree = tree.preorder(root=item)
                comments_Tree.append(single_tree)
            category = models.Category.objects.all()
            like_user = models.UserArticle.objects.filter(article_id=id).all()
            if (article_info):
                return render(request, 'edit_article.html',
                              {'article_info': article_info, 'category': category, 'like_user': like_user,
                               'comment_tree': comments_Tree})
            else:
                return HttpResponse("别乱搞")
        else:
            ret = {'status': True, 'msg': None}
            try:
                title = request.POST.get('title')
                content = request.POST.get('content')
                category_id = request.POST.get('category_id')
                brief = request.POST.get('brief')
                id = request.POST.get('id')

                """从文本内容抓取src,并且和数据库比对,未使用的文件删除"""
                current_image = re.findall(r'<img src="([^"]*)?', content)
                for i in range(len(current_image)):
                    current_image[i] = current_image[i].split('"')[0]
                current_image_path = '#'.join(current_image)

                """从数据库抓取某元素某字段值"""
                pre_image = models.Article.objects.values('illustration').filter(id=id)[0]['illustration']
                pre_image_path = pre_image.split('#')
                for path in pre_image_path:
                    if path not in current_image and path != '':
                        os.remove(path[1:])

                current_video = re.findall(r'<video src="([^"]*)?', content)
                for i in range(len(current_video)):
                    current_video[i] = current_video[i].split('"')[0]
                current_video_path = '#'.join(current_video)
                pre_video = models.Article.objects.values('video').filter(id=id)[0]['video']
                pre_video_path = pre_video.split('#')
                for video_path in pre_video_path:
                    if video_path not in current_video and video_path != '':
                        os.remove(video_path[1:])

                models.Article.objects.filter(id=id).update(title=title, brief=brief, category_id=category_id,
                                                            illustration=current_image_path, video=current_video_path)
                models.Article_detail.objects.filter(art_id=id).update(content=content)
            except Exception as e:
                ret['status'] = False
                ret['msg'] = str(e)
            return HttpResponse(json.dumps(ret))


def message(request):
    if request.session.get('user_id') == 1:
        if request.method == 'GET':
            message_list = models.Message.objects.order_by('-id')
            return render(request, "backend_message.html", {'message_list': message_list})
    else:
        return HttpResponse("404")


def media(request):  # 后台上传图片和视频
    if request.session.get('user_id') == 1:
        if request.method == 'GET':
            return HttpResponse("OK")
        else:
            myFile = request.FILES  # 获取上传的文件，如果没有文件，则默认为None
            file_type = request.POST.get('file_type')
            urls = []
            if not myFile:
                return HttpResponse("no files for upload!")
            if file_type == 'video':
                path = 'videos'
            else:
                path = 'illustration'
            dir_path = os.path.join(settings.MEDIA_URL, path)
            file_num = len(os.listdir(dir_path))
            for k in myFile.keys():
                postfix = str(myFile[k]).split('.')[-1]
                back_path = '/' + dir_path  # 回显路径
                file_path = back_path + '/' + path + str(file_num + 1) + '.' + postfix
                while os.path.exists(file_path[1:]):    #如果存在就换个名字
                    file_num += 1
                    file_path = back_path + '/' + path + str(file_num + 1) + '.' + postfix
                urls.append(file_path)
                with open(os.path.join(BASE_DIR, file_path[1:]), 'wb+') as f:
                    for chunk in myFile[k].chunks():
                        f.write(chunk)
            return HttpResponse(json.dumps({"errno": 0, 'data': urls}))
