from django.db import models
from django.db.models import Q
import os
import random
from django.db.models.signals import pre_save, post_save
from retail_project.utils import unique_slug_generator
from django.urls import reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    title = instance.title.replace(" ", "")
    new_filename = random.randint(1, 5000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{title}/{final_filename}".format(title=title, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | \
            Q(description__icontains=query) | \
                Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # define New all() method with active filter
    # def all(self):
    #     return self.get_queryset().active()
    def search(self, query):
        return self.get_queryset().search(query)

    def featured(self): # Product.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=9.99) #null - empty in the DB
    image = models.ImageField(upload_to=upload_image_path, null = True, blank=True) # empty value in DB and not required in Django
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug) # hard-coded return
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
