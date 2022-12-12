from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Recipe
from .forms import CommentForm, RecipeForm
import datetime

class AddRecipe(SuccessMessageMixin, LoginRequiredMixin, CreateView):

    model = Recipe
    form_class = RecipeForm
    template_name = 'add_recipe.html'

    login_url = '/accounts/login/'
    redirect_field_name = 'account_login'
    success_message = "Your recipe was added successfully"

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.object.slug})

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['author'] = self.request.user
        return initial

# view for the recipe list
class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


# methods to display recipes and receive comments
class RecipeDetail(View):
    # display recipes
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        return render(
            request,
            'recipe_detail.html',
            {
                'recipe': recipe,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )

    # post comments
    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False) 
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()
        
        return render(
            request,
            'recipe_detail.html',
            {
                'recipe': recipe,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )


# creates ability to add or remove like from recipes
class RecipeLike(View):

    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


# allows recipe to be edited
class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name_suffix = '_update_form'
    template_name = 'recipe_update_form.html'
    success_url = '/'


# deletes recipe
class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipe_delete.html'
    success_url = reverse_lazy('home')


