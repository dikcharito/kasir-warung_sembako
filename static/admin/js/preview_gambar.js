// Tunggu halaman selesai load
document.addEventListener('DOMContentLoaded', function() {
    // Cari input file gambar
    const inputGambar = document.querySelector('input[type="file"]');
    
    if (inputGambar) {
        // Saat user pilih file
        inputGambar.addEventListener('change', function() {
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                
                // Saat file selesai dibaca
                reader.onload = function(e) {
                    let preview = document.getElementById('preview-img');
                    
                    // Kalau elemen preview belum ada, buat baru
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'preview-img';
                        preview.style.cssText = 'max-height:150px;border-radius:8px;margin-bottom:10px;display:block';
                        // Taruh sebelum input file
                        inputGambar.parentElement.insertBefore(preview, inputGambar);
                    }
                    
                    // Tampilkan preview
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                
                // Baca file sebagai URL
                reader.readAsDataURL(file);
            }
        });
    }
});