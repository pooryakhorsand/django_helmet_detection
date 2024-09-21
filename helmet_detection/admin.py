# helmet_detection/admin.py

from django.contrib import admin
from .models import PredictImageModel, CCTVPredictionModel

admin.site.register(PredictImageModel)
admin.site.register(CCTVPredictionModel)