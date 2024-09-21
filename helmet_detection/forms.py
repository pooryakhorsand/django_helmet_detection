# helmet_detection/forms.py
from django import forms


class ImageUploadForm(forms.Form):
	"""
    Form for uploading images for helmet detection.
    """
	image = forms.ImageField(label='Upload an Image', required=True)


class CCTVUploadForm(forms.Form):
	"""
    Form for submitting CCTV URLs for helmet detection.
    """
	cctv_url = forms.URLField(label='CCTV URL', max_length=200, required=True)
