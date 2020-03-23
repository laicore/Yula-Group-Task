from django.shortcuts import render, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

# Create your views here.


@login_required
def logout(request):
    _logout(request)
    return HttpResponseRedirect('/signup')


def loadNews(request):

    limit = 3
    queryPosts = PostModel.objects.new()
    paginator = Paginator(queryPosts, limit)
    getPage = request.GET.get('page', 1)
    def postsDetail(i): return {
        'name': page[i].name, 'url': page[i].get_url()}
    try:
        page = paginator.page(getPage)
        posts = {x: postsDetail(x) for x in range(len(page))}
        form = {'status': 'ok', 'data': posts}
    except:
        form = {'status': 'warning', 'warn': 'контент закончился'}

    return HttpResponse(json.dumps(form, indent=4))


def main(request):

    return render(request, 'base.html', {
        'templ': 'main.html'
    })


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            auth = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            _login(request, auth)
            return HttpResponseRedirect('/')
    return render(request, 'base.html',
                  {
                      'templ': 'signup.html',
                      'actionPath': request.path,
                      'form': form
                  })


def postshow(request, id):
    post = get_object_or_404(PostModel, id=id)
    if post.moderated == False:
        if (request.user != post.author) and (not request.user.is_superuser):
            raise Http404('post not found')
    return render(request, 'base.html', context={
        'post': post,
        'templ': 'post.html'
    })


@login_required
def profile(request):
    user = request.user
    userPosts = PostModel.objects.filter(author=user)
    form = {'user': user, 'userPosts': userPosts}
    return render(request, 'base.html', {
        'form': form,
        'templ': 'profile.html'
    })


@login_required
def addNews(request):
    form = AddNewsForm(request.user or None,
                       data=request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)

    return render(request, 'base.html', {
        'form': form,
        'templ': 'addNews.html',
        'actionPath': request.path
    })


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            auth = authenticate(**form.save())
            _login(request, auth)
            return HttpResponseRedirect('/')

    return render(request, 'base.html',
                  {
                      'templ': 'login.html',
                      'actionPath': request.path,
                      'form': form
                  })
