document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultsDiv = document.getElementById('results');
    const resultContent = document.getElementById('result-content');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = form.querySelector('.btn-primary');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '⏳ Processing...';
        submitBtn.disabled = true;
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayResults(result);
                resultsDiv.classList.remove('hidden');
                // Scroll to results
                resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            alert('Error making prediction: ' + error.message);
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
    
    function displayResults(result) {
        const icon = document.getElementById('prediction-icon');
        const text = document.getElementById('prediction-text');
        const fill = document.getElementById('probability-fill');
        const label = document.getElementById('probability-label');
        const list = document.getElementById('explanation-list');
        
        // Clear previous results
        list.innerHTML = '';
        
        // Set prediction
        const isClick = result.prediction === 1;
        icon.textContent = isClick ? '✅' : '❌';
        text.textContent = isClick ? 'User will likely click on the ad!' : 'User is unlikely to click on the ad';
        text.style.color = isClick ? '#48bb78' : '#fc8181';
        
        // Set probability meter
        const prob = result.probability;
        fill.style.width = prob + '%';
        label.textContent = `Click Probability: ${prob}%`;
        
        // Set meter color
        if (prob < 40) {
            fill.style.background = 'linear-gradient(90deg, #fc8181, #f6ad55)';
        } else if (prob < 60) {
            fill.style.background = 'linear-gradient(90deg, #f6ad55, #68d391)';
        } else {
            fill.style.background = 'linear-gradient(90deg, #68d391, #48bb78)';
        }
        
        // Add explanation
        if (result.explanation && Array.isArray(result.explanation)) {
            result.explanation.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                list.appendChild(li);
            });
        }
    }
    
    // Reset form
    document.querySelector('.btn-secondary').addEventListener('click', function() {
        resultsDiv.classList.add('hidden');
        document.getElementById('probability-fill').style.width = '0%';
    });
});