from django.db import models

class Content(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Film'), 
        ('series', 'Dizi'), 
        ('game', 'Oyun'),
        ('animation', 'Animasyon')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    poster_url = models.CharField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Puan")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Tür", help_text="Örn: Dram, Aksiyon, Suç")

    # --- GENEL BİLGİLER ---
    year = models.CharField(max_length=20, blank=True, verbose_name="Yıl")
    director = models.CharField(max_length=200, blank=True, verbose_name="Yönetmen")
    season_count = models.CharField(max_length=50, blank=True, verbose_name="Sezon Sayısı")
    duration = models.CharField(max_length=50, blank=True, verbose_name="Süre")
    developer = models.CharField(max_length=200, blank=True, verbose_name="Geliştirici")
    studio = models.CharField(max_length=200, blank=True, verbose_name="Stüdyo")

    def __str__(self):
        return self.title


class CastMember(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='cast_members')
    name = models.CharField(max_length=200, verbose_name="Oyuncu Adı")
    role = models.CharField(max_length=200, blank=True, verbose_name="Rol Adı")
    photo_url = models.CharField(max_length=500, blank=True, verbose_name="Fotoğraf URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.content.title})"


class StoryVersion(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'), 
        ('B1', 'B1'), ('B2', 'B2'), 
        ('C1', 'C1'), ('C2', 'C2')
    ]
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='versions')
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES)
    text_en = models.TextField(verbose_name="İngilizce Metin", default="") 
    text_tr = models.TextField(verbose_name="Türkçe Metin", default="")

    class Meta:
        unique_together = ('content', 'level')

    def __str__(self):
        return f"{self.content.title} - {self.level}"
class DictionaryWord(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    word = models.CharField(max_length=100, unique=True, verbose_name="Kelime")
    word_type = models.CharField(max_length=50, blank=True, verbose_name="Kelime Türü")
    meaning_tr = models.CharField(max_length=300, blank=True, verbose_name="Türkçe Anlam")
    definition_en = models.TextField(blank=True, verbose_name="İngilizce Tanım")
    example_sentence = models.TextField(blank=True, verbose_name="Örnek Cümle")
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES, blank=True, verbose_name="Seviye")
    phonetic = models.CharField(max_length=100, blank=True, verbose_name="Telaffuz")

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word

class Vocabulary(models.Model):
    version = models.ForeignKey(StoryVersion, on_delete=models.CASCADE, related_name='vocabularies')
    word = models.CharField(max_length=100)
    word_type = models.CharField(max_length=50, help_text="Örn: n., v., adj.") 
    meaning = models.CharField(max_length=200)
    example_sentence = models.TextField()

    def __str__(self):
        return f"{self.word} ({self.version.content.title} - {self.version.level})"
    