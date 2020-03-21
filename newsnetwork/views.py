from django.shortcuts import render, get_object_or_404
from .forms import *
# Create your views here.
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def logout(request):
    _logout(request)
    return HttpResponseRedirect('/signup')


def main(request):
    return HttpResponse('OK')


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            auth = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            _login(request, auth)
            return HttpResponseRedirect('/')
    templ = 'signup.html'
    return render(request, 'base.html',
                  {
                      'templ': templ,
                      'actionPath': request.path,
                      'form': form
                  })


def postshow(request, id):
    post = get_object_or_404(PostModel, id=id)
    print(not request.user.is_superuser)
    if post.moderated == False:
        if (request.user != post.author) and (not request.user.is_superuser):
            raise Http404('post not found')
    return render(request, 'base.html', context={
        'post': post,
        'templ': 'post.html'
    })


@login_required
def addNews(request):
    if request.method == 'POST':
        form = AddNewsForm(request.user, data=request.POST,
                           files=request.FILES)
        val = form.is_valid()
        print(val)
        if val:
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
        return HttpResponseRedirect(request.path)

    form = AddNewsForm()

    templ = 'addNews.html'
    return render(request, 'base.html', {
        'form': form,
        'templ': templ,
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

    templ = 'login.html'
    return render(request, 'base.html',
                  {
                      'templ': templ,
                      'actionPath': request.path,
                      'form': form
                  })
