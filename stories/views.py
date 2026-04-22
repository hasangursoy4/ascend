from django.shortcuts import render, get_object_or_404
from .models import Content
import re

CATEGORY_LABELS = {
    'series': 'Diziler',
    'movie': 'Filmler',
    'animation': 'Animasyon',
    'game': 'Oyunlar',
}

def index(request):
    cat_name = request.GET.get('level') 
    if cat_name:
        contents = Content.objects.filter(category__iexact=cat_name)
    else:
        contents = Content.objects.all()
    return render(request, 'stories/index.html', {'contents': contents})

def category_page(request, category):
    contents = Content.objects.filter(category=category)
    label = CATEGORY_LABELS.get(category, category)
    return render(request, 'stories/category.html', {
        'contents': contents,
        'category': category,
        'category_label': label,
    })

def story_detail(request, story_id):
    content = get_object_or_404(Content, id=story_id)
    level = request.GET.get('ver', 'A1') 
    selected_version = content.versions.filter(level=level).first()

    highlighted_en = None
    if selected_version:
        text = selected_version.text_en
        vocabs = selected_version.vocabularies.all()
        for vocab in vocabs:
            word = vocab.word
            meaning = vocab.meaning
            # Slug: özel karakterleri temizle
            slug = re.sub(r"[^a-z0-9]+", '-', word.lower()).strip('-')
            pattern = re.compile(r'\b(' + re.escape(word) + r')\b', re.IGNORECASE)
            replacement = (
                f'<span class="vocab-highlight" '
                f'data-meaning="{meaning}" '
                f'data-slug="{slug}">'
                f'\\1</span>'
            )
            text = pattern.sub(replacement, text)
        highlighted_en = text

    return render(request, 'stories/story_detail.html', {
        'content': content,
        'selected_version': selected_version,
        'current_level': level,
        'highlighted_en': highlighted_en,
        'levels': ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
        'level_desc': {'A1': 'Başlangıç', 'A2': 'Temel', 'B1': 'Orta Öncesi', 'B2': 'Orta', 'C1': 'İleri', 'C2': 'Uzman'},
    })