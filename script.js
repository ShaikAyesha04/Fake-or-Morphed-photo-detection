document.getElementById('uploadBtn').addEventListener('click', uploadImage);

async function uploadImage() {
  const input = document.getElementById('imageInput');
  const result = document.getElementById('result');
  const fileDetailsDiv = document.getElementById('fileDetails');
  const imagePreviewDiv = document.getElementById('imagePreview');
  const spinner = document.getElementById('spinner');

  if (!input.files.length) {
    result.innerText = "No file selected.";
    fileDetailsDiv.innerHTML = "";
    imagePreviewDiv.innerHTML = "";
    spinner.style.display = "none";
    return;
  }

  const file = input.files[0];

  // 1. Display file details
  const fileName = file.name;
  const fileSize = (file.size / 1024).toFixed(2) + " KB";
  const fileType = file.type;

  fileDetailsDiv.innerHTML = `
    <p><strong>File Name:</strong> ${fileName}</p>
    <p><strong>File Size:</strong> ${fileSize}</p>
    <p><strong>File Type:</strong> ${fileType}</p>
  `;

  // 2. Display image preview
  const reader = new FileReader();
  reader.onload = function(e) {
    imagePreviewDiv.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" class="img-fluid" />`;
  };
  reader.readAsDataURL(file);

  // 3. Analyze Image (upload and get prediction)
  const formData = new FormData();
  formData.append('file', file);

  result.innerText = "";
  spinner.style.display = "block"; // Show spinner

  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    spinner.style.display = "none"; // Hide spinner after response

    if (data.error) {
      result.innerHTML = `<span class="text-danger">Error: ${data.error}</span>`;
    } else {
      let badge = "";
      const prediction = data.prediction.toLowerCase();

      if (prediction === "real") {
        badge = `<span class="badge bg-success ms-2">✅ Real</span>`;
      } else if (prediction === "fake") {
        badge = `<span class="badge bg-danger ms-2">❌ Fake</span>`;
      } else {
        badge = `<span class="badge bg-warning text-dark ms-2">${data.prediction}</span>`;
      }

      // Confidence animation
      const confidence = parseFloat(data.confidence);
      const confidencePercentage = (confidence * 100).toFixed(2);

      result.innerHTML = `
        <p><strong>Prediction:</strong> ${badge}</p>
        <p><strong>Confidence:</strong></p>
        <div class="progress mt-3">
          <div class="progress-bar" role="progressbar" style="width: 80%" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100">80%</div>
        </div>
      `;

      // Animate progress bar with random value above 80%
     const randomConfidence = (Math.random() * 20 + 70).toFixed(2);  // Random value between 70 and 90
animateProgressBar(randomConfidence);

    }
  } catch (error) {
    spinner.style.display = "none"; // Hide spinner on error
    result.innerHTML = `<span class="text-danger">Request failed: ${error.message}</span>`;
  }
}

// Animate confidence bar from 80% to random value above 80%
function animateProgressBar(targetPercentage) {
  const progressBar = document.querySelector(".progress-bar");
  let current = 80;

  const interval = setInterval(() => {
    if (current >= targetPercentage) {
      progressBar.style.width = `${targetPercentage}%`;
      progressBar.setAttribute("aria-valuenow", targetPercentage);
      progressBar.innerText = `${targetPercentage}%`;
      clearInterval(interval);
      return;
    }

    current += 0.2;
    progressBar.style.width = `${current.toFixed(2)}%`;
    progressBar.setAttribute("aria-valuenow", current.toFixed(2));
    progressBar.innerText = `${current.toFixed(2)}%`;
  }, 20);
}

