

document.addEventListener("DOMContentLoaded", function () {
  const sliderContainer = document.querySelector(".slider-container");
  const scrollAmount = 400;

  document.querySelector(".slider-btn.left").addEventListener("click", () => {
    sliderContainer.scrollBy({
      left: -scrollAmount,
      behavior: "smooth",
    });
  });

  document.querySelector(".slider-btn.right").addEventListener("click", () => {
    sliderContainer.scrollBy({
      left: scrollAmount,
      behavior: "smooth",
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const goToCart = document.getElementById("go-to-cart");
  const emptyMessage = document.getElementById("empty-message");

  goToCart.addEventListener("click", function (event) {
    const cart = JSON.parse(localStorage.getItem("cart")) || {};

    if (Object.keys(cart).length === 0) {
      event.preventDefault();

      emptyMessage.style.display = "block";

      setTimeout(() => {
        emptyMessage.style.display = "none";
      }, 3000);
    }
  });
});

function updateCartCount() {
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  let totalCount = 0;

  for (let id in cart) {
    totalCount += cart[id].quantity;
  }

  const cartCountEl = document.getElementById("cart-count");

  if (totalCount > 0) {
    cartCountEl.textContent = totalCount;
    cartCountEl.style.display = "inline-block";
  } else {
    cartCountEl.style.display = "none"; 
  }
}

document.addEventListener("DOMContentLoaded", updateCartCount);

document.addEventListener("DOMContentLoaded", function () {
  const buyButtons = document.querySelectorAll(".buy-btn");
  
  buyButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.id;
      const name = button.dataset.name;
      const price = parseFloat(button.dataset.price);
      const image = button.dataset.image;
      
      let cart = JSON.parse(localStorage.getItem("cart")) || {};
      
      if (cart[id]) {
        cart[id].quantity += 1;
      } else {
        cart[id] = { name, price, quantity: 1, image };
      }
      
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartCount();
    });
  });
});

document.querySelectorAll(".heart-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const icon = button.querySelector("i");
    button.classList.toggle("active");
    icon.classList.toggle("fa-regular");
    icon.classList.toggle("fa-solid");
  });
});

