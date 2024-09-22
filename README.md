# Helmet Detection Application 

## Overview
This application is developed to enhance safety protocols at the Iran National Steel Group by providing real-time monitoring of helmet usage among workers. Utilizing advanced computer vision techniques and machine learning models, the application effectively detects when workers are not wearing helmets, ensuring compliance with safety regulations.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Usage](#usage)
- [Customization](#customization)
- [Videos](#videos)
- [Research Paper](#research-paper)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Real-Time Detection**: Utilizes YOLO (You Only Look Once) for fast and accurate helmet detection.
- **Workshop Customization**: Each workshop has a custom-trained model based on specific datasets, improving detection accuracy.
- **Database Notifications**: If a worker is detected without a helmet for more than 15 seconds, a notification is logged in a PostgreSQL database for safety monitoring.
- **API Integration**: Provides endpoints for interacting with the detection system, allowing users to upload images and receive prediction results.
- **Scalable Design**: The system can be expanded with additional workshops or cameras as needed.

## Architecture
- **CCTV Setup**: Three CCTV cameras are installed in three different workshops to capture video feeds.
- **Data Processing**: The captured video data is processed in real-time using a YOLO model trained on custom datasets.
- **Database Integration**: Notifications about helmet violations are stored in a PostgreSQL database, allowing for easy access and reporting.
- **API**: The application exposes RESTful API endpoints for image uploads and results retrieval.


## Videos
Here are demonstration videos of the Helmet Detection Application in action. Each video shows the system in use for different workshops.

### 1. Application Overview
[![Application Overview](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
*Watch how the application monitors helmet usage in real-time and sends notifications to the database.*

### 2. Workshop 1
[![Workshop 1](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
*Helmet detection in Workshop 1 with the custom-trained YOLOv8 model.*

### 3. Workshop 2
[![Workshop 2](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
*Monitoring helmet usage in Workshop 2.*

### 4. Workshop 3
[![Workshop 3](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
*Real-time detection of helmet violations in Workshop 3.*
