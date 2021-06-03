from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.forms import CommentForm
from taggit.models import Tag
# Create your views here.
def post_list_view(request,slug_tag=None):
    post_list=Post.objects.all()
    tag=None
    if slug_tag :
        tag=get_object_or_404(Tag,slug=slug_tag)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try :
        post_list=paginator.page(page_number)
    except PageNotAnInteger :
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})


from django.views.generic import ListView
class PostListView(ListView):
    model=Post
    paginate_by=1

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else :
        form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

from blog.forms import SendMailForm
from django.core.mail import send_mail
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=SendMailForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) Recomend\'s you to read post: {}'.format(cd['Name'],cd['Email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read the Post At : \n {} \n\n {} '.format(post_url,cd['comment'])
            send_mail(subject,message,cd['Email'],[cd['To']])
            sent=True
    else :
        form=SendMailForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})
