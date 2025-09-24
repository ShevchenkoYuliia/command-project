document.addEventListener("DOMContentLoaded", function () {
  const checkoutItemsContainer = document.getElementById("checkout-items");
  const checkoutTotalPrice = document.getElementById("checkout-total-price");
  const orderItemsInput = document.getElementById("orderItems");
  const totalPriceInput = document.getElementById("totalPrice");

  const cart = JSON.parse(localStorage.getItem("cart")) || {};

  let total = 0;
  const orderItems = [];

  Object.entries(cart).forEach(([id, item]) => {
    const itemTotal = item.price * item.quantity;
    total += itemTotal;

    orderItems.push({
      product_id: id,
      product_name: item.name,
      price: item.price,
      quantity: item.quantity,
    });

    const div = document.createElement("div");
    div.className = "checkout-item";
    div.innerHTML = `
    <div class="checkout-item-name">${item.name}</div>
    <div class="checkout-item-price">${item.price} грн. × ${item.quantity} = ${itemTotal} грн.</div>
`;
    checkoutItemsContainer.appendChild(div);
  });

  checkoutTotalPrice.textContent = `${total} грн.`;

  orderItemsInput.value = JSON.stringify(orderItems);
  totalPriceInput.value = total;

  document
    .getElementById("order-form")
    .addEventListener("submit", function (e) {
      if (orderItems.length === 0) {
        e.preventDefault();
        alert(
          "Ваш кошик порожній. Додайте товар, перш ніж оформити замовлення."
        );
        window.location.href = "/catalog";
      }
    });
});
document.getElementById('order-form').addEventListener('submit', function(event) {
    const phone = document.getElementById('phone').value.trim();
    const address = document.getElementById('address').value.trim();
    const payment = document.getElementById('payment_method').value;

    const phoneRegex = /^[\d+\-\s]{7,15}$/;
    if (!phoneRegex.test(phone)) {
        alert('Введіть коректний номер телефону');
        event.preventDefault();
        return;
    }

    if (address.length < 5) {
        alert('Введіть коректну адресу доставки');
        event.preventDefault();
        return;
    }

    if (!payment) {
        alert('Оберіть спосіб оплати');
        event.preventDefault();
        return;
    }
});