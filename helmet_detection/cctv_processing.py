# helmet_detection/cctv_processing.py

from ultralytics import YOLO
import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os


def process_cctv(url_file, model_path):
	# Load the YOLO model
	model = YOLO(model_path)
	
	cap = cv2.VideoCapture(url_file)
	
	# Dictionary to keep track of time each person is without a helmet
	no_helmet_times = {}
	cropped_images = []
	no_helmet_count = 0
	frame_skip_interval = 30  # Configure as needed
	frame_count = 0
	
	try:
		while True:
			success, img = cap.read()
			if not success:
				break
			
			frame_count += 1
			if frame_count % frame_skip_interval != 0:
				continue
			
			results = model(img, stream=True)
			
			for r in results:
				boxes = r.boxes
				for i, box in enumerate(boxes):
					x1, y1, x2, y2 = box.xyxy[0]
					x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
					
					# If a person is wearing a helmet (class 0)
					if box.cls == 0:
						cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
						cv2.putText(img, 'helmet', (x1 - 14, y1 - 10),
						            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
						            (0, 255, 255), 2)
						
						# Reset no helmet time if they were tracked
						if i in no_helmet_times:
							no_helmet_times.pop(i)
					
					# If a person is not wearing a helmet (class 1)
					elif box.cls == 1:
						# Update no helmet time
						if i not in no_helmet_times:
							no_helmet_times[i] = 0
						no_helmet_times[i] += 1
						
						# Calculate time without helmet in seconds
						seconds_without_helmet = no_helmet_times[i] // (
								30 // frame_skip_interval)  # Convert frames to seconds
						
						# Set bounding box color to red if more than 30 seconds without helmet
						if seconds_without_helmet > 30:
							box_color = (0, 0, 255)  # Red color
							
							# Crop the bounding box area if more than 30 seconds
							cropped_img = img[y1:y2, x1:x2]
							
							# Encode the cropped image
							_, cropped_encoded = cv2.imencode('.jpg',
							                                  cropped_img)
							cropped_img_bytes = cropped_encoded.tobytes()
							
							# Save the cropped image to the media directory
							cropped_file_name = f'cctv_cropped_{no_helmet_count}.jpg'
							cropped_file = ContentFile(cropped_img_bytes,
							                           cropped_file_name)
							cropped_path = default_storage.save(
								os.path.join('cropped_images',
								             cropped_file_name),
								cropped_file)
							
							# Add the path to the list
							cropped_images.append(cropped_path)
							no_helmet_count += 1
						
						else:
							box_color = (255, 255, 0)  # Yellow color
						
						# Draw the bounding box with the chosen color
						cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 3)
						
						# Display the time without helmet next to the "no helmet" label
						label = f"no helmet: {seconds_without_helmet}s"
						cv2.putText(img, label, (x1 - 14, y1 - 10),
						            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
						            (255, 255, 255),
						            2)
			
			# Encode the processed frame
			_, frame_encoded = cv2.imencode('.jpg', img)
			frame_bytes = frame_encoded.tobytes()
			
			# Save the processed frame to a file if necessary or further process it
			frame_file = ContentFile(frame_bytes, 'processed_frame.jpg')
			default_storage.save(os.path.join('frames', 'processed_frame.jpg'),
			                     frame_file)
	
	finally:
		cap.release()
	
	# Return the count of detections and the list of cropped images
	return no_helmet_count, cropped_images
