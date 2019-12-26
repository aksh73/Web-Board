# from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import NewTopicForm, PostForm
from .models import Board,Topic, Post
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.views.generic import UpdateView,ListView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def home(request):
    boards=Board.objects.all()
    return render(request,'boards/home.html',{'boards':boards})
# below is the GCBV implementation of the home page
# class BoardListView(ListView):
#     model = Board
#     context_object_name = 'boards'
#     template_name = 'boards/home.html'

# FBV implementation of Pagination
def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    # Board.objects.get(pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 15)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request,'boards/topics.html' , {'board':board,'topics':topics})

@login_required
def new_topic(request,pk):
    board=get_object_or_404(Board,pk=pk)
    # user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return HttpResponseRedirect(reverse('topic_posts', args=(pk,topic.pk)))

    else:
        form=NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})

# @login_required
def topic_posts(request,pk,topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})

# @login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()  
            topic.save()

            # topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            # topic_post_url = '{url}?page={page}#{id}'.format(
            #     url=topic_url,
            #     id=post.pk,
            #     page=topic.get_page_count()
            # )

            return HttpResponseRedirect(reverse('topic_posts',args=(pk,topic_pk)))

    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})

# below is generic class-based view
@method_decorator(login_required, name='dispatch')             # stop unauthorized users to gain access to edit page
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):                # to avoid accessing edit post option by other users
        queryset = super().get_queryset()
        return queryset.filter(created_by = self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return HttpResponseRedirect(reverse('topic_posts',args=(post.topic.board.pk, post.topic.pk)))

def delete_post(request,pk,topic_pk, post_pk):
    template = 'boards/delete_post.html'
    topics = get_object_or_404(Topic ,board__pk=pk, pk=topic_pk)
    post = topics.posts.get(pk=post_pk)
    post.save()
    post.delete()
    return HttpResponseRedirect(reverse('topic_posts',args=(post.topic.board.pk, post.topic.pk)))

# Pagination using GCVB
@method_decorator(login_required, name='dispatch')             # stop unauthorized users to gain access to edit page
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset



    # if request.method == 'POST':
    #     subject = request.POST['subject']
    #     message = request.POST['message']
    #     user = User.objects.first()   # to get the currently logged in user
    #
    #     topic = Topic.objects.create(subject=subject, board=board, starter = user)
    #     post = Post.objects.create(
    #         message=message,
    #         topic=topic,
    #         created_by=user
    #     )
    #     # return redirect('board_topics', pk=board.pk)  # redirect to the created topic page
    #     return render(request,'boards/topics.html' , {'board':board})
    # return render(request,'boards/new_topic.html', {'board': board})
