function confirmEdit(user_id, name, email, role) {
  document.getElementById('editUserForm').action = `/update-user/${user_id}`;
  document.getElementById('user_id').value = user_id;
  document.getElementById('name').value = name;
  document.getElementById('email').value = email;
  document.getElementById('role').value = role;

  var myModal = new bootstrap.Modal(document.getElementById('editUserModal'));
  myModal.show();
}
document.addEventListener('DOMContentLoaded', function() {
    const editProductModalEl = document.getElementById('editProductModal');
    const editProductModal = new bootstrap.Modal(editProductModalEl);

    const editButtons = document.querySelectorAll('.edit-product-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-id');
            const productName = this.getAttribute('data-name');
            const description = this.getAttribute('data-description');
            const price = this.getAttribute('data-price');
            const category = this.getAttribute('data-category');
            const material = this.getAttribute('data-material');
            const color = this.getAttribute('data-color');
            const available = this.getAttribute('data-available') === 'true';
            const image = this.getAttribute('data-image');
            
            console.log("Данные продукта:", { 
                productId, productName, description, price, 
                category, material, color, available, image 
            });
            
            document.getElementById('product_id').value = productId;
            document.getElementById('product_name').value = productName;
            document.getElementById('description').value = description;
            document.getElementById('price').value = price;
            document.getElementById('category').value = category;
            document.getElementById('material').value = material;
            document.getElementById('color').value = color;
            document.getElementById('available').checked = available;
            document.getElementById('image').value = image || '';
            
            document.getElementById('editProductForm').action = `/update-product/${productId}`;
            
            editProductModal.show();
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const editOrderModalEl = document.getElementById('editOrderModal');
    if (!editOrderModalEl) {
        console.error('Модальное окно редактирования заказа не найдено!');
        return;
    }
    
    const editOrderModal = new bootstrap.Modal(editOrderModalEl);
    const editOrderForm = document.getElementById('editOrderForm');
    
    if (!editOrderForm) {
        console.error('Форма редактирования заказа не найдена!');
        return;
    }

    const editOrderButtons = document.querySelectorAll('.edit-order-btn');
    
    editOrderButtons.forEach(button => {
        button.addEventListener('click', function() {
            try {
                const orderId = this.getAttribute('data-order-id');
                const userId = this.getAttribute('data-user-id');
                const totalPrice = this.getAttribute('data-total-price');
                const status = this.getAttribute('data-status');
                const createdAt = this.getAttribute('data-created-at');
                const phone = this.getAttribute('data-phone');
                const address = this.getAttribute('data-address');
                const paymentMethod = this.getAttribute('data-payment-method');
                
                safeSetValue('order_id', orderId);
                safeSetValue('order_user_id', userId);
                safeSetValue('order_total_price', totalPrice);
                safeSetValue('order_status', status);
                safeSetValue('order_created_at', createdAt);
                safeSetValue('order_phone', phone);
                safeSetValue('order_address', address);
                safeSetValue('order_payment_method', paymentMethod);
                
                editOrderForm.action = `/update-order/${orderId}`;
                
                editOrderModal.show();
            } catch (error) {
                console.error('Ошибка при обработке кнопки редактирования:', error);
            }
        });
    });
    function safeSetValue(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.value = value || '';
        } else {
            console.warn(`Элемент с ID ${elementId} не найден!`);
        }
    }
});