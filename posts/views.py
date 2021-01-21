from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect,reverse
from .models import Post, Author, PostView
from marketing.models import Singup
from .forms import CommentForm, PostForm

def get_user(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None

def search(request):
	queryset = Post.objects.all()
	query    = request.GET.get('q')
	if query:
		queryset = queryset.filter(
			Q(title__icontains=query) |
			Q(overview__icontains=query)
		).distinct()
		context = {'queryset' : queryset}
		return render(request, 'search_result.html', context)


def get_category_count():
	queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
	return queryset

def index(request):
	featured = Post.objects.filter(featured=True)
	latest = Post.objects.order_by('-timestamp')[:3]
	
	if request.method == 'POST':
		email = request.POST['email']
		new_singup = Singup()
		new_singup.email = email
		new_singup.save()

	context  = {'object_list' : featured, 'latest' : latest} 
	return render(request, 'index.html', context)

def blog(request):
	category_count = get_category_count()
	# print(category_count)
	most_recent = Post.objects.order_by('-timestamp')
	queryset  = Post.objects.all()
	paginator = Paginator(queryset, 2)
	page_request_var = 'page'
	page      = request.GET.get(page_request_var)

	try:
		paginate_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginate_queryset = paginator.page(1)
	except EmptyPage:
		paginate_queryset = paginator.page(paginator.num_pages)
 
	context = {
		'most_recent' : most_recent,
		'queryset' : paginate_queryset,
		'page_request_var': page_request_var,
		'category_count': category_count,
		}
	return render(request, 'blog.html', context)

def post(request, id):
	post = get_object_or_404(Post, id = id)
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-timestamp')	
	
	if request.user.is_authenticated:
		PostView.objects.get_or_create(user=request.user, post=post)

	form = CommentForm(request.method == 'POST' or None)
	if request.method == "POST":
		if form.is_valid():
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect(reverse('post-detail', kwargs= {
				'id': post.id
			}))

	context = {
		'form': form,
		'post': post,
		'most_recent' : most_recent,
		'category_count': category_count,
		}
	return render(request, 'post.html', context)

def post_create(request):
	title = 'Create'
	form = PostForm(request.POST or None, request.FILES or None)
	author = get_user(request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.instance.author = author
			form.save()
			return redirect(reverse('post-detail', kwargs={
				'id': form.instance.id
			}))
			
	context = {
		'title' : title,
		'form': form
		}
	return render(request, 'post_create.html', context)

def post_update(request, id):
	title = 'Update'
	post = get_object_or_404(Post, pk = id)
	form = PostForm(request.POST or None, request.FILES or None, instance=post)
	author = get_user(request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.instance.author = author
			form.save()
			return redirect(reverse('post-detail', kwargs={
				'id': form.instance.id
			}))
		
	context = {
		'title' : title,
		'form': form
	}
	return render(request, 'post_create.html', context)

def post_delete(request, id):
	post = get_object_or_404(Post, id=id)
	post.delete()
	return redirect(reverse('post-list'))

