from django.db import models

# Create your models here.
class userInfo(models.Model):
    nickname=models.CharField(verbose_name="昵称",max_length=32,null=True,default="nameless")
    username=models.CharField(verbose_name="用户名", max_length=32,unique=True)
    password=models.CharField(verbose_name="密码", max_length=64)
    email=models.EmailField(verbose_name="邮箱")
    gender=models.IntegerField(verbose_name="性别",null=True,blank=True, default="0")
    presentation=models.CharField(verbose_name="个人说明",null=True,blank=True,max_length=240)
    avatar=models.ImageField(verbose_name="头像",default='/media/avatar/HP.jpg',upload_to='media/avatar')
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True,null=True)
    like_article=models.ManyToManyField("Article",through="UserArticle")
    like_msg=models.ManyToManyField("Message",through="UserMsg")
    like_comment=models.ManyToManyField("Comment",through="UserComment")

class Article(models.Model):
    type_choice = [(1, "心情随笔"),(2, "时光再忆"),(3, "分享给你")]
    title=models.CharField(verbose_name="标题",max_length=64)
    brief=models.CharField(verbose_name="简要",max_length=254)
    illustration=models.ImageField(verbose_name="插图",upload_to='illustration')
    video=models.FileField(verbose_name="视频",upload_to='videos',blank=True,null=True,default='')
    browse=models.IntegerField(default=0)
    like=models.IntegerField(default=0)
    comment=models.IntegerField(default=0)
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True,null=True)
    category=models.ForeignKey("Category",verbose_name="文章类型",null=True,choices=type_choice,on_delete=models.CASCADE)

class UserArticle(models.Model):
    user=models.ForeignKey("userInfo", on_delete=models.CASCADE)
    article=models.ForeignKey("Article", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)

class Article_detail(models.Model):
    content=models.TextField()
    art=models.OneToOneField("article",on_delete=models.CASCADE)

class Category(models.Model):
    title=models.CharField(verbose_name="分类标题", max_length=32)
    name=models.CharField(verbose_name="名称",max_length=32)

class Comment(models.Model):
    user=models.ForeignKey("userInfo",related_name="user",on_delete=models.CASCADE)
    content=models.TextField()
    reply=models.ForeignKey("Comment",null=True,blank=True,related_name="answer",on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True,null=True)
    article=models.ForeignKey("Article",null=True,blank=True,on_delete=models.CASCADE,related_name="comments")

class Message(models.Model):
    user = models.ForeignKey("userInfo", related_name="user_info", on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.ForeignKey("Message", null=True, blank=True, related_name="answer", on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True,null=True)

class UserMsg(models.Model):
    user=models.ForeignKey("userInfo", on_delete=models.CASCADE)
    article=models.ForeignKey("Message", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)

class UserComment(models.Model):
    user=models.ForeignKey("userInfo", on_delete=models.CASCADE)
    article=models.ForeignKey("Comment", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)