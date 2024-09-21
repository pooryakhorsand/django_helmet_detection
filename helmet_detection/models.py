# helmet_detection/models.py

from django.db import models


class PredictImageModel(models.Model):
	"""
    Model to store the result of helmet detection from uploaded images.
    """
	# The name of the uploaded image file
	image_name = models.CharField(max_length=255)
	
	# The result of the prediction, e.g., the number of helmets detected
	prediction_result = models.CharField(max_length=255)
	
	# The timestamp when the prediction was created
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		# Default ordering by creation date (most recent first)
		ordering = ['-created_at']
	
	def __str__(self):
		return f'{self.image_name} - {self.prediction_result}'


class CCTVPredictionModel(models.Model):
	"""
    Model to store the result of helmet detection from CCTV feed.
    """
	# The URL or name associated with the CCTV feed
	cctv_url_name = models.CharField(max_length=255, default='default_cctv_url')
	
	# The result of the prediction, e.g., the number of helmets detected
	prediction_result = models.CharField(max_length=255)
	
	# The timestamp when the prediction was created
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		# Default ordering by creation date (most recent first)
		ordering = ['-created_at']
	
	def __str__(self):
		return f'{self.cctv_url_name} - {self.prediction_result}'
