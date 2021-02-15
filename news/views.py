from django.shortcuts import render,redirect
from django.contrib import messages
from news.forms import ArticleUploadForm
from news.models import ArticleModel
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Q
from django.contrib.auth.models import Permission

def show_home(request):

    main_article_m = ArticleModel.objects.filter(
        Q(article_priority=1 ) &
        Q(active_news=True) &
        Q(trending_news=True))[0]
    #main_article_m = ArticleModel.objects.filter(article_priority=1)[0]

    carousel_article_m = ArticleModel.objects.filter(carousel_news=True)
    trending_article_m = ArticleModel.objects.filter(trending_news=True)

    #pagination
    #all_article_m = ArticleModel.objects.all()
    #all_article_m = ArticleModel.objects.filter(active_news=True)
    all_article_m = ArticleModel.objects.all()

    page = request.GET.get('pg')

    all_article_m = ArticleModel.objects.all()
    page = request.GET.get('pg',1)

    paginator = Paginator(all_article_m, 10)
    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)



    print('article: ',article)
    for each in article:
        print(each)
    print('num of pages: ',paginator.num_pages)
    #print(carousel_article_m)
    #count_all_article= ArticleModel.objects.all().order_by('article_priority').count()

    return render(request,'index.html',{'main_article_m':main_article_m,'carousel_article_m':carousel_article_m,
                                        'all_article_m':article,'trending_article_m':trending_article_m})






def show_news(request):
    id=request.GET['go']
    main_art_m = ArticleModel.objects.get(pk=id)
    main_art_m.article_views+=1
    main_art_m.save()
    trending_article_m = ArticleModel.objects.filter(trending_news=True)
    #main_article={'news':main_art_m,'header':main_art_m.article_header, 'body':main_art_m.article_body[0:500]}
    return render(request,'news.html',{'main_art_m':main_art_m,'trending_article_m':trending_article_m})


# Create your views here.
@permission_required('news.can_upload_news')
def upload(request):
    print('upload clicked')
    if request.method == 'POST':
        article_form=ArticleUploadForm(request.POST, request.FILES)
        if article_form.is_valid():
            messages.success(request, 'News Created Successfully')
            print(article_form)
            print('article_priority: ',article_form.cleaned_data['article_priority'])

            a_model=create_article_model_instance(article_form,request)
            #article_form.cleaned_data['image1'].name
            #print(article_form)
            a_model.save()
            return redirect('upload')

        else:
            messages.error(request,article_form.errors)
            #return redirect('upload')
            return render(request, 'upload.html', {'article_form': article_form})
    else:
        article_form = ArticleUploadForm()
        return render(request,'upload.html',{'article_form':article_form})


def view(request):
    all_articles=ArticleModel.objects.all()
    return render(request, 'view.html', {'all_articles': all_articles})

def list(request):
    #pagination
    if request.method == 'POST':
        print('post method')
        print(request.POST.get('technology'))
        print('date: ',request.POST.get('date'))
        page = request.GET.get('pg')
        all_article_m,msg='',''
        filter_val={'general':request.POST.get('general'),'technology':request.POST.get('technology'),
                    'politics':request.POST.get('politics'),'history':request.POST.get('history'),
                    'science':request.POST.get('science'),'aeronautics':request.POST.get('aeronautics'),
                    'general1': request.POST.get('general1'), 'technology1': request.POST.get('technology1'),
                    'politics1': request.POST.get('politics1'), 'history1': request.POST.get('history1'),
                    'science1': request.POST.get('science1'), 'aeronautics1': request.POST.get('aeronautics1'),
                    'date':request.POST.get('date'),'popularity':request.POST.get('popularity'),
                    'date1':request.POST.get('date1'),'popularity1':request.POST.get('popularity1')}

        all_article_m1 = ArticleModel.objects.filter(article_category='Technology' if request.POST.get('technology') =='on' else None)
        all_article_m = ArticleModel.objects.filter(
                                                    Q(article_category='Technology' if request.POST.get('technology')  else None) |
                                                    Q(article_category='Politics' if request.POST.get('politics') else None) |
                                                    Q(article_category='History' if request.POST.get('history') else None) |
                                                    Q(article_category='Science' if request.POST.get('science') else None ) |
                                                    Q(article_category='General' if request.POST.get('general') else None ) |
                                                    Q(article_category='Technology' if request.POST.get('technology1') else None) |
                                                    Q(article_category='Politics' if request.POST.get('politics1') else None) |
                                                    Q(article_category='History' if request.POST.get('history1') else None) |
                                                    Q(article_category='Science' if request.POST.get('science1') else None) |
                                                    Q(article_category='General' if request.POST.get('general1') else None)
                                                    )

        print('article m before any filter: \n',all_article_m)
        print('article m 1 before any filter: \n', all_article_m1)
        if all_article_m:
            print('got value in article m')
            all_article_m = sort_articles(all_article_m, filter_val)
            print('page1:', page)
            if page is None:
                paginator = Paginator(all_article_m, 20)

                all_article_m = paginator.page(1)
            else:
                paginator = Paginator(all_article_m, 20
                                      )
                all_article_m = paginator.page(page)
            return render(request, 'list.html', {'all_article_m': all_article_m,'filter_val':filter_val})
        else:
            all_article_m = ArticleModel.objects.all().order_by('article_uploaded_date_time')
            all_article_m=sort_articles(all_article_m,filter_val)
            print('page1:', page)
            if page is None:
                paginator = Paginator(all_article_m, 20)

                all_article_m = paginator.page(1)
            else:
                paginator = Paginator(all_article_m, 20
                                      )
                all_article_m = paginator.page(page)

            msg= 'No articles available for the selected filter/filters'
            return render(request, 'list.html', {'all_article_m': all_article_m,'filter_val':filter_val,'msg':msg})
    else:
        print('get request')
        all_article_m = ArticleModel.objects.all().order_by('article_uploaded_date_time').reverse()
        page = request.GET.get('pg')
        if page is None:
            paginator = Paginator(all_article_m, 20)

            all_article_m=paginator.page(1)
        else:
            paginator = Paginator(all_article_m, 20
                                  )
            all_article_m = paginator.page(page)
        #all_articles=ArticleModel.objects.all()

        return render(request, 'list.html', {'all_article_m': all_article_m})


