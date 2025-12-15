const productsList = document.getElementById("productsList");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");

let products = [];

async function fetchProducts() {
  const res = await fetch("https://dummyjson.com/products");
  const data = await res.json();
  products = data.products;
  renderProducts(products);
}

function renderProducts(items) {
  productsList.innerHTML = "";

  items.forEach(product => {
    const card = document.createElement("div");
    card.className = "product-card";

    card.innerHTML = `
      <img src="${product.thumbnail}" alt="${product.title}">
      <div class="product-info">
        <h3>${product.title}</h3>
        <p>${product.description}</p>
        <p class="price">₹ ${product.price}</p>
      </div>
    `;

    productsList.appendChild(card);
  });
}

searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();
  const filtered = products.filter(product =>
    product.title.toLowerCase().includes(value)
  );
  renderProducts(filtered);
});

sortSelect.addEventListener("change", () => {
  let sortedProducts = [...products];

  if (sortSelect.value === "low-high") {
    sortedProducts.sort((a, b) => a.price - b.price);
  } else if (sortSelect.value === "high-low") {
    sortedProducts.sort((a, b) => b.price - a.price);
  }

  renderProducts(sortedProducts);
});

fetchProducts();