document.addEventListener("DOMContentLoaded", function () {
    const cartContainer = document.getElementById("cart-items");
    let cart = JSON.parse(localStorage.getItem("cart")) || {};

    function renderCart() {
        const cartItemsContainer = document.getElementById("cart-items");
        const totalPriceWrapper = document.getElementById("total-price-wrapper");
    
        cartItemsContainer.innerHTML = "";
    
        const items = Object.entries(cart);
        if (items.length === 0) {
            cartItemsContainer.innerHTML = "<p class='empty'>Кошик порожній</p>";
            totalPriceWrapper.style.display = "none";
            return;
        }
    
        items.forEach(([id, item]) => {
            const div = document.createElement("div");
            div.className = "cart-item";
            div.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <div>
                    <h3>${item.name}</h3>
                    <p>Ціна: ${item.price} грн.</p>
                    <div class="quantity">
                        <button class="decrease" data-id="${id}">-</button>
                        <span>${item.quantity}</span>
                        <button class="increase" data-id="${id}">+</button>
                    </div>
                    <p>Сума: ${item.price * item.quantity} грн.</p>
                </div>
            `;
            cartItemsContainer.appendChild(div);
        });
    
        totalPriceWrapper.style.display = "block";
    
        updateTotalPrice();

        const checkoutWrapper = document.getElementById("checkout-wrapper");
        if (items.length > 0) {
            checkoutWrapper.style.display = "block";
        } else {
            checkoutWrapper.style.display = "none";
        }

        setupButtons();
    }
    
    function updateTotalPrice() {
        const totalPrice = Object.entries(cart).reduce((total, [id, item]) => {
            return total + item.price * item.quantity;
        }, 0);
    
        const totalPriceElement = document.getElementById("total-price");
        totalPriceElement.textContent = `${totalPrice} грн.`;
    }    

    function setupButtons() {
        document.querySelectorAll(".increase").forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                cart[id].quantity += 1;
                updateCart();
            });
        });

        document.querySelectorAll(".decrease").forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                cart[id].quantity -= 1;
                if (cart[id].quantity <= 0) {
                    delete cart[id];
                }
                updateCart();
            });
        });
    }

    function updateCart() {
        localStorage.setItem("cart", JSON.stringify(cart));
        renderCart();
    }

    renderCart();

    document.getElementById("clear-cart").addEventListener("click", () => {
        localStorage.removeItem("cart");
        cart = {};
        renderCart();
    });   
    
    document.getElementById("checkout-btn").addEventListener("click", () => {
        window.location.href = "/checkout";
    });
});