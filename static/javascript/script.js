// Fungsi untuk toggle menu dropdown
function toggleMenu() {
    var menu = document.getElementById("dropdown-menu");
    menu.classList.toggle('show');  // Menggunakan toggle untuk menambah/menghapus class
}
// Fungsi untuk toggle menu dropdown
function toggleMenu() {
    var menu = document.getElementById("dropdown-menu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

// Menutup dropdown jika klik di luar menu dropdown
window.onclick = function(event) {
    if (!event.target.matches('.menu-icon button, .menu-icon i')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
};


// Tutup menu dropdown jika klik di luar area menu
window.addEventListener('click', function(event) {
    if (!event.target.matches('.menu-icon button, .menu-icon i')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
});

// Fungsi untuk menampilkan kategori tertentu
function showCategory(category) {
    document.getElementById('home-section').style.display = 'none';
    document.getElementById('makanan-section').style.display = 'none';
    document.getElementById('minuman-section').style.display = 'none';
    document.getElementById('fotocopy-section').style.display = 'none';

    if (category === 'makanan') {
        document.getElementById('makanan-section').style.display = 'block';
    } else if (category === 'minuman') {
        document.getElementById('minuman-section').style.display = 'block';
    } else if (category === 'fotocopy') {
        document.getElementById('fotocopy-section').style.display = 'block';
    } else if (category === 'home') {
        document.getElementById('home-section').style.display = 'block';
    }
}

// Pengelolaan Keranjang
let cart = [];
let cartCount = 0;
let totalPrice = 0;

// Fungsi untuk menambah jumlah item
function increaseQuantity(itemName, itemPrice) {
    const quantityElement = document.getElementById(`quantity-${itemName}`);
    let quantity = parseInt(quantityElement.innerText);
    quantity++;
    quantityElement.innerText = quantity;

    // Perbarui jumlah di keranjang
    updateCartQuantity(itemName, itemPrice, 1);
}

// Fungsi untuk mengurangi jumlah item
function decreaseQuantity(itemName, itemPrice) {
    const quantityElement = document.getElementById(`quantity-${itemName}`);
    let quantity = parseInt(quantityElement.innerText);

    if (quantity > 0) {
        quantity--;
        quantityElement.innerText = quantity;

        // Perbarui jumlah di keranjang
        updateCartQuantity(itemName, itemPrice, -1);
    }
}

// Fungsi untuk menambah item ke keranjang
function addToCart(itemName, itemPrice) {
    const quantityElement = document.getElementById(`quantity-${itemName}`);
    let quantity = parseInt(quantityElement.innerText);
    if (quantity > 0) {
        const existingItem = cart.find(item => item.name === itemName);
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({ name: itemName, price: itemPrice, quantity: quantity });
        }
        cartCount += quantity;
        totalPrice += quantity * itemPrice;

        updateCartDisplay();
        openCart(); // Buka keranjang secara otomatis setelah item ditambahkan
    }
}

// Fungsi untuk memperbarui jumlah item di keranjang
function updateCartQuantity(itemName, itemPrice, change) {
    const existingItem = cart.find(item => item.name === itemName);
    if (existingItem) {
        existingItem.quantity += change;

        // Jika jumlah item <= 0, hapus dari keranjang
        if (existingItem.quantity <= 0) {
            cart = cart.filter(item => item.name !== itemName);
        }

        // Update cart count dan total price
        cartCount += change;
        totalPrice += change * itemPrice;
        
        // Pastikan nilai total tidak negatif
        if (cartCount < 0) cartCount = 0;
        if (totalPrice < 0) totalPrice = 0;

        updateCartDisplay();
    }
}

// Fungsi untuk memperbarui tampilan keranjang
function updateCartDisplay() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = ''; // Kosongkan konten keranjang sebelum menambahkan item baru

    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `<p>${item.name} - Rp${(item.price * item.quantity).toLocaleString()} x${item.quantity}</p>`;
        cartItems.appendChild(cartItem);
    });

    // Update total harga dan jumlah item di badge
    document.getElementById('total-price').textContent = `Rp${totalPrice.toLocaleString()}`;
    document.getElementById('cart-count').textContent = cartCount;
}

// Fungsi untuk membuka modal keranjang
function openCart() {
    document.getElementById('cart-modal').style.display = 'block';
}

// Fungsi untuk menutup modal keranjang
function closeModal() {
    document.getElementById('cart-modal').style.display = 'none';
}

// Event untuk close modal dengan klik di luar modal
window.onclick = function(event) {
    const modal = document.getElementById('cart-modal');
    if (event.target === modal) {
        closeModal();
    }
}

// Fungsi untuk mengonfirmasi pesanan
function confirmOrder() {
    // Simpan data pesanan ke localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    localStorage.setItem('total-price', totalPrice);

    // Pastikan penyimpanan terjadi sebelum redirect
    window.location.href = 'Pesanan.html';
}

// Fungsi untuk menampilkan halaman detail pesanan
function showOrderDetails() {
    // Mengambil data pesanan dari localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalPrice = localStorage.getItem('total-price') || 0;

    // Menampilkan daftar pesanan di halaman
    const orderItemsList = document.getElementById('order-items-list');
    cart.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item.name} - Rp${(item.price * item.quantity).toLocaleString()} x${item.quantity}`;
        orderItemsList.appendChild(listItem);
    });

    // Menampilkan total harga
    document.getElementById('order-total-price').textContent = `Rp${parseInt(totalPrice).toLocaleString()}`;
}

// Fungsi untuk pembayaran
function makePayment() {
    const paymentMethod = document.getElementById('payment-method').value;
    alert(`Pembayaran menggunakan metode: ${paymentMethod}. Terima kasih telah berbelanja!`);
    // Logika pembayaran bisa ditambahkan di sini
}
  // Simpan data ke localStorage dan buka halaman Struk
document.getElementById("place-order-btn").addEventListener("click", function() {
    const orderData = {
        storeName: "Gorengan Bu Ade",
        storeAddress: "Jl. Sukajadi No. 123, Bandung",
        items: cartItems.map(item => ({
            name: item.name,
            quantity: item.quantity,
            price: item.price * item.quantity
        })),
        totalPrice: calculateTotalPrice(),
        paymentMethod: document.getElementById("payment-method").value || "Cash" // Default ke Cash
    };

    localStorage.setItem("orderData", JSON.stringify(orderData));
    window.location.href = "Struk.html";
});

function completeOrder() {
    alert("Pesanan berhasil dibuat!");
    localStorage.removeItem("cart"); // Hapus data pesanan setelah diproses
    window.location.href = "Menu1.html";
}
