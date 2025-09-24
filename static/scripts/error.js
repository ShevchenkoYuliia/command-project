document.addEventListener('DOMContentLoaded', function () {
    const background = document.querySelector('.error-background');
    if (!background) return;

    for (let i = 0; i < 15; i++) {
        const exclamation = document.createElement('div');
        exclamation.textContent = '!';
        exclamation.className = 'exclamation';

        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        exclamation.style.left = `${posX}%`;
        exclamation.style.top = `${posY}%`;

        const delay = Math.random() * 5;
        exclamation.style.animationDelay = `${delay}s`;

        const duration = 6 + Math.random() * 6;
        exclamation.style.animationDuration = `${duration}s`;

        background.appendChild(exclamation);
    }

    for (let i = 0; i < 10; i++) {
        const errorText = document.createElement('div');
        errorText.textContent = 'ERROR';
        errorText.className = 'error-text';

        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        errorText.style.left = `${posX}%`;
        errorText.style.top = `${posY}%`;

        const delay = Math.random() * 5;
        errorText.style.animationDelay = `${delay}s`;

        const duration = 8 + Math.random() * 10;
        errorText.style.animationDuration = `${duration}s`;

        background.appendChild(errorText);
    }
});