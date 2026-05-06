from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Content, DictionaryWord
import requests
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
        'dict_matches': [],
    })
def sozluk(request):
    query = request.GET.get('q')
    selected_level = request.GET.get('level')
    selected_type = request.GET.get('type')

    word_list = DictionaryWord.objects.all().order_by('word')

    if query:
        word_list = word_list.filter(word__icontains=query)
    if selected_level:
        word_list = word_list.filter(level=selected_level)
    if selected_type:
        word_list = word_list.filter(word_type=selected_type)

    paginator = Paginator(word_list, 20)
    page_number = request.GET.get('page')
    words = paginator.get_page(page_number)

    return render(request, 'stories/sozluk.html', {
        'words': words,
        'query': query,
        'selected_level': selected_level,
        'selected_type': selected_type,
    })


def fetch_word_api(request):
    word = request.GET.get('word', '').strip()
    if not word:
        return JsonResponse({'error': 'Kelime yok'}, status=400)

    result = {
        'word': word,
        'word_type': '',
        'definition_en': '',
        'example_sentence': '',
        'phonetic': '',
        'meaning_tr': ''
    }

    try:
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=5)
        if r.status_code == 200:
            data = r.json()[0]
            result['phonetic'] = data.get('phonetic', '')
            meanings = data.get('meanings', [])
            if meanings:
                m = meanings[0]
                result['word_type'] = m.get('partOfSpeech', '')
                defs = m.get('definitions', [])
                if defs:
                    result['definition_en'] = defs[0].get('definition', '')
                    result['example_sentence'] = defs[0].get('example', '')
    except Exception:
        pass

    try:
        r2 = requests.get(
            f'https://api.mymemory.translated.net/get?q={word}&langpair=en|tr',
            timeout=5
        )
        if r2.status_code == 200:
            result['meaning_tr'] = r2.json()['responseData']['translatedText']
    except Exception:
        pass

    return JsonResponse(result)