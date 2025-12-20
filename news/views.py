from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import NewsArticle


def news_list_view(request):
    today = timezone.now().date()
    articles = NewsArticle.objects.filter(
        published=True
    ).exclude(
        expiry_date__lt=today
    ).order_by('-date_entered')
    
    return render(request, 'news/news_list.html', {'articles': articles})


def news_detail_view(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, published=True)
    article.view_count += 1
    article.save(update_fields=['view_count'])
    
    return render(request, 'news/news_detail.html', {'article': article})

def guide_dog(request):
    return render(request, 'news/guidedog.html')

def guide_puppy(request):
    return render(request, 'news/guidepuppy.html')

def guide_cat(request):
    return render(request, 'news/guidecat.html')

def guide_kitten(request):
    return render(request, 'news/guidekitten.html')