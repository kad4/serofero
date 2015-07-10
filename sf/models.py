from django.template.defaultfilters import slugify
from django.db import models

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
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=305)
    category = models.ForeignKey(Category)
    
    url = models.URLField()
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    img_url = models.URLField()
    image = models.ImageField(upload_to='pages')

    def __str__(self):
        return self.title

    def get_remote_img(self):
        import requests

        self.image.save(
            self.id+'.'+img_url.split('.')[-1],
            requests.get(self.img_url).content
            )
        