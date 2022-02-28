from django.db import models

# Create your models here.
from auctions.models import User


class CategoryManager(models.Manager):
    def active_category(self, slug, id):
        return self.filter(status=True, slug=slug, id=id)
    def status_category(self):
        return self.filter(status=True)

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    objects = CategoryManager()
    def __str__(self):
        return self.title

class ListManager(models.Manager):
    def active_list(self, slug, id):
        return self.filter(status=True, slug=slug, id=id)

    def status_list(self):
        return self.filter(status=True)


class List(models.Model):
    title = models.CharField(max_length=120)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    descriptions = models.TextField()
    Initial_price = models.IntegerField()
    image_url = models.URLField()
    slug = models.SlugField(unique=True, default=None)
    status = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name='list_category')

    objects = ListManager()

    def __str__(self):
        return self.title



class ProposedPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proposed_price = models.IntegerField()

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list_comment', default=None)


    def __str__(self):
        return self.user.username




class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='bid_list', default=None)
    price = models.IntegerField()

    def __str__(self):
        return self.list.title
