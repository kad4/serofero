from django.template.defaultfilters import slugify
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=500)
    url = models.URLField()
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title
