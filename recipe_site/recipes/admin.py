from django.contrib import admin
from django.utils.html import mark_safe
from django import forms
from .models import Category, Recipe, RecipeStep, Ingredient


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    form = RecipeStepForm
    extra = 1
    fields = ('order', 'instruction', 'image_preview', 'image')
    readonly_fields = ('image_preview',)
    verbose_name = "Шаг приготовления"
    verbose_name_plural = "Шаги приготовления"

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" style="border-radius: 5px;" />')
        return "🖼️ Изображение не загружено"

    image_preview.short_description = "Превью"


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = ('name', 'quantity', 'measure')
    verbose_name = "Ингредиент"
    verbose_name_plural = "Ингредиенты"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_display', 'cooking_time', 'created_at')
    list_filter = ('categories', 'created_at')
    search_fields = ('title', 'description')
    inlines = [RecipeStepInline, IngredientInline]
    readonly_fields = ('created_at', 'image_preview')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'categories', 'author')
        }),
        ('Детали', {
            'fields': ('cooking_time', 'main_image', 'image_preview', 'created_at')
        }),
    )

    def author_display(self, obj):
        return obj.author.username if obj.author else "Гость"

    author_display.short_description = "Автор"

    def image_preview(self, obj):
        if obj.main_image:
            return mark_safe(f'<img src="{obj.main_image.url}" width="150" style="border-radius: 5px;" />')
        return "🖼️ Основное изображение не загружено"

    image_preview.short_description = "Превью"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine')
    search_fields = ('name', 'cuisine')


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'order', 'short_instruction', 'image_preview')
    list_filter = ('recipe',)
    search_fields = ('instruction',)
    readonly_fields = ('image_preview',)
    form = RecipeStepForm

    fieldsets = (
        (None, {
            'fields': ('recipe', 'order')
        }),
        ('Содержание', {
            'fields': ('instruction', 'image', 'image_preview')
        }),
    )

    def short_instruction(self, obj):
        return obj.instruction[:50] + '...' if len(obj.instruction) > 50 else obj.instruction

    short_instruction.short_description = "Инструкция"

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" style="border-radius: 5px;" />')
        return "🖼️ Изображение не загружено"

    image_preview.short_description = "Превью"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'name', 'quantity', 'measure')
    list_filter = ('recipe', 'measure')
    search_fields = ('name',)
