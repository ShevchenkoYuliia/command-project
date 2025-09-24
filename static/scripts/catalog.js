document.addEventListener("DOMContentLoaded", () => {
  // Get all filter buttons
  const filterButtons = document.querySelectorAll(".catalog-filter span");
  const products = document.querySelectorAll(".product-card");
  const clearAllButton = document.getElementById("clear-all-filters");

  // Get URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const categoryParam = urlParams.get('category');
  const materialParam = urlParams.get('material');
  const colorParam = urlParams.get('color');

  console.log("Current URL parameters:", {
    category: categoryParam,
    material: materialParam,
    color: colorParam
  });

  // Add event listeners to filter buttons
  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filterType = btn.dataset.filterType;  // category, material, or color
      const filterValue = btn.dataset.value;      // the specific value

      console.log(`Filter clicked: ${filterType} = ${filterValue}`);

      // Check if this filter is already active
      const isActive = btn.classList.contains("active-filter");
      
      // Build the new URL
      let newUrl = new URL(window.location.href);
      
      if (isActive) {
        // If active, remove this filter
        newUrl.searchParams.delete(filterType);
      } else {
        // If not active, add this filter
        newUrl.searchParams.set(filterType, filterValue);
      }
      
      // Navigate to the new URL (causes a full page reload)
      window.location.href = newUrl.toString();
    });
  });

  // Event listener for "Clear all filters" button
  if (clearAllButton) {
    clearAllButton.addEventListener("click", () => {
      // Redirect to the base catalog URL
      window.location.href = "/catalog";
    });
  }

  // Add to cart functionality
  const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.id;
      const name = button.dataset.name;
      const price = parseFloat(button.dataset.price);
      const image = button.dataset.image;

      let cart = JSON.parse(localStorage.getItem("cart")) || {};

      if (cart[id]) {
        cart[id].quantity += 1;
      } else {
        cart[id] = {
          name,
          price,
          image,
          quantity: 1,
        };
      }

      localStorage.setItem("cart", JSON.stringify(cart));
      showCustomAlert(`${name} додано до кошика!`);
      updateCartCount();
    });
  });

  // Update cart count on page load
  updateCartCount();
});

function showCustomAlert(message) {
  const alertBox = document.getElementById("custom-alert");
  if (alertBox) {
    alertBox.textContent = message;
    alertBox.classList.add("show");

    setTimeout(() => {
      alertBox.classList.remove("show");
    }, 2500);
  }
}

function updateCartCount() {
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  let totalCount = 0;

  for (let id in cart) {
    totalCount += cart[id].quantity;
  }

  const cartCountEl = document.getElementById("cart-count");
  if (cartCountEl) {
    if (totalCount > 0) {
      cartCountEl.textContent = totalCount;
      cartCountEl.style.display = "inline-block";
    } else {
      cartCountEl.style.display = "none";
    }
  }
}

