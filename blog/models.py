from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField

STATUS = ((0, 'Draft'), (1, 'Published'))

# Makes a usable model for recipe creation for the blog
class Recipe(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = AutoSlugField(populate_from='title', always_update=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    ingredients = models.TextField(null=True)
    steps = models.TextField(null=True)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

# usable model for comment creation
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=60)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"