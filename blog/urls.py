from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('add_recipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path('recipe_edit/<slug:slug>', views.RecipeEditView.as_view(),
         name='recipe_edit'),
    path('recipe_delete/<slug:slug>', views.RecipeDeleteView.as_view(),
         name='recipe_delete'),
]