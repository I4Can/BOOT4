from repository import models
def visit(request, result):
    visit = request.session.get('username')
    if (visit):
        if request.path.split('/')[1]=='blog':
            like_list = models.userInfo.objects.filter(
                id=request.session.get('user_id')).first().like_comment.all()  # 不能用[start:end]
        elif request.path.split('/')[1]=='message':
            like_list = models.userInfo.objects.filter(
                id=request.session.get('user_id')).first().like_msg.all()  # 不能用[start:end]
        else:
            like_list = models.userInfo.objects.filter(
                id=request.session.get('user_id')).first().like_article.all()  # 不能用[start:end]
        ids = []
        for item in like_list:
            ids.append(item.id)
        result['ids'] = ids
    return result