@permission_required('news.can_edit_news')
def edit(request,id):

    if request.method == 'POST':
        print(request.POST)
        article = ArticleModel.objects.get(pk=id)
        article_form = ArticleUploadForm(request.POST or None,request.FILES, instance=article)
        if article_form.is_valid():
            messages.success(request, 'It is success')
            print(article_form)
            article_form.save()

            all_articles = ArticleModel.objects.all()
            return render(request, 'view.html', {'all_articles': all_articles})
            #return render(request, 'edit.html', {'article': article})
        else:
            messages.error(request, article_form.errors)
            return render(request, 'edit.html', {'article': article})


    else:
        article=ArticleModel.objects.get(pk=id)
        article_form = ArticleUploadForm( request.POST or None, instance=article)
        return render(request, 'edit.html', {'article': article,'article_form':article_form})


@permission_required('news.can_delete_news')
def delete(request,id):
    article = ArticleModel.objects.get(pk=id)
    article.delete()
    all_articles = ArticleModel.objects.all()
    return render(request, 'view.html', {'all_articles': all_articles})



def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(type(ip))
    return ip

def create_article_model_instance(article_form,request):
    uploader_ip_address = get_ip_address(request)
    dt=datetime.now().strftime('%Y%m%d%H%M%S')
    print()
    tag = datetime.now().strftime("%Y%m%d%M%S")
    a_model = ArticleModel(
        article_header=article_form.cleaned_data['article_header'],
        article_body=article_form.cleaned_data['article_body'],
        article_priority=article_form.cleaned_data['article_priority'],
        article_category=article_form.cleaned_data['article_category'],
        # article_uploaded_date_time=article_form.cleaned_data['article_uploaded_date_time'],
        uploader_ip_address=uploader_ip_address,
        carousel_image=article_form.cleaned_data['carousel_image'],
        image1=article_form.cleaned_data['image1'],
        image2=article_form.cleaned_data['image2'],
        image3=article_form.cleaned_data['image3'],
        image4=article_form.cleaned_data['image4'],
        image5=article_form.cleaned_data['image5'],
        image6= article_form.cleaned_data['image6'],
        image7= article_form.cleaned_data['image7'],
        active_news=article_form.cleaned_data['active_news'],
        carousel_news=article_form.cleaned_data['carousel_news'],
        trending_news=article_form.cleaned_data['trending_news'],

    )
    return a_model


@register.filter
def get_range(value):
    print(range(value))
    return range(value)

@register.filter(name='truncatewords_c')
def truncatewords_c(value, arg):
    arg_list=arg.split(',')
    start,end=int(arg_list[0]),int(arg_list[1])

    word_list_extracted=[]
    words_list=value.split(' ')
    #print(1,words_list[start])
    print(2, len(words_list))
    #print(3, words_list[len(words_list)-1])
    if len(words_list)-1 > start and len(words_list)-1 >end:
        word_list_extracted= [words_list[each] for each in range(start,end) if each >= start and each<= end ]
    elif len(words_list)-1 > start and len(words_list)-1 < end :
        print('word is less',start,end)
        word_list_extracted = [words_list[each] for each in range(start, len(words_list)-1) if each >= start and each <= end]

    else:
        pass
    sentence =  ' '.join(word_list_extracted)

    print(start,end)
    print(sentence)
    return sentence

@register.filter(name='to_str_c')
def truncatewords_c(value):
    val=str(value)
    return val


#
def sort_articles(all_article_m,filter_val):
    print(filter_val)
    if (filter_val['date'] or filter_val['date1']) and (filter_val['popularity'] or filter_val['popularity1']):
        print('both filter active')
        all_article_m = all_article_m.order_by('article_uploaded_date_time', 'article_views').reverse()
    elif (filter_val['date'] or filter_val['date1']) and (filter_val['popularity'] is None or filter_val['popularity1'] is None):
        print('date filter active')
        all_article_m = all_article_m.order_by('article_uploaded_date_time').reverse()
    elif (filter_val['date'] is None or filter_val['date1'] is None) and (filter_val['popularity'] or filter_val['popularity1']):
        print('pop filter active')
        all_article_m = all_article_m.order_by('article_views').reverse()
    else:
        print('no filter active')
        all_article_m = all_article_m.order_by('article_uploaded_date_time').reverse()
    return all_article_m