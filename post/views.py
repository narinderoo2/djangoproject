from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,HttpResponseRedirect
from django.contrib import messages,auth
from .models import News,Comment,Contact,Message
from django.utils import timezone
from .form import CommentForm
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required


def home(request):

    news = News.objects.all().order_by('-news_id')
    news1 = News.objects.all().order_by('-news_id')[4:10]
    news2 = News.objects.all()


    if request.method == 'POST':
        username = request.POST['username']
        uemail= request.POST['uemail']
        umessage= request.POST['umessage']
        contact1 = Message(name=username, email=uemail, message=umessage)
        contact1.save()
        return redirect('home')

    add1 = {'news': news,
            'news1':news1,
            'news2':news2,
            }
    return render(request, 'home.html',add1)


#===============================Search Function ========================================

# @login_required(login_url='/login')
def contact(request):
    if request.method == 'POST':
        username = request.POST['username']
        uemail= request.POST['uemail']
        upassword= request.POST['upassword']
        repassword= request.POST['repassword']
        uphone= request.POST['uphone']

        if not username.isalnum():
            messages.error(request,"not opertor are use")
            return redirect('contact')

        if upassword != repassword:
            messages.error(request,"Passwords do not match")
            return redirect('contact')

        contact1 = User.objects.create_user(username=username, password=upassword, email=uemail)
        # Any user submit info. admin panel User, so this method can use it
        contact1.save()

        contact2 = Contact(Name=username,Password=upassword, Email=uemail,Re_Password=repassword,Phone=uphone)
        # all data save in contact
        contact2.save()

        messages.success(request, 'you are now registered & can login')
        return redirect('login')
    return render(request, 'contact.html')


#===============================Log In  Function ========================================
def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password= request.POST['upassword']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
            messages.success(request, 'Successfully Logged In ')
        else:
            messages.error(request, 'Invalid data, Please correct data submit ')
            return redirect('login')

    return render(request, 'login.html')


#===============================Log Out Function { not create html page } ========================================

def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully log out')
    return redirect('login')

# def postpage(request, id):
#     post = get_object_or_404(News, news_id=id)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             m = form.save(commit=False)
#             m.post_id = post
#             m .save()
#             return redirect('postpage', id=post.news_id)
#     else:
#         form = CommentForm()

#     add= {'post':post, 'form': form}
#     return render(request, 'postpage.html',add)

#===============================Postpage Function( All pages link of this page) ========================================

# def postpage(request, title ):
#     title = title.replace('-',' ')
#     post = get_object_or_404(News, title=title)
#     post2 = News.objects.all().order_by('-pub_date')
#     news2 = News.objects.all().filter(heading0='it')
#     if request.method == "POST":
#         msg1 = request.POST['msg0']
#         cmt =Comment(post_id=post, msg=msg1)
#         cmt.save()
#
#         return redirect('postpage', title=post.title)
#
#     add= {'post':post,
#           'post2': post2,
#           'news2':news2,}
#     return render(request, 'postpage.html',add)

def postpage(request, title ):
    title = title.replace('-',' ')
    post = get_object_or_404(News, title=title)
    post2 = News.objects.all().order_by('-pub_date')
    news2 = News.objects.all().filter(heading0='it')
    comments = Comment.objects.filter(post_id=post,  reply=None)
    if request.method == "POST":
        msg1 = request.POST['msg0']
        msg_name = request.POST['user_name']
        com_id = request.POST.get('reply_id')
        comment_as = None
        if com_id:
            comment_as = Comment.objects.get(id = com_id)
        cmt = Comment(post_id=post, msg=msg1, user_name=msg_name, reply=comment_as)
        cmt.save()
        if post.title != title:
            return redirect('postpage', title=post.title)
        else:
            pass
             # return redirect('postpage', title=post.title)


    add= {'post':post,
          'post2': post2,
          'news2':news2,
          'comments': comments,}
    return render(request, 'postpage.html',add)

#===============================Search Function( Dilog box ) ========================================

def search(request):
    query = request.GET['query']
    news2 = News.objects.all().order_by('-pub_date')[:5]
    if len(query) > 50:
        search1 = News.objects.none()
    else:
        search1title = News.objects.filter(title__icontains=query)
        search1post0 = News.objects.filter(post0__icontains=query)
        search1 = search1title.union(search1post0)

    paginator = Paginator(search1,4)  #pagination start in search page
    page_number = request.GET.get('page')
    search1 = paginator.get_page(page_number)

    content = {'search1': search1,
               'query': query,
               'news2':news2,
               'values': request.GET}
    return render(request, 'search.html', content)


#==================================About Fuction( It is only Html page ) ==================================
def about(request):
    news2 = News.objects.all()
    return render(request, 'about.html',{'news2':news2})


#==Error page ( Any user put wrong keyword in website url, so this is alert the user)========================
def error_404_view(request,exception):
    data1 = {"name":"ThepythonDjango.com"}
    return render(request,'error_404.html', data1)




##=========================Down side all pages of website =======================================================

##==========================It page==========================================================

def it(request):
    news2 = News.objects.all().filter(heading0='it')
    it1 = News.objects.filter(heading0='it').order_by('-news_id')
    return render(request, 'page/it.html', {'it1': it1 ,
                                            'news2':news2})


#===========================Python page===================================================

def python(request):
    news2 = News.objects.all().filter(heading0='python')
    python1 =News.objects.filter(heading0='python').order_by('-news_id')
    paginator = Paginator(python1,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'page/Python.html', {'python1': python1,
                                                'page_obj': page_obj,
                                                'news2':news2})


#==============================Web devloper page=================================================

def webdevloper(request):
    news2 = News.objects.all().filter(heading0='gaming')
    web1 =News.objects.filter(heading0='python').order_by('-news_id')
    return render(request, 'page/Webdevloper.html',{ 'web1':web1,
                                                     'news2':news2 })


#===========================Tkinter page===================================================

def tkinter(request):
    news2 = News.objects.all().filter(heading0='tkinter')
    tk1 =News.objects.filter(heading0='tkinter').order_by('-news_id')
    return render(request, 'page/Tkinter.html',{ 'tk1':tk1,
                                                 'news2':news2})


#===========================Django page==================================================

def django(request):
    news2 = News.objects.all().filter(heading0='django')
    dj1 =News.objects.filter(heading0='django').order_by('-news_id')
    return render(request, 'page/Django.html',{ 'dj1': dj1 ,
                                                'news2':news2})


#============================Gaming page===================================================

def gaming(request):
    news2 = News.objects.all().filter(heading0='gaming')
    game1 =News.objects.filter(heading0='gaming').order_by('-news_id')
    return render(request, 'page/Gaming.html',{ 'game1': game1 ,
                                                'news2':news2})
