document.getElementById('login').addEventListener('submit', function() {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = 'flex';

    let seconds = 0;

    const timerInterval = setInterval(() => {
        seconds++;

        
        if (seconds >= 3) {
            clearInterval(timerInterval);
                overlay.style.display = 'none';
        }
    }, 1000);
});