from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.models import User
import re


# function to get ip address
def getIp(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


# home page
def home(request):

    # Logging system: compare ips if user is authenticated (redirect page when a user registers or logins)
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            lastIp = request.user.userprofile.ipAddress
        else:
            lastIp = ""
        currentIp = getIp(request)

        if currentIp == lastIp:
            ipStat = "Safe IP"
        else:
            ipStat = "Warning: Different IP than usual"
    else:
        ipStat = getIp(request)
    # render the html passing ip info
    return render(request, "api/home.html", {"ipStat": ipStat})


# posts of last hour page
def posts(request):
    response = []
    # get time now
    this_hour = datetime.now()
    # -1 hour
    one_hour_before = this_hour - timedelta(hours=1)
    # filter posts
    posts = Post.objects.filter(datetime__range=(one_hour_before, this_hour))

    # building Json response
    for post in posts:
        response.append(
            {
                'title': post.title,
                'datetime': post.datetime,
                'content': post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId
            }
        )
    # return Json in the page
    return JsonResponse(response, safe=False)


# function that handles how feed is shown

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@csrf_exempt
@cache_page(CACHE_TTL)
def postList(request):

    # filter to show most recent post on top of page
    posts = Post.objects.filter().order_by('-datetime')

    # post form
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.datetime = datetime.now()

            # Uncomment below if you want all posts validated on block chain
            # post.writeOnChain()

            post.save()
            cache.clear()
            form = PostForm()
        return redirect('/postList', {'posts': posts, 'form': form})
    else:
        form = PostForm()
        return render(request, 'api/postList.html', {'posts': posts, 'form': form})


# Analytics page | only superuser can access | passing number of posts
def analytics(response):
    userPosts = User.objects.annotate(total_posts=Count('post'))
    return render(response, "api/analytics.html", {"userPosts": userPosts})


# page /user/<int:_id>/ showing some info for each user (try id: 1 , 20 , 21)
def userId(request, _id):
    user = get_object_or_404(User, id=_id)
    userPosts = Post.objects.filter(user=user).count()
    return render(request, 'api/user_id.html', {'user': user, "userPosts": userPosts})


# /wordCheck?q=<GET> endpoint check with GET number of times a word is present in posts
def wordCheck(request):
    r = request.GET.get('q', '')
    posts = Post.objects.filter().order_by('-datetime')
    resp = 0
    for post in posts:
        print(r)
        wordList = re.sub("[^\w]", " ", post.content).split()
        if post.title == r or r in wordList:
            resp += 1
    # return message on page
    return HttpResponse(f'The word {r} appears {resp} times in all posts')



