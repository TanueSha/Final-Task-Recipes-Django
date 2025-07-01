from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    cuisine = models.CharField("Тип кухни", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.cuisine})"


class Recipe(models.Model):
    MEASUREMENTS = [
        ('г', 'грамм'), ('кг', 'килограмм'),
        ('мл', 'миллилитр'), ('л', 'литр'),
        ('шт', 'штука'), ('ч.л.', 'чайная ложка'),
        ('ст.л.', 'столовая ложка'),
        ('щепотка', 'щепотка'),
        ('по вкусу', 'по вкусу')
    ]

    title = models.CharField("Название рецепта", max_length=200, blank=True)
    description = models.TextField("Описание", blank=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    cooking_time = models.PositiveIntegerField("Время приготовления (мин)", blank=True, null=True)
    main_image = models.ImageField("Основное изображение", upload_to='recipes/main/')

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name="Рецепт", related_name='steps', on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Порядковый номер")
    instruction = models.TextField('Инструкция')
    image = models.ImageField("Изображение", upload_to='recipes/steps/', blank=True, null=True,
                              help_text="Изображение для этого шага (необязательно)")

    class Meta:
        verbose_name = "Шаг приготовления"
        verbose_name_plural = "Шаги приготовления"
        ordering = ['order']
        unique_together = ['recipe', 'order']


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name="Рецепт", related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=100)
    quantity = models.FloatField("Количество")
    measure = models.CharField("Единица измерения", max_length=20, choices=Recipe.MEASUREMENTS)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
