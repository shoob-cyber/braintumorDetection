document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const predictBtn = document.getElementById('predict-btn');
    const resultContainer = document.getElementById('result-container');
    const predictionText = document.getElementById('prediction');
    const specialistText = document.getElementById('specialist');
    const infoText = document.getElementById('info');
    let uploadedFile = null;

    fileInput.addEventListener('change', (event) => {
        uploadedFile = event.target.files[0];
        if (uploadedFile) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                resultContainer.style.display = 'none';
            }
            reader.readAsDataURL(uploadedFile);
        }
    });

    predictBtn.addEventListener('click', async () => {
        if (!uploadedFile) {
            alert("Please choose an image first!");
            return;
        }

        const formData = new FormData();
        formData.append('file', uploadedFile);
        predictBtn.textContent = 'Classifying...';
        predictBtn.disabled = true;

        try {
            const response = await fetch('/predict', { method: 'POST', body: formData });
            const data = await response.json();

            if (data.error) {
                predictionText.textContent = `Error: ${data.error}`;
                specialistText.textContent = '';
                infoText.textContent = '';
            } else {
                predictionText.textContent = `Prediction: ${data.prediction} (${data.confidence.toFixed(2)}% confidence)`;
                specialistText.textContent = `Suggested Specialist: ${data.specialist}`;
                infoText.textContent = `General Info: ${data.info}`;
            }
            resultContainer.style.display = 'block';
        } catch (error) {
            predictionText.textContent = 'An error occurred during prediction.';
        } finally {
            predictBtn.textContent = 'Classify Tumor';
            predictBtn.disabled = false;
        }
    });
});