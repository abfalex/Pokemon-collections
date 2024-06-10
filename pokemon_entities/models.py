from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    title_en = models.CharField(verbose_name='Название (англ.)', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название (яп.)', max_length=200, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'Pokemon',
        on_delete=models.SET_NULL,
        verbose_name='Предыдущая эволюция',
        null=True,
        blank=True,
        related_name='next_evolutions'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Покемон'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    attack = models.IntegerField(verbose_name='Атака', null=True, blank=True)
    protection = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    endurance = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    class Meta:
        verbose_name = 'Детали покемона'