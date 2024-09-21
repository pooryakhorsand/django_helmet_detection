// Function to handle model selection and update background
function selectModel(model, button, imageId) {
    // Set the selected model value
    const selectedModel = document.getElementById('selected_model');
    selectedModel.value = model;

    // Hide all image containers
    const containers = document.querySelectorAll('.image-container');
    containers.forEach(container => container.style.display = 'none');

    // Show the selected image container and update overlay text
    const selectedContainer = document.getElementById(`${imageId}-container`);
    if (selectedContainer) {
        selectedContainer.style.display = 'block';
        updateOverlayText(selectedContainer, model, imageId);
    }

    // Update left-panel background image
    updateLeftPanelBackground(model);

    // Update button styles
    updateButtonStyles(button);
}

// Function to update overlay text based on model and imageId
function updateOverlayText(container, model, imageId) {
    const overlay = container.querySelector('.image-overlay');
    if (overlay) {
        let workshopText = '';
        switch (imageId) {
            case 'image1':
                workshopText = model === 'model1' || model === 'first' ? 'Workshop 1' : '';
                break;
            case 'image2':
                workshopText = model === 'model2' || model === 'second' ? 'Workshop 2' : '';
                break;
            case 'image3':
                workshopText = model === 'model3' || model === 'third' ? 'Workshop 3' : '';
                break;
            default:
                workshopText = '';
        }
        overlay.textContent = workshopText;
    }
}

// Function to update the background of the left panel
function updateLeftPanelBackground(model) {
    const leftPanel = document.querySelector('.left-panel');
    leftPanel.classList.remove('background-image-1', 'background-image-2', 'background-image-3');

    if (model === 'model1' || model === 'first') {
        leftPanel.classList.add('background-image-1');
    } else if (model === 'model2' || model === 'second') {
        leftPanel.classList.add('background-image-2');
    } else if (model === 'model3' || model === 'third') {
        leftPanel.classList.add('background-image-3');
    }
}

// Function to update button styles
function updateButtonStyles(button) {
    const buttons = document.querySelectorAll('.btn-model');
    buttons.forEach(btn => btn.classList.remove('btn-active'));
    button.classList.add('btn-active');
}

// Function to initialize the default view
function initializeDefaultView() {
    const defaultImageId = 'image1';
    const defaultButton = document.getElementById('btn-model1');
    selectModel('model1', defaultButton, defaultImageId);
}

// Function to save the displayed image
function saveImage() {
    const image = document.getElementById('outputImage');
    if (image) {
        downloadImage(image.src, 'saved_image.png');
    } else {
        alert('No image to save');
    }
}

// Function to save all cropped images
function saveCroppedImages() {
    const croppedImages = document.querySelectorAll('#cropped-images-container .cropped-image');
    if (croppedImages.length === 0) {
        alert('No cropped images to save');
        return;
    }

    croppedImages.forEach((image, index) => {
        downloadImage(image.src, `cropped_image_${index + 1}.png`);
    });
}

// Helper function to trigger download for an image
function downloadImage(src, filename) {
    const link = document.createElement('a');
    link.href = src;
    link.download = filename;
    link.click();
}

// Initialize default view when the page loads
window.onload = initializeDefaultView;
