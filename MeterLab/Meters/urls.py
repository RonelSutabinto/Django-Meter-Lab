from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    #     path('', views.meterList, name='meterList'),
    path('', RRViews.as_view(), name='rrviews'),

    path('delete/<int:id>/', views.delete_meters, name='delete_meters'),
    path('seriallist/<int:idmeters>/edit/<int:id>/',
         views.edit_meters, name='edit_meters'),

    path('seriallist/<int:id>/', views.seriallist, name='seriallist'),
    path('listofserials/<int:id>/',views.seriallist_data, name='listofserials'),
#     path('meterlist/<int:id>', MeterList.as_view(), 'meterlist'),

    path('selected_serial/', views.selected_serial,name='selected_serial'),
    path('seriallist/<int:idmeters>/calibrate_meter/<int:id>/', views.calibrate_meter,name='calibrate_meter'),
    path('multiple_calibration/<int:id>/',
         views.multiple_calibration, name='multiple_calibration'),
    path('delete_serials/<int:id>/', views.delete_serials, name='delete_serials'),

    path('seriallist/<int:idmeters>/meter_test_report/<int:id>/',
         views.meter_test_report, name='meter_test_report'),

    path('save_selectedTable',
         views.save_selectedTable, name='save_selectedTable'),

]
