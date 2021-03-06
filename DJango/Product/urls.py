from django.http import HttpResponse
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


def index(request):
    return HttpResponse("this is Product page")


urlpatterns = [
    path('test', index),
    path('django_web', views.index),
    path('addProducts', views.post_product_data),

    path('personForm', views.get_form),
    path('showpersonForm', views.show_person_mf),
    path('deletepersonForm/<int:person_id>', views.delete_person_form),
    path('updatepersonForm/<int:person_id>', views.update_person_form),

    path('studentForm', views.post_student),
    path('getForm', views.get_student),
    path('deleteStudent/<int:i_id>', views.delete_student),
    path('updateStudent/<int:i_id>', views.update_student),

    path('getFile', views.get_file),
    path('postFile', views.post_file),
    path('deleteFile/<int:file_id>', views.delete_file),
    path('updateFile/<int:file_id>', views.update_file),

    path('getFileMF', views.get_file_mf),
    path('addFileMF', views.post_file_mf),
    path('deleteFileMF/<int:file_id>', views.delete_file_mf),
    path('updateFileMF/<int:file_id>', views.update_file_mf),

    path('profile', views.user_account),
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='product/passwordChange.html')),
    path('password_change_done', auth_views.PasswordChangeView.as_view(template_name='product/passwordChangeDone.html'), name='password_change_done'),

    path('getReporterMF', views.show_reporter_mf),
    path('postReporterMF', views.post_reporter_mf),
    path('getArticleMF', views.show_article_mf),
    path('postArticleMF', views.post_article_mf),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)