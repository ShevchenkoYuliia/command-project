let products = []; // глобально, чтобы и fetch и search к ней имели доступ

document.addEventListener("DOMContentLoaded", async () => {
  products = await fetchProducts(); // дождись загрузки продуктов

  const searchTrigger = document.querySelector(".search-trigger");
  const searchBox = document.querySelector(".search-box");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  if (!searchTrigger || !searchBox || !searchInput || !searchResults) return;

  searchTrigger.addEventListener("click", () => {
    searchBox.classList.toggle("show");
    if (searchBox.classList.contains("show")) {
      searchInput.focus();
    }
  });

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    searchResults.innerHTML = "";

    if (query.trim() === "") return;

    const filtered = products.filter((product) =>
      product.name.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
      searchResults.innerHTML = "<li>Нічого не знайдено</li>";
    } else {
      filtered.forEach((product) => {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = `/details/${product.id}`;
        link.textContent = product.name;
        li.appendChild(link);
        searchResults.appendChild(li);
      });
    }
  });
});

async function fetchProducts() {
  try {
    const response = await fetch("/products/simple");
    const data = await response.json();
    console.log("Продукти завантажені:", data);
    return data;
  } catch (error) {
    console.error("Помилка при завантаженні даних:", error);
    return [];
  }
}
