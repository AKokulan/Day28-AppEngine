from django.db import models
from django.core.validators import validate_image_file_extension

# Create your models here.

class ArticleModel(models.Model):
    article_category_list=[('General','General'),('Technology','Technology'),('Politics','Politics'),('History','History'),('Science','Science'),('Aeronautics','Aeronautics')]
    article_header=models.CharField(blank=False,max_length=500)
    article_body = models.TextField(blank=False,max_length=10000)
    article_category = models.CharField(blank=False, max_length=500,default='General',choices=article_category_list)
    article_priority=models.IntegerField(blank=True)
    article_uploaded_date_time=models.DateTimeField(auto_now=True)
    uploader_ip_address=models.GenericIPAddressField(null=True,blank=True,max_length=100)
    carousel_image=models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True)
    image1=models.ImageField(upload_to='images/%Y/%m/%d/', blank=False,validators=[validate_image_file_extension])
    image2 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    image3 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    image4 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    image5 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    image6 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    image7 = models.ImageField(upload_to='images/%Y/%m/%d/%H%M%S', blank=True,validators=[validate_image_file_extension])
    active_news = models.BooleanField(default=False)
    carousel_news = models.BooleanField(default=False)
    trending_news = models.BooleanField(default=False)
    article_views=models.IntegerField(default=0)

    class Meta:
        permissions = (

            ("can_edit_news", "Can edit news"),
            ("can_delete_news", "Can delete news"),
            ("can_view_news", "Can view news"),
            ("can_upload_news", "Can upload news"),


        )

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.article_header)




