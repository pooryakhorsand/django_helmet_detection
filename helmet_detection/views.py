# helmet_detection/urls.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.utils import timezone
from django.views.generic.edit import FormView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from .forms import ImageUploadForm, CCTVUploadForm
from .models import PredictImageModel, CCTVPredictionModel
from .image_processing import process_image
from .cctv_processing import process_cctv
import os


# View for handling helmet detection via a form
class HelmetDetectionView(LoginRequiredMixin, FormView):
	"""
    Handles the upload of images for helmet detection, processes them with a YOLO model,
    and displays the results on a webpage.
    """
	template_name = 'helmet_detection/index.html'
	form_class = ImageUploadForm
	login_url = '/accounts/login/'
	
	def form_valid(self, form):
		"""
        Processes the uploaded image using the selected YOLO model and prepares the context
        for rendering the results on the webpage.
        """
		# Retrieve the uploaded image and model choice from the form data
		uploaded_image = form.cleaned_data['image']
		model_choice = self.request.POST.get('model', 'first')
		model_path = {
			'second': settings.SECOND_YOLO_MODEL_PATH,
			'third': settings.THIRD_YOLO_MODEL_PATH
		}.get(model_choice, settings.FIRST_YOLO_MODEL_PATH)
		
		try:
			# Process the image and obtain the results
			processed_image_file, no_helmet_count, cropped_image_paths = process_image(
				uploaded_image, model_path
			)
		except Exception as e:
			# Handle errors during image processing
			form.add_error(None, f"An error occurred: {str(e)}")
			return self.form_invalid(form)
		
		# Save the processed image and prepare URLs for the cropped images
		file_name = 'processed_' + uploaded_image.name
		file_path = default_storage.save(os.path.join('uploads', file_name),
		                                 processed_image_file)
		file_url = default_storage.url(file_path)
		cropped_image_urls = [default_storage.url(path) for path in
		                      cropped_image_paths]
		
		# Save the prediction result to the database
		PredictImageModel.objects.create(
			image_name=uploaded_image.name,
			prediction_result=f'{no_helmet_count}'
		)
		
		# Prepare the context for rendering the response
		context = {
			'form': form,
			'uploaded_image_url': file_url,
			'cropped_image_urls': cropped_image_urls,
			'no_helmet_count': no_helmet_count,
		}
		return self.render_to_response(context)


# API view for helmet detection
class HelmetDetectionAPIView(LoginRequiredMixin, APIView):
	"""
    API endpoint for helmet detection. Accepts an image file, processes it using a YOLO model,
    and returns the results in JSON format.
    """
	parser_classes = [MultiPartParser, FormParser]
	renderer_classes = [JSONRenderer]
	
	def post(self, request, *args, **kwargs):
		"""
        Handles POST requests to process an uploaded image and returns the results in JSON format.
        """
		image = request.FILES.get('image')
		if image is None:
			return Response({'error': 'No image file provided.'}, status=400)
		
		model_path = settings.SECOND_YOLO_MODEL_PATH
		
		try:
			# Process the image and handle any errors
			processed_image_file, no_helmet_count, cropped_image_paths = process_image(
				image, model_path
			)
		except Exception as e:
			return Response({'error': f'An error occurred: {str(e)}'},
			                status=500)
		
		# Save and prepare URLs for the processed and cropped images
		file_name = 'processed_' + image.name
		file_path = default_storage.save(os.path.join('uploads', file_name),
		                                 ContentFile(
			                                 processed_image_file.read()))
		file_url = default_storage.url(file_path)
		cropped_image_urls = [default_storage.url(path) for path in
		                      cropped_image_paths]
		
		return Response({
			'processed_image_url': file_url,
			'cropped_image_urls': cropped_image_urls,
			'no_helmet_count': no_helmet_count
		})


# View for handling CCTV detection via a form
class CCTVDetectionView(LoginRequiredMixin, FormView):
	"""
    Handles the upload of CCTV URLs, processes the video stream for helmet detection,
    and displays the results on a webpage.
    """
	template_name = 'helmet_detection/index.html'
	form_class = CCTVUploadForm
	
	def form_valid(self, form):
		"""
        Processes the CCTV URL using the selected model and prepares the context
        for rendering the results on the webpage.
        """
		cctv_url = form.cleaned_data['cctv_url']
		model_choice = self.request.POST.get('model', 'first')
		model_path = settings.SECOND_CCTV_MODEL_PATH if model_choice == 'second' else settings.FIRST_CCTV_MODEL_PATH
		
		try:
			# Process the CCTV stream and handle any errors
			no_helmet_count, cropped_image_paths = process_cctv(cctv_url,
			                                                    model_path)
		except Exception as e:
			form.add_error(None, f"An error occurred: {str(e)}")
			return self.form_invalid(form)
		
		# Prepare URLs for the cropped images
		cropped_image_urls = [default_storage.url(path) for path in
		                      cropped_image_paths]
		
		# Save the prediction result to the database
		CCTVPredictionModel.objects.create(
			cctv_url_name=cctv_url,
			prediction_result=f'{no_helmet_count}'
		)
		
		# Prepare the context for rendering the response
		context = {
			'form': form,
			'cropped_image_urls': cropped_image_urls,
			'no_helmet_count': no_helmet_count,
			'cctv_url': cctv_url,
		}
		return self.render_to_response(context)


# API view for CCTV detection
class CCTVDetectionAPIView(LoginRequiredMixin, APIView):
	"""
    API endpoint for CCTV detection. Accepts a CCTV URL, processes the stream using a specified model,
    and returns the results in JSON format.
    """
	parser_classes = [MultiPartParser, FormParser]
	renderer_classes = [JSONRenderer]
	
	def post(self, request, *args, **kwargs):
		"""
        Handles POST requests to process a CCTV URL and returns the results in JSON format.
        """
		cctv_url = request.data.get('cctv_url')
		if not cctv_url:
			return Response({'error': 'No CCTV URL provided.'}, status=400)
		
		model_path = settings.SECOND_CCTV_MODEL_PATH
		
		try:
			# Process the CCTV stream and handle any errors
			no_helmet_count, cropped_image_paths = process_cctv(cctv_url,
			                                                    model_path)
		except Exception as e:
			return Response({'error': f'An error occurred: {str(e)}'},
			                status=500)
		
		# Prepare URLs for the cropped images
		cropped_image_urls = [default_storage.url(path) for path in
		                      cropped_image_paths]
		
		return Response({
			'cctv_url': cctv_url,
			'cropped_image_urls': cropped_image_urls,
			'no_helmet_count': no_helmet_count,
		})


# View to display helmet detection records with filtering options
class ImageTableView(LoginRequiredMixin, ListView):
	"""
    Displays helmet detection records with filtering options for various time periods.
    """
	model = PredictImageModel
	template_name = 'helmet_detection/image_table.html'
	context_object_name = 'detections'
	
	def get_queryset(self):
		"""
        Filters the queryset based on the selected filter type.
        """
		filter_type = self.request.GET.get('filter', 'all')
		now = timezone.now()
		
		if filter_type == 'today':
			start_date = now.date()
			queryset = PredictImageModel.objects.filter(
				created_at__date=start_date)
		elif filter_type == 'yesterday':
			start_date = now.date() - timezone.timedelta(days=1)
			queryset = PredictImageModel.objects.filter(
				created_at__date=start_date)
		elif filter_type == 'this_week':
			start_date = now - timezone.timedelta(days=now.weekday())
			queryset = PredictImageModel.objects.filter(
				created_at__date__gte=start_date)
		else:
			queryset = PredictImageModel.objects.all()
		
		return queryset


# View to display CCTV detection records
class CCTVTableView(LoginRequiredMixin, TemplateView):
	"""
    Displays CCTV detection records.
    """
	template_name = 'helmet_detection/cctv_table.html'
