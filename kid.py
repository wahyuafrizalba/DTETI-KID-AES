#Anggota kelompok
#Lukman Nurhakim            18/429073/TK/47575
#Ragil Putra Siswanto       18/431402/TK/47995
#Wahyu Afrizal Bahrul Alam  18/431411/TK/48004

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import sys

class EnkripsiDekripsi:
    def __init__(self, kunci):
        self.kunci = kunci

    def padding(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def enkrip(self, teks_biasa, kunci):
        teks_biasa = self.padding(teks_biasa)
        inisial_vektor = Random.new().read(AES.block_size)
        ciper = AES.new(kunci, AES.MODE_CBC, inisial_vektor)
        return inisial_vektor + ciper.encrypt(teks_biasa)

    def file_enkripsi(self, nama_file):
        try:
            with open(nama_file, 'rb') as f:
                teks_biasa = f.read()
        except IOError as e:
            print('\nFile tidak ditemukan,\nPastikan anda memasukkan nama file beserta format ekstensinya secara benar')
            print("Kemudian buka kembali program\n")
            sys.exit(0)
        teks_enkrip = self.enkrip(teks_biasa, self.kunci)
        with open(nama_file + ".kid", 'wb') as f:
            f.write(teks_enkrip)
        os.remove(nama_file)

    def dekrip(self, teks_enkrip, kunci):
        inisial_vektor = teks_enkrip[:AES.block_size]
        ciper = AES.new(kunci, AES.MODE_CBC, inisial_vektor)
        try:
            text_biasa = ciper.decrypt(teks_enkrip[AES.block_size:])
            return text_biasa.rstrip(b"\0")
        except ValueError as e:
            print("Dekripsi Gagal")
            print("Terdapat beberapa file yang dalam kondisi tidak terenkripsi")
            print("Fitur ini hanya bekerja saat semua file dalam kondisi terenkripsi terlebih dahulu")
            sys.exit(0)
       
    def file_dekripsi(self, nama_file):
        try:
            with open(nama_file, 'rb') as f:
                teks_enkrip = f.read()
        except IOError as e:
            print('\nFile tidak ditemukan,\nPastikan anda memasukkan nama file beserta format ekstensinya secara benar')
            print("Kemudian buka kembali program\n")
            sys.exit(0)
        teks_biasa = self.dekrip(teks_enkrip, self.kunci)
        with open(nama_file[:-4], 'wb') as f:
            f.write(teks_biasa)
        os.remove(nama_file)

    def akses_penyimpanan(self):
        letak_penyimpanan = os.path.dirname(os.path.realpath(__file__))
        penyimpanan = []
        for nama_penyimpanan, subpenyimpanan, daftar_file in os.walk(letak_penyimpanan):
            for nama_file in daftar_file:
                if (nama_file != 'kid.py' and nama_file != 'data.txt.kid' and nama_file != 'kunci.txt'):
                    penyimpanan.append(nama_penyimpanan + "\\" + nama_file)
        return penyimpanan

    def enkripsi_semua(self):
        penyimpanan = self.akses_penyimpanan()
        for file_name in penyimpanan:
            self.file_enkripsi(file_name)

    def dekripsi_semua(self):
        penyimpanan = self.akses_penyimpanan()
        for file_name in penyimpanan:
            self.file_dekripsi(file_name)

kunci = "Bawaan"
sembunyi = EnkripsiDekripsi(kunci)
hapus = lambda: os.system('cls')

if os.path.isfile('data.txt.kid'):
    hapus()
    i=3
    while i>0:
        akun = str(input("Masukkan nama pengguna: "))
        sandi = str(input("Masukkan kata sandi: "))
        try:
            with open("kunci.txt", "rb") as f:
                p = f.read()
        except IOError as e:
            print('File "kunci.txt" tidak ditemukan, silakan masukkan file tersebut secara manual')
            print("Kemudian buka kembali program\n")
            sys.exit(0)
        sembunyi = EnkripsiDekripsi(p)
        sembunyi.file_dekripsi("data.txt.kid")
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == akun+sandi:
            sembunyi.file_enkripsi("data.txt")
            break
        else:
            sembunyi.file_enkripsi("data.txt")
            hapus()
            print("Kombinasi Nama Pengguna dan Kata Sandi Salah")
            print(i-1,"Percobaan Tersisa\n")
        i-=1
        
    else :
        hapus()
        print("Anda salah memasukkan Kombinasi Nama Pengguna dan Kata Sandi  3 kali, data diblokir")
        os.remove("data.txt.kid")
        os.remove("kunci.txt")
        sys.exit(0)

    while True:
        hapus()
        choice = str(input(
            """
            Menu Utama

            1. Masukkan '1' untuk mengenkripsi file.
            2. Masukkan '2' untuk mendekripsi file.
            3. Masukkan '3' untuk mengenkripsi semua file.
            4. Masukkan '4' untuk mendekripsi semua file.
            5. Masukkan '5' untuk keluar.\n"""))

        if choice == '1':
            sembunyi.file_enkripsi(str(input("\nMasukkan nama file yang akan dienkripsi beserta ekstensi filenya : ")))
            print("\nEnkripsi Sukses")
            time.sleep(1)
        elif choice == '2':
            sembunyi.file_dekripsi(str(input("\nMasukkan nama file yang akan didekripsi beserta ekstensi filenya : ")))
            print("\nDekripsi Sukses")
            time.sleep(1)
        elif choice == '3':
            sembunyi.enkripsi_semua()
            print("\nEnkripsi Sukses")
            time.sleep(1)
        elif choice == '4':
            sembunyi.dekripsi_semua()
            print("\nDekripsi Sukses")
            time.sleep(1)
        elif choice == '5':
            hapus()
            sys.exit(0)
        else:
            print("Menu tidak tersedia, silakan pilih antara menu 1-5")
            time.sleep(1)

else:
    while True:
        hapus()
        print("Program Enkripsi v2.61\n")
        print("Program ini akan mengamankan file Anda\n\n")
        print("Akun tidak terdeteksi, Silakan membuat akun untuk menggunakan program\n")
        akun = str(input("Masukkan nama pengguna: "))
        sandi = str(input("Masukkan kata sandi: "))
        ksandi = str(input("Konfirmasi kata sandi: "))
        if sandi == ksandi:
            break
        else:
            print("\nKata sandi tidak sama, silakan coba lagi")
            time.sleep(1)
    def gantikunci():
        global kunci
        if os.path.isfile('kunci.txt'):
            with open("kunci.txt", "rb") as f:
                kunci = f.read()
        else:
            kunci = os.urandom(16)
    gantikunci()
    backup = kunci
    sembunyi = EnkripsiDekripsi(kunci)
    f = open("data.txt", "w+")
    f.write(akun+sandi)
    f.close()
    f = open("kunci.txt", "wb")
    f.write(backup)
    f.close()
    sembunyi.file_enkripsi("data.txt")
    hapus()
    i=30
    while i>=0:
        hapus()
        print("\nRegistrasi sukses, silakan mulai ulang program untuk mengakses menu utama\n")
        print('Jangan lupa mencadangkan file "kunci.txt"\nAgar saat akun anda terblokir namun ada file yang masih terenkripsi,')
        print('File tersebut dapat dipulihkan dengan "kunci.txt" cadangan yang telah Anda buat\n')
        print("Anda memiliki",i,"detik untuk mencadangkannya sebelum file dihapus permanen oleh sistem")
        time.sleep(1)
        i-=1
    os.remove("kunci.txt")
    print('\nFile terhapus\nSilakan masukkan "kunci.txt" secara manual saat memulai ulang program\n')

