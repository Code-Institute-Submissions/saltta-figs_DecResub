from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin


# makes the content field a summernote field
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    summernote_fields = ('content')

