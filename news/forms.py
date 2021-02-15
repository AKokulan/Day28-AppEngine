from django import forms

from news.models import ArticleModel

class ArticleUploadForm(forms.ModelForm):

    class Meta:
        model=ArticleModel
        fields=['article_header','article_body','article_category','article_priority',
                'carousel_image','image1','image2','image3','image4','image5','image6','image7',
                'active_news','carousel_news','trending_news']