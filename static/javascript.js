const uploadBtn = document.getElementById('upload');
const fileInput = document.getElementById('file-input');
/// Voice Recognition Feature
const startVoiceBtn = document.getElementById('start-voice');
const paragraph = document.getElementById('paragraph');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;  // Only recognize a single phrase
    recognition.lang = 'en-US';       // Set language to English
    recognition.interimResults = true; // Enable interim results for faster feedback
    recognition.maxAlternatives = 1;  // We only care about the best result

    let finalTranscript = '';  // Holds the final recognized text

    startVoiceBtn.addEventListener('click', () => {
        finalTranscript = '';  // Reset transcript when starting
        recognition.start();
    });

    recognition.onresult = (event) => {
        let interimTranscript = '';  // Temporary storage for interim results

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';  // Append final results to final transcript
            } else {
                interimTranscript += transcript;  // Append interim results to the interim transcript
            }
        }

        // Update the textarea with interim or final result
        paragraph.value = finalTranscript + interimTranscript;
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error detected: ' + event.error);
    };

    recognition.onspeechend = () => {
        recognition.stop();  // Stop recognition when the user stops speaking
    };
} else {
    console.error('Speech Recognition API not supported in this browser.');
}

// Image Upload and OCR Feature
/*const uploadBtn = document.getElementById('upload');
const fileInput = document.getElementById('file-input');

uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = () => {
            Tesseract.recognize(
                img,
                'eng',
                { logger: m => console.log(m) }
            ).then(({ data: { text } }) => {
                paragraph.value += text + ' ';
            }).catch(err => {
                console.error('Error during OCR: ', err);
            });
        };
    }
});*/

uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

// Handle file input change
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = () => {
            // Create a canvas to preprocess the image
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            // Set canvas dimensions to image dimensions
            canvas.width = img.width;
            canvas.height = img.height;

            // Draw the image onto the canvas
            ctx.drawImage(img, 0, 0);

            // Apply preprocessing
            let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            imageData = preprocessImage(imageData);
            ctx.putImageData(imageData, 0, 0);

            // Perform OCR using Tesseract with additional options
            Tesseract.recognize(
                canvas.toDataURL(),  // Pass the data URL of the canvas
                'eng',
                {
                    logger: m => console.log(m),
                    tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', // Limit character set
                    oem: 1  // Use the LSTM OCR Engine
                }
            ).then(({ data: { text } }) => {
                paragraph.value += text + ' ';
            }).catch(err => {
                console.error('Error during OCR: ', err);
            });
        };
    }
});

// Function to preprocess the image (grayscale and contrast adjustment)
function preprocessImage(imageData) {
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
        // Convert to grayscale
        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = data[i + 1] = data[i + 2] = avg;

        // Optional contrast adjustment
        data[i] = Math.min(255, data[i] * 1.5);
        data[i + 1] = Math.min(255, data[i + 1] * 1.5);
        data[i + 2] = Math.min(255, data[i + 2] * 1.5);
    }
    return imageData;
}