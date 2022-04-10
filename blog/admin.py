from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin


# makes the content field a summernote field
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']

