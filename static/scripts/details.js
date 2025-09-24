document.querySelectorAll(".letter-by-letter").forEach((el) => {
  const text = el.dataset.text.trim();
  el.innerHTML = "";
  const words = text.split(" ");
  words.forEach((word, wIndex) => {
    const wordSpan = document.createElement("span");
    wordSpan.style.display = "inline-block";
    wordSpan.style.marginRight = "8px";

    [...word].forEach((char, i) => {
      const span = document.createElement("span");
      span.textContent = char;
      span.style.animationDelay = `${(wIndex * 6 + i) * 0.03}s`;
      wordSpan.appendChild(span);
    });

    el.appendChild(wordSpan);
  });
});

document.querySelectorAll(".buy-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const flash = btn.querySelector(".flash");
    flash.classList.add("active");
    setTimeout(() => flash.classList.remove("active"), 400);
  });
});

document.addEventListener("mousemove", (e) => {
  const dot = document.createElement("div");
  dot.classList.add("sparkle-dot");
  dot.style.left = `${e.clientX}px`;
  dot.style.top = `${e.clientY}px`;
  document.getElementById("cursor-trail").appendChild(dot);
  setTimeout(() => dot.remove(), 1000);
});
