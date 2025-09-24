document.addEventListener("DOMContentLoaded", () => {
    localStorage.removeItem("cart");

    import('https://cdn.skypack.dev/canvas-confetti').then((module) => {
        const confetti = module.default;
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6 },
        });
    });

    const colors = ["#e74c3c", "#f39c12", "#27ae60", "#3498db", "#9b59b6", "#e91e63"];

    function createBalloon(container) {
        const balloon = document.createElement("div");
        balloon.classList.add("balloon");

        const isHeart = Math.random() < 0.3;
        const color = colors[Math.floor(Math.random() * colors.length)];

        if (isHeart) {
            balloon.classList.add("heart");
            balloon.style.color = color;

            const heart = document.createElement("div");
            heart.classList.add("heart-body");
            balloon.appendChild(heart);
        } else {
            const balloonBody = document.createElement("div");
            balloonBody.classList.add("balloon-body");
            balloonBody.style.backgroundColor = color;
            const size = Math.floor(Math.random() * 20) + 50;
            balloonBody.style.width = `${size}px`;
            balloonBody.style.height = `${size * 1.3}px`;
            balloon.appendChild(balloonBody);
        }

        const string = document.createElement("div");
        string.classList.add("balloon-string");

        balloon.style.left = `${Math.random() * 60 + 10}px`;
        balloon.style.animationDuration = `${Math.random() * 2 + 5}s`;

        balloon.appendChild(string);
        container.appendChild(balloon);

        setTimeout(() => balloon.remove(), 8000);
    }

    const leftContainer = document.querySelector(".balloons-container.left");
    const rightContainer = document.querySelector(".balloons-container.right");

    for (let i = 0; i < 7; i++) {
        setTimeout(() => {
            createBalloon(leftContainer);
            createBalloon(rightContainer);
        }, i * 500);
    }
});