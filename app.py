import os
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from PIL import Image

from main import (
    hitung_frekuensi_grayscale, 
    hitung_probabilitas_nk, 
    hitung_cdf_ekualisasi, 
    pemetaan_inverse, 
    penerapan_histogram
)

app = Flask(__name__)

def gambar_ke_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proses', methods=['POST'])
def proses_gambar():
    if 'gambar_input' not in request.files or 'gambar_target' not in request.files:
        return jsonify({'error': 'Gambar tidak lengkap'}), 400

    file_input = request.files['gambar_input']
    file_target = request.files['gambar_target']

    # Konversi otomatis ke 8-bit Grayscale menggunakan Pillow
    img_in = Image.open(file_input).convert('L')
    img_tar = Image.open(file_target).convert('L')

    # Ekstrak data piksel menjadi list 1D
    piksel_in = list(img_in.getdata())
    piksel_tar = list(img_tar.getdata())

    # --- Eksekusi Modul Anda ---
    
    # 1. Frekuensi
    nk_in = hitung_frekuensi_grayscale(piksel_in)
    nk_tar = hitung_frekuensi_grayscale(piksel_tar)

    # 2. Probabilitas (PDF)
    pdf_in = hitung_probabilitas_nk(nk_in, len(piksel_in))
    pdf_tar = hitung_probabilitas_nk(nk_tar, len(piksel_tar))

    # 3. CDF Ekualisasi
    cdf_eq_in = hitung_cdf_ekualisasi(pdf_in)
    cdf_eq_tar = hitung_cdf_ekualisasi(pdf_tar)

    # 4. Pemetaan Invers
    mapp = pemetaan_inverse(cdf_eq_in, cdf_eq_tar)

    # 5. Penerapan
    piksel_out = penerapan_histogram(piksel_in, mapp)
    
    # Hitung histogram hasil untuk ditampilkan di grafik
    nk_out = hitung_frekuensi_grayscale(piksel_out)

    # Buat objek gambar baru untuk dikirim ke frontend
    img_out = Image.new('L', img_in.size)
    img_out.putdata(piksel_out)

    return jsonify({
        'img_input': gambar_ke_base64(img_in),
        'img_target': gambar_ke_base64(img_tar),
        'img_output': gambar_ke_base64(img_out),
        'hist_in': nk_in,
        'hist_tar': nk_tar,
        'hist_out': nk_out
    })

if __name__ == '__main__':
    app.run(debug=True)