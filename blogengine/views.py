import datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext, HttpResponse
from blogengine.forms import UserForm, UserProfileForm, AddPostForm
from blogengine.models import Post
# Create your views here.
@csrf_protect
def register(request):

	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			registered = True
		
		else:
			print user_form.errors, profile_form.errors
			
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response('blog/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},context)


@csrf_protect
def user_login(request):

	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
			
		if user:
            	
			if user.is_active:
				login(request, user)
					#posts = Post.objects.all().filter(post__author=name)
				return HttpResponseRedirect('/blog/1/')
			else:
				return HttpResponse("Your Blogengine account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('blog/login.html', {}, context)


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/blogengine/')



@login_required
def personalised_view(request, selected_page=1):
	context = RequestContext(request)
	client = User.objects.get(username = request.user)
	name = User.get_full_name(client)
	posts = Post.objects.all().filter(author__username = client.username)
	#posts = posts.order_by('-pub_date')
	pages = Paginator(posts, 5)

    # Get the specified page
	try:
		returned_page = pages.page(selected_page)
	except EmptyPage:
		returned_page = pages.page(1)
	return render_to_response('blog/homepage.html',{ 'client': name , 'posts':returned_page.object_list, 'page':returned_page }, context)	



def public_view(request):
	context = RequestContext(request)
	posts = Post.objects.all()[:5]

	return render_to_response('blog/first_page.html',{ 'posts': posts}, context)

def singlePost(request, postUrl):
	#print postUrl
	context = RequestContext(request)
	blogpost = Post.objects.get(url = postUrl)
	#print blogpost.url
	return render_to_response('blog/single.html', { 'posts': blogpost , }, context)

@login_required
def addPost(request):
	context = RequestContext(request)
	posted = False

	if request.method == 'POST':
		
		newPost = Post()
		newPost.title = request.POST['title']
		newPost.url = request.POST['url']
		newPost.author = request.user
		newPost.pub_date = datetime.datetime.now()
		newPost.body = request.POST['content']
		print newPost.body
		newPost.views = 0;
		titles = Post.objects.all().filter(title = request.POST['title'])
		if titles:
			return HttpResponse("The title is already is use")
		else:
			newPost.save()
			posted = True
			#return HttpResponseRedirect('/blog/')
			
	
	return render_to_response('blog/rand.html', {'posted': posted}, context)

def about(request):
	context = RequestContext(request)

	return render_to_response('blog/about.html',{},context)

@login_required
def profile(request):
	context = RequestContext(request)
	user = User.objects.get(username=request.user)
	context_dict = {}
	try:
		user_profile = UserProfile.objects.get(user=u)
	except:
		user_profile = None

	context_dict['user'] = user
	context_dict['userprofile'] = user_profile
	return render_to_response('blog/profile.html', context_dict, context)