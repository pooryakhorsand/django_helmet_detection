# Helmet Detection Application 

## Overview
This application is developed to enhance safety protocols at the Iran National Steel Group by providing real-time monitoring of helmet usage among workers. Utilizing advanced computer vision techniques and machine learning models, the application effectively detects when workers are not wearing helmets, ensuring compliance with safety regulations.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Videos](#videos)
- [Research Paper](#research-paper)


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
https://github.com/user-attachments/assets/b56eafc0-451b-4c31-814b-27908e4521a8


### 2. Workshop 1
https://github.com/user-attachments/assets/e48818a5-2e75-473f-a4aa-8c4a96d9e9d2



### 3. Workshop 2
https://github.com/user-attachments/assets/a297b335-59cd-4e12-b476-fb7d6a70b868

### 4. Workshop 3
https://github.com/user-attachments/assets/9bf1f7c9-9d01-435e-9c0e-1b64514fcbac

### 5.Helmet Alert
https://github.com/user-attachments/assets/6fc5c81b-d7a7-4061-b655-bfd109752b96


## Research Pape

This research paper documents the development and implementation of the Helmet Detection Application designed for the Iran National Steel Group. It explores the methodology employed in training custom YOLO models for each workshop, the data collection process using CCTV feeds, and the system's effectiveness in enhancing workplace safety. The paper highlights key findings related to real-time helmet detection and the impact of automated alerts on compliance with safety regulations.

