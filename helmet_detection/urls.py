# helmet_detection/urls.py
from django.urls import path
from .views import HelmetDetectionView, HelmetDetectionAPIView, \
    CCTVDetectionAPIView, ImageTableView, CCTVTableView

app_name = 'helmet_detection'

urlpatterns = [
    # URL for the form view to handle image uploads via the web interface
    path('', HelmetDetectionView.as_view(), name='index'),

    # URL for displaying CCTV detection records
    path('cctv_table/', CCTVTableView.as_view(), name='cctv_table'),

    # URL for displaying helmet detection records with filtering options
    path('image_table/', ImageTableView.as_view(), name='image_table'),

    # API endpoint for handling helmet detection image uploads
    path('api/helmet-detection/', HelmetDetectionAPIView.as_view(), name='helmet_detection_api'),

    # API endpoint for handling CCTV detection requests
    path('api/cctv-detection/', CCTVDetectionAPIView.as_view(), name='cctv_detection_api'),
]
