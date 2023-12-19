from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from Home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('about/',about_view, name='about'),
    path('submit_contact_form/',submit_contact_form, name='submit_contact_form'),
    path('submit_sub_form/',submit_sub_form, name='submit_sub_form'),
    path('photogallery/',photogallery_view, name='photogallery'),
    path('activate/',student_card_view, name='cardactivate'),
    path('Teachers_Portal/', include("Teachers_Portal.urls")),
    path('Student_Portal/', include("Student_Portal.urls")),
    path('Accounts/', include("Accounts.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header='GPL Academy'
admin.site.index_title='Site Administration'