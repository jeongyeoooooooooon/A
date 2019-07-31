from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator #페이지네이션 임폴트 해줘야함
from .models import Blog
from .form import BlogPost

def home(request):
    blogs = Blog.objects.all().order_by('-id')
    #블로그의 모든 글들 대상으로
    blog_list = Blog.objects.all().order_by('-id')
    #블로그 객체 세 개를 한 페이지로 자르기
    paginator = Paginator(blog_list, 3)
    #request된 페이지가 뭔지를 알아내고 (request페이지를 변수에 담아내고)
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 해준다.
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs': blogs, 'posts':posts})

def detail(request, blog_id):
    blog_details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'details':details})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))
    
def blogpost(request):
#1. 입력된 내용을 처리하는 기능 -> post
    if request.method =='POST':
        form = BlogPost(request.POST)
        if form.is_valid():                 #잘 입력되었는지 검사하는 함수is_valid(): 함수
            post = form.save(commit=False)  #모델 객체를 반환 하돼 아직 저장하지 말아라
            post.pub_date=timezone.now()    #폼에서 입력하지 않은 시간을 여기 함수에서 대신 입력한다.
            post.save()                     #저장 한다.
            return redirect('home')         #저장하고 다시 홈을 띄워라

#2. 빈 페이지를 띄워주는 기능 ->GET
    else:
        form = BlogPost()
        return render(request,'new.html',{'form':form})