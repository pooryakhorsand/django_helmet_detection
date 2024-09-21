# Helmet Detection Application 

## Overview
In industrial environments, worker safety is of paramount importance. This Helmet Detection Application has been developed for the Iran National Steel Group to monitor helmet compliance among workers in real-time. By leveraging advanced computer vision techniques and machine learning models, this application aims to significantly reduce the risk of injuries related to head safety.

The system utilizes CCTV cameras strategically placed in three workshops to continuously monitor workers. When a worker is detected without a helmet for more than 15 seconds, a notification is sent to a PostgreSQL database, enabling timely interventions. This proactive approach to safety helps ensure a secure working environment and compliance with safety regulations.

## Objectives
- **Enhance Worker Safety**: Minimize the risk of injuries by ensuring all workers are wearing helmets at all times.
- **Data-Driven Decisions**: Enable safety managers to access real-time data regarding helmet usage and violations, leading to informed decision-making.
- **Custom Solutions**: Allow for customization of detection models for specific workshops, ensuring the application is tailored to the unique environments of each site.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [API](#api)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Videos](#videos)
- [Research Paper](#research-paper)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Real-Time Detection**: Utilizes YOLO (You Only Look Once) for fast and accurate helmet detection.
- **Workshop Customization**: Each workshop has a custom-trained model based on specific datasets, improving detection accuracy tailored to each environment.
- **Database Notifications**: If a worker is detected without a helmet for more than 15 seconds, a notification is logged in a PostgreSQL database for safety monitoring and reporting.
- **API Integration**: Provides RESTful API endpoints for interacting with the detection system, allowing users to upload images and receive prediction results.
- **Scalable Design**: The system can be expanded with additional workshops or cameras as needed, making it suitable for larger industrial setups.

## Architecture
The application architecture consists of the following components:
- **CCTV Setup**: Three CCTV cameras are installed in three different workshops to capture real-time video feeds of workers.
- **Data Processing**: The captured video data is processed using a YOLO model trained on custom datasets. This allows the application to accurately identify whether workers are wearing helmets.
- **Database Integration**: Notifications regarding helmet violations are stored in a PostgreSQL database, allowing safety managers to track compliance and identify patterns of behavior.
- **API**: The application exposes RESTful API endpoints for image uploads and results retrieval, facilitating integration with other systems or applications.

## API
The application provides several API endpoints:
- **POST /api/upload/**: Upload an image for helmet detection.
- **GET /api/results/**: Retrieve the results of the helmet detection process.
  
### Example Usage
#### Upload Image
```bash
curl -X POST http://localhost:8000/api/upload/ -F 'image=@/path/to/image.jpg'
