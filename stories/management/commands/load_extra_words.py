import time
import requests
import random
from django.core.management.base import BaseCommand
from stories.models import DictionaryWord
from english_words import get_english_words_set

def fetch_definition(word):
    try:
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=5)
        if r.status_code == 200:
            data = r.json()[0]
            phonetic = data.get('phonetic', '')
            meanings = data.get('meanings', [])
            if meanings:
                m = meanings[0]
                word_type = m.get('partOfSpeech', '')
                defs = m.get('definitions', [])
                if defs:
                    return phonetic, word_type, defs[0].get('definition',''), defs[0].get('example','')
    except: pass
    return '', '', '', ''

def fetch_translation(word):
    try:
        r = requests.get(f'https://api.mymemory.translated.net/get?q={word}&langpair=en|tr', timeout=5)
        if r.status_code == 200:
            return r.json()['responseData']['translatedText']
    except: pass
    return ''

class Command(BaseCommand):
    help = 'Sözlüğe otomatik olarak binlerce rastgele kelime takviyesi yapar'

    def handle(self, *args, **options):
        # Yaygın kullanılan İngilizce kelimeleri çek
        all_english = list(get_english_words_set(['web2'], lower=True))
        random.shuffle(all_english)
        
        target_count = 500 
        added_count = 0
        
        self.stdout.write(self.style.WARNING(f'{target_count} kelime için işlem başlatılıyor...'))

        for word in all_english:
            if added_count >= target_count:
                break

            word = word.lower().strip()
            
            if len(word) < 3 or DictionaryWord.objects.filter(word__iexact=word).exists():
                continue

            phonetic, word_type, definition_en, example = fetch_definition(word)
            meaning_tr = fetch_translation(word)

            if meaning_tr and definition_en:
                if len(word) <= 4: level = 'A2'
                elif len(word) <= 7: level = 'B1'
                else: level = 'B2'

                DictionaryWord.objects.create(
                    word=word, level=level, phonetic=phonetic,
                    word_type=word_type, definition_en=definition_en,
                    example_sentence=example, meaning_tr=meaning_tr,
                )
                added_count += 1
                self.stdout.write(self.style.SUCCESS(f'[{added_count}/{target_count}] Eklendi: {word}'))
                time.sleep(0.6)

        self.stdout.write(self.style.SUCCESS(f'\nİşlem tamam! {added_count} yeni kelime eklendi.'))
                                                            