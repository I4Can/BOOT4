from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
class userLogin(MiddlewareMixin):
    def process_request(self,request):
        print(request.session.get('user_id'))
        if request.path in need_login:
            if request.session.get('user_id')!=2:
                return HttpResponse("权限不足，不可登入")