from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    title_en = models.CharField(verbose_name='Название (англ.)', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название (яп.)', max_length=200, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    health = models.IntegerField(verbose_name='Здоровье', default=0)
    attack = models.IntegerField(verbose_name='Атака', default=0)
    protection = models.IntegerField(verbose_name='Уровень', default=0)
    endurance = models.IntegerField(verbose_name='Выносливость', default=0)
