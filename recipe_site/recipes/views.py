from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from .models import Recipe, RecipeStep, Category
from .forms import RecipeStepFormSet, IngredientFormSet

from django.contrib.auth.decorators import login_required


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.select_related('author').prefetch_related('categories')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['steps'] = recipe.steps.all().order_by('order')
        return context


class RecipeCreateView(CreateView):
    model = Recipe
    fields = ['title', 'description', 'categories', 'cooking_time', 'main_image']
    template_name = 'recipes/add_recipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['steps_formset'] = RecipeStepFormSet(self.request.POST, self.request.FILES)
            context['ingredients_formset'] = IngredientFormSet(self.request.POST)
        else:
            context['steps_formset'] = RecipeStepFormSet(prefix='steps')
            context['ingredients_formset'] = IngredientFormSet(prefix='ingredients')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        steps_formset = context['steps_formset']
        steps_formset = RecipeStepFormSet(self.request.POST, self.request.FILES, instance=self.object)
        ingredients_formset = context['ingredients_formset']

        # Сохраняем рецепт
        self.object = form.save(commit=False)
        self.object.save()

        form.save_m2m()

        steps_formset.instance = self.object
        ingredients_formset.instance = self.object

        if self.request.user.is_authenticated:
            self.object.author = self.request.user

        if steps_formset.is_valid() and ingredients_formset.is_valid():
            steps_formset.save()
            ingredients_formset.save()
            return super().form_valid(form)

        return self.form_invalid(form)
