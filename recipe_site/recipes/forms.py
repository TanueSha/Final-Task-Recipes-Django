from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeStep, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'categories', 'cooking_time', 'main_image']
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание рецепта',
            'categories': 'Категории',
            'cooking_time': 'Время приготовления (минуты)',
            'main_image': 'Основное изображение'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True }),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'required': True }),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['order', 'instruction', 'image']
        labels = {
            'order': 'Шаг',
            'instruction': 'Инструкция',
            'image': 'Изображение шага'
        }
        widgets = {
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Номер шага'
            }),
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Подробное описание шага'
            }),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measure']
        labels = {
            'name': 'Название ингредиента',
            'quantity': 'Количество',
            'measure': 'Единица измерения'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Мука'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': 0
            }),
            'measure': forms.Select(attrs={'class': 'form-control'})
        }


RecipeStepFormSet = inlineformset_factory(
    Recipe,
    RecipeStep,
    fields=('order', 'instruction', 'image'),
    form=RecipeStepForm,
    extra=1,
    can_delete=True,
    labels={
        'DELETE': 'Удалить шаг'
    }
)

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    fields=('name', 'quantity', 'measure'),
    form=IngredientForm,
    extra=1,
    can_delete=True,
    labels={
        'DELETE': 'Удалить ингредиент'
    }
)
