from django.shortcuts import render,redirect,get_object_or_404
from .models import Review,Comment
from django.views.decorators.http import require_http_methods,require_POST
from .forms import ReviewForm, CommentForm
# Create your views here.
def index(request):
    reviews = Review.objects.order_by('-pk')[0:5]
    context = {
        "reviews" : reviews
    }
    return render(request, 'community/index.html',context)


def reviews(request):
    reviews = Review.objects.all()
    context = {
        "reviews" : reviews
    }
    return render(request, 'community/reviews.html',context)


# @login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method =='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) # 당장 저장하지 않고 user 등록후 저장 
            review.user = request.user # accounts기능 완료후 필요 
            review.save()
            ## 데이터 모델링에서 user를 넣어놔서 
            # user필드가 비게되면 오류가 뜨기 때문에 accounts기능을 먼저 
            # 구현하거나 모델링을 수정해가면 할 필요가 있음...
            return redirect('community:index') # 추후에 detail로 수정필요 
    else:
        form = ReviewForm()
    context = {
        'form' : form ,
    }
    return render(request,'community/create.html',context)


def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


# @login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    # 수정하는 유저와, 게시글 작성 유저가 같은지 
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    # else:
    #     return redirect('articles:index') # request.user와 한묶음
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)


@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=pk)
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('community:detail', review.pk)



def comments_create(request,pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review,pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            print('&&&&',review.pk)
            return redirect('community:detail', review.pk)
        context = {
            'comment_form' : comment_form,
            'review':review,
        }            
        return render(request, 'community/detail.html',context)
    return redirect('accounts:login')



def comments_delete(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk = comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', review_pk)