document.addEventListener('DOMContentLoaded', function() {
    const videoForm = document.getElementById('videoForm');
    const questionForm = document.getElementById('questionForm');
    const videoStatus = document.getElementById('videoStatus');
    const answer = document.getElementById('answer');
    const processLoader = document.getElementById('processLoader');
    const askLoader = document.getElementById('askLoader');
    const processBtn = document.getElementById('processBtn');
    const askBtn = document.getElementById('askBtn');

    videoForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const videoUrl = document.getElementById('videoUrl').value;
        
        // Show loading state
        videoStatus.style.display = 'none';
        processLoader.style.display = 'inline-block';
        processBtn.disabled = true;

        try {
            const response = await fetch("/process_video", {
                method: "POST",
                body: new FormData(videoForm),
            });
            const result = await response.json();
            processLoader.style.display = 'none';
            processBtn.disabled = false;
            videoStatus.style.display = 'block';

            if (result.error) {
                videoStatus.textContent = result.error;
                videoStatus.style.borderLeftColor = 'var(--accent)';
                videoStatus.classList.add('error');
            } else {
                videoStatus.textContent = result.message;
                videoStatus.style.borderLeftColor = 'var(--success)';
                videoStatus.classList.remove('error');
                // Enable question form
                document.getElementById('question').disabled = false;
                askBtn.disabled = false;
            }
        } catch (error) {
            processLoader.style.display = 'none';
            processBtn.disabled = false;
            videoStatus.style.display = 'block';
            videoStatus.textContent = "Error: " + error.message;
            videoStatus.style.borderLeftColor = 'var(--accent)';
            videoStatus.classList.add('error');
        }
    });

    questionForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const question = document.getElementById('question').value;
        
        // Show loading state
        answer.style.display = 'none';
        askLoader.style.display = 'inline-block';
        askBtn.disabled = true;

        try {
            const response = await fetch("/ask_question", {
                method: "POST",
                body: new FormData(questionForm),
            });
            const result = await response.json();
            askLoader.style.display = 'none';
            askBtn.disabled = false;
            answer.style.display = 'block';

            if (result.error) {
                answer.textContent = result.error;
                answer.style.borderLeftColor = 'var(--accent)';
                answer.classList.add('error');
            } else {
                answer.innerHTML = `<strong>Answer:</strong> ${result.answer}`;
                answer.style.borderLeftColor = 'var(--secondary)';
                answer.classList.remove('error');
            }
        } catch (error) {
            askLoader.style.display = 'none';
            askBtn.disabled = false;
            answer.style.display = 'block';
            answer.textContent = "Error: " + error.message;
            answer.style.borderLeftColor = 'var(--accent)';
            answer.classList.add('error');
        }
    });
});