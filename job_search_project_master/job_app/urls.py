from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.jobs_form, name= 'search_insert'), # get and post request for insert operation
#    path('<int:id>/', views.jobs_form, name='jobs_update'), # get and post request for update operation
    #path('delete/<int:id>/', views.jobs_delete, name='jobs_delete'),
    path('searchresults/', views.jobs_list, name= 'jobs_list') # get and post request for retrieve and display all items
]