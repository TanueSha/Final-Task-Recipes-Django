from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView


urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('add/', RecipeCreateView.as_view(), name='add_recipe'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)