document.addEventListener('DOMContentLoaded', function() {
    function updateHPP(produkId) {
        const hppField = document.querySelector('.field-hpp_saat_ini .readonly');
        if (!hppField) return;
        
        if (produkId) {
            fetch('/api/products/')
                .then(res => res.json())
                .then(data => {
                    const produk = data.data.find(p => p.id == produkId);
                    if (produk) {
                        hppField.innerHTML = `<strong style="color:#4CAF50;font-size:16px">Rp ${parseInt(produk.hpp).toLocaleString('id-ID')}</strong>`;
                    }
                });
        } else {
            hppField.innerHTML = 'Pilih produk dulu';
        }
    }

    // Cek setiap 500ms apakah nilai select berubah (karena Select2)
    let lastValue = '';
    setInterval(function() {
        const select = document.querySelector('#id_produk');
        if (select && select.value !== lastValue) {
            lastValue = select.value;
            updateHPP(select.value);
        }
    }, 500);
});