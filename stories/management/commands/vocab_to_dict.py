from django.core.management.base import BaseCommand
from stories.models import Vocabulary, DictionaryWord

class Command(BaseCommand):
    help = 'Tüm vocab kelimelerini DictionaryWord sözlüğüne aktarır'

    def handle(self, *args, **options):
        vocabs = Vocabulary.objects.select_related('version__content').all()
        added = 0
        skipped = 0

        for vocab in vocabs:
            word = vocab.word.strip()
            if not word:
                continue

            if DictionaryWord.objects.filter(word__iexact=word).exists():
                skipped += 1
                continue

            # Seviyeyi story version'dan al
            level = vocab.version.level if vocab.version else ''

            DictionaryWord.objects.create(
                word=word,
                word_type=vocab.word_type or '',
                meaning_tr=vocab.meaning or '',
                definition_en='',
                example_sentence=vocab.example_sentence or '',
                phonetic='',
                level=level,
            )
            added += 1
            self.stdout.write(f'✓ {word} eklendi')

        self.stdout.write(f'\n✅ {added} eklendi, {skipped} zaten vardı.')