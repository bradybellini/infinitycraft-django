from django.shortcuts import render
from django.views import generic

from .models import Post
# Create your views here.

def home(request):
    return render(request, 'index.html')
    
    
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'