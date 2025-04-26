from django.shortcuts import render, redirect
from django.contrib import messages
from .models import News

def news(request):
    if request.method == 'POST':
        if not (request.user.is_authenticated and request.user.is_staff):
            messages.error(request, 'Только администраторы могут управлять новостями.')
            return redirect('news')

        # Добавление новости
        if 'title' in request.POST and 'content' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                News.objects.create(title=title, content=content)
                messages.success(request, 'Новость добавлена!')
            else:
                messages.error(request, 'Заполните все поля.')
            return redirect('news')

        # Удаление новости
        if 'delete' in request.POST:
            news_id = request.POST.get('delete')
            try:
                news_item = News.objects.get(id=news_id)
                news_item.delete()
                messages.success(request, 'Новость удалена!')
            except News.DoesNotExist:
                messages.error(request, 'Новость не найдена.')
            return redirect('news')

    # Получаем последние 10 новостей, отсортированных по убыванию даты создания (новые сверху)
    news_items = News.objects.all().order_by('-created_at')[:10]
    return render(request, 'news.html', {'news': news_items})