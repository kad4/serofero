from urllib.parse import urlparse

from django.template.defaultfilters import slugify
from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import requests

class Article(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 80)
    content = models.TextField(max_length = 305)
    
    url = models.URLField()
    views = models.IntegerField(default = 0)
    pub_date = models.DateTimeField(auto_now_add = True)

    category = models.CharField(max_length = 20)

    img_url = models.URLField(default = '')
    image = models.ImageField(upload_to = 'articles')

    def __str__(self):
        return self.title

    def get_remote_img(self):
        if(self.img_url == ''):
            return
        
        # Obtain filename
        file_name = urlparse(self.img_url).path.split('/')[-1] 
        
        # Read image data
        img_data = requests.get(self.img_url).content
        
        # Write the image data in temporary file
        img_temp = NamedTemporaryFile(delete = True)
        img_temp.write(img_data)
        img_temp.flush()

        self.image.save(file_name, File(img_temp))
