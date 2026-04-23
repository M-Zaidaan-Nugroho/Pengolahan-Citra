

# Frekuensi nilai intensitas piksel (nk)
def hitung_frekuensi_grayscale(img):
    nk = [0] * 256
    for piksel in img:
        nk[piksel] += 1
    return nk

def hitung_probabilitas_nk(nk, total_piksel):
    pdf = [0] * len(nk)
    for i in range(len(nk)):
        pdf[i] = nk[i] / total_piksel
    return pdf

def hitung_cdf_ekualisasi(pdf):

    cdf = [0] * len(pdf)
    cdf[0] = pdf[0]

    # CDF yang sudah di ekualisasi
    cdf_eq = [0] * len(pdf)

    for i in range(1, len(pdf)):
        cdf[i] = cdf[i - 1] + pdf[i]
        cdf_eq[i] = round(cdf[i] * (len(pdf) - 1))

    return cdf_eq

def pemetaan_inverse(cdf_input, cdf_target):

    mapp = [0] * 256
    
    for k in range(256):
        nilai_sk = cdf_input[k]
        
        selisih_minimum = 256 
        nilai_q_terbaik = 0
        
        for q in range(256):
            selisih = abs(nilai_sk - cdf_target[q])
            
            if selisih < selisih_minimum:
                selisih_minimum = selisih
                nilai_q_terbaik = q
                
        mapp[k] = nilai_q_terbaik
        
    return mapp

def penerapan_histogram(img, mapp):
    gambar_baru = []
    for piksel in img:
        gambar_baru.append(mapp[piksel])
    return gambar_baru