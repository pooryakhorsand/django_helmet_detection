# helmet_detection/image_processing.py

from ultralytics import YOLO
import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os


def process_image(image_file, model_path):
	"""
	Processes the uploaded image to detect helmets using YOLO model.

	Args:
		image_file: Uploaded image file.
		model_path: Path to the YOLO model file.

	Returns:
		Tuple containing:
		- Processed image as ContentFile.
		- Count of images with no helmet detected.
		- List of paths to cropped images.
	"""
	# Load the YOLO model
	model = YOLO(model_path)
	
	# Read the image from the uploaded file
	image_array = np.frombuffer(image_file.read(), np.uint8)
	img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
	
	# Extract the original image name (without extension)
	original_image_name = os.path.splitext(image_file.name)[0]
	
	# Perform helmet detection
	results = model(img, stream=True)
	
	# Initialize no-helmet count and a list to store cropped image file paths
	no_helmet_count = 0
	cropped_images = []
	
	for r in results:
		boxes = r.boxes
		for box in boxes:
			# Extract coordinates and class
			x1, y1, x2, y2 = map(int, box.xyxy[0])
			
			if box.cls == 0:  # Class 0: Human with helmet
				# Draw blue bounding box and green text for "helmet"
				cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
				cv2.putText(img, 'helmet', (x1 - 14, y1 - 10),
				            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			
			elif box.cls == 1:  # Class 1: Human without helmet
				# Draw red bounding box and orange text for "no helmet"
				cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
				cv2.putText(img, 'no helmet', (x1 - 14, y1 - 10),
				            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
				
				# Increment no-helmet count
				no_helmet_count += 1
				
				# Crop the bounding box area
				cropped_img = img[y1:y2, x1:x2]
				
				# Encode and save cropped image
				_, cropped_encoded = cv2.imencode('.jpg', cropped_img)
				cropped_img_bytes = cropped_encoded.tobytes()
				
				cropped_file_name = f'{original_image_name}_cropped_{no_helmet_count}.jpg'
				cropped_file = ContentFile(cropped_img_bytes, cropped_file_name)
				cropped_path = default_storage.save(
					os.path.join('cropped_images', cropped_file_name),
					cropped_file)
				
				# Add path to cropped images list
				cropped_images.append(cropped_path)
	
	# Encode the processed image back to a format that can be saved or returned
	_, img_encoded = cv2.imencode('.jpg', img)
	img_bytes = img_encoded.tobytes()
	
	# Return the processed image, no-helmet count, and list of cropped image paths
	return ContentFile(img_bytes,
	                   'processed_image.jpg'), no_helmet_count, cropped_images
