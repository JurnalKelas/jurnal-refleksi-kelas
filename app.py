import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import datetime
import random 

# ==========================================
# BAGIAN 1: PENGATURAN DATABASE (SQLITE)
# ==========================================
def init_db():
    conn = sqlite3.connect('database_tahfidz.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_lengkap TEXT,
            mata_pelajaran TEXT,
            name TEXT,
            kelas TEXT,
            absen TEXT,
            feeling TEXT,
            belajar_tentang TEXT,
            sudah_paham TEXT,
            kesulitan TEXT,
            cara_atasi TEXT,
            hal_disukai TEXT,
            target_berikutnya TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS guru_auth (
            mata_pelajaran TEXT PRIMARY KEY,
            password TEXT UNIQUE
        )
    ''')
    
    c.execute('SELECT COUNT(*) FROM guru_auth')
    if c.fetchone()[0] == 0:
        password_bawaan = [
            ("Halaqoh Ustadz Mursanto", "Mursanto"),
            ("Halaqoh Ustadz M. Tohir Asyhuri", "M. Tohir Asyhuri"),
            ("Halaqoh Ustadz Arif Subkhan", "Arif Subkhan"),
            ("Halaqoh Ustadz Ach. Jalilul Chakam", "Ach. Jalilul Chakam"),
            ("Halaqoh Ustadz Ach. Wahyu Zakariya", "Ach. Wahyu Zakariya"),
            ("Semua Halaqoh", "adminSUPER")
        ]
        c.executemany('INSERT OR IGNORE INTO guru_auth (mata_pelajaran, password) VALUES (?, ?)', password_bawaan)
        
    conn.commit()
    conn.close()

def insert_data(waktu_lengkap, mapel, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target):
    conn = sqlite3.connect('database_tahfidz.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reflections (waktu_lengkap, mata_pelajaran, name, kelas, absen, feeling, belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (waktu_lengkap, mapel, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect('database_tahfidz.db')
    df = pd.read_sql_query("SELECT * FROM reflections", conn)
    conn.close()
    return df

def get_mapel_by_password(pwd):
    conn = sqlite3.connect('database_tahfidz.db')
    c = conn.cursor()
    c.execute('SELECT mata_pelajaran FROM guru_auth WHERE password = ?', (pwd,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def update_password(mapel, new_pwd):
    conn = sqlite3.connect('database_tahfidz.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE guru_auth SET password = ? WHERE mata_pelajaran = ?', (new_pwd, mapel))
        conn.commit()
        sukses = True
    except sqlite3.IntegrityError:
        sukses = False
    conn.close()
    return sukses

init_db()

# ==========================================
# BAGIAN 2: KAMUS BAHASA & QUOTE ISLAMI
# ==========================================
st.set_page_config(page_title="Jurnal Tahfidz Siswa", page_icon="📖", layout="centered")

quotes_id = [
    ("خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ", "Sebaik-baik kalian adalah yang mempelajari Al-Qur'an dan mengajarkannya. (HR. Bukhari)"),
    ("اقْرَءُوا الْقُرْآنَ فَإِنَّهُ يَأْتِي يَوْمَ الْقِيَامَةِ شَفِيعًا لِأَصْحَابِهِ", "Bacalah Al-Qur'an, karena ia akan datang pada hari kiamat memberi syafa'at. (HR. Muslim)"),
    ("أَهْلُ الْقُرْآنِ هُمْ أَهْلُ اللَّهِ وَخَاصَّتُهُ", "Para ahli Al-Qur'an, merekalah keluarga Allah dan hamba pilihan-Nya. (HR. Ibnu Majah)"),
    ("تَعَاهَدُوا هَذَا الْقُرْآنَ", "Jagalah hafalan Al-Qur'an ini dengan senantiasa memurojaahnya. (Muttafaqun 'Alaih)")
]

quotes_en = [
    ("خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ", "The best among you are those who learn the Quran and teach it. (Bukhari)"),
    ("اقْرَءُوا الْقُرْآنَ فَإِنَّهُ يَأْتِي يَوْمَ الْقِيَامَةِ شَفِيعًا لِأَصْحَابِهِ", "Read the Quran, for it will come as an intercessor for its reciters. (Muslim)"),
    ("أَهْلُ الْقُرْآنِ هُمْ أَهْلُ اللَّهِ وَخَاصَّتُهُ", "The people of the Quran are the people of Allah and His chosen ones. (Ibn Majah)"),
    ("تَعَاهَدُوا هَذَا الْقُرْآنَ", "Keep refreshing your knowledge of the Quran. (Agreed Upon)")
]

with st.sidebar:
    language = st.selectbox("🌐 Pilih Bahasa / Language:", ["Indonesia", "English"])
    st.divider()
    
if language == "Indonesia":
    quote_arab, quote_arti = random.choice(quotes_id)
    t = {
        "title": "📖 Jurnal Setoran Tahfidz",
        "subtitle": "Mari luruskan niat, dan catat progres hafalan serta murojaah kita hari ini.",
        "teacher_settings": "🎨 Pengaturan Tampilan",
        "bg_color": "Pilih Warna Latar:",
        "help_center": "📖 Pusat Bantuan",
        "btn_dl_guide": "📥 Download Panduan",
        "student_profile": "Data Diri Santri",
        "subject": "Halaqoh / Ustadz Pembimbing:",
        "date": "Tanggal:",
        "time": "Waktu Setoran:",
        "name": "Nama Lengkap:",
        "class": "Kelompok/Kelas:", 
        "absen": "Nomor Presensi:",
        "q_header": "Lembar Mutaba'ah (Evaluasi Diri)",
        "q_feel": "Menurut penilaianmu sendiri, bagaimana tingkat kelancaran hafalanmu hari ini?",
        "q1": "1. Hari ini saya menyetorkan hafalan (Juz / Surah / Ayat):",
        "q2": "2. Ayat/Surah yang sudah dirasa sangat lancar:",
        "q3": "3. Kesulitan yang saya alami (Tersendat / Lupa ayat / Tajwid dll):",
        "q4": "4. Cara saya mengatasi kesulitan tersebut (misal: diulang 10x):",
        "q5": "5. Hal yang paling disyukuri saat menghafal hari ini:",
        "q6": "6. Target hafalan / murojaah saya untuk pertemuan berikutnya:",
        "btn_submit": "Simpan Catatan Tahfidz",
        "warn_name": "Tolong masukkan nama lengkapmu ya!",
        "success": "Alhamdulillah, {}! Catatan setoranmu telah tersimpan. Tetap istiqomah!",
        
        # --- TEKS PORTAL ORANG TUA ---
        "parent_header": "👨‍👩‍👧 Portal Unduh Rapor Orang Tua",
        "parent_desc": "Ayah/Bunda dapat memantau progres hafalan ananda dengan mengunduh rapor Tahfidz berstandar internasional di bawah ini. Masukkan Nama Lengkap dan Nomor Presensi ananda untuk mengakses dokumen.",
        "p_name": "Nama Lengkap Ananda (Sesuai di atas):",
        "p_absen": "Nomor Presensi:",
        "p_btn": "Akses Rapor Tahfidz",
        "p_error": "Afwan, data tidak ditemukan. Pastikan ketikan nama dan nomor presensi ananda benar.",
        "p_success": "Alhamdulillah data ditemukan! Silakan unduh dokumen PDF di bawah ini.",
        "btn_dl_rapor": "📥 Download Tahfidz Progress Report ({})",

        "board_header": "🕌 Ruang Guru & Laporan Halaqoh",
        "chart_header": "📊 Grafik Kelancaran Halaqoh - {}",
        "pass_header": "🔒 Akses Data Ustadz/Ustadzah",
        "pass_desc": "Masukkan kata sandi halaqoh Anda untuk merekap data evaluasi.",
        "pass_input": "Kata Sandi (Password):",
        "pass_success": "Sandi diterima! Ahlan wa sahlan, menampilkan data: **{}**",
        "pass_error": "Afwan, kata sandi salah. Silakan coba lagi.",
        "filter_time_header": "⏳ Filter Waktu Setoran",
        "filter_time_desc": "Pilih rentang tanggal untuk merekap mutaba'ah per pekan atau per bulan.",
        "start_date": "Dari Tanggal:",
        "end_date": "Sampai Tanggal:",
        "no_date_data": "Tidak ada setoran pada rentang tanggal tersebut.",
        "print_header": "👤 Cetak Buku Mutaba'ah Lengkap",
        "print_desc": "Unduh rekam jejak mendetail santri beserta catatan kesulitan dan cara mengatasinya.",
        "select_name": "Pilih Nama Santri:",
        "graph_mood": "**Grafik Kelancaran: {}**",
        "last_entry": "**Setoran Terakhir:**",
        "difficulty": "Kesulitan:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Buku Mutaba'ah (Detail)",
        "gallery_header": "📌 Galeri Catatan Santri",
        "gallery_desc": "Klik pada nama santri untuk membaca rincian kesulitan dan target mereka.",
        "export_header": "💾 Export Laporan Keseluruhan",
        "export_desc": "Unduh seluruh data setoran dan rekap jumlah setoran santri di halaqoh Anda.",
        "btn_dl_all": "📥 Download Laporan (PDF)",
        "btn_dl_csv": "📥 Download Data Excel (CSV)",
        "btn_dl_rank": "📥 Download Rekap Jumlah Setoran (CSV)",
        "no_data": "Belum ada santri yang menyetorkan catatan di halaqoh ini.",
        "pdf_class_title": "Laporan Jurnal Tahfidz - {}", 
        "pdf_ind_title": "Buku Mutaba'ah Tahfidz: {}",
        "change_pass_header": "Ubah Kata Sandi Akses",
        "change_pass_desc": "Ganti kata sandi bawaan dengan sandi rahasia Anda sendiri.",
        "new_pass_input": "Masukkan Kata Sandi Baru:",
        "btn_save_pass": "Simpan Kata Sandi Baru",
        "pass_changed_success": "Berhasil! Sandi Anda telah diubah. Halaman akan dimuat ulang.",
        "pass_changed_error": "Gagal! Kata sandi ini sudah digunakan oleh halaqoh lain."
    }
else:
    quote_arab, quote_arti = random.choice(quotes_en)
    t = {
        "title": "📖 Tahfidz Mutaba'ah Journal",
        "subtitle": "Let's purify our intentions and record our memorization progress today.",
        "teacher_settings": "🎨 Appearance Settings",
        "bg_color": "Select Background Color:",
        "help_center": "📖 Help Center",
        "btn_dl_guide": "📥 Download User Guide",
        "student_profile": "Student Profile",
        "subject": "Halaqoh / Tahfidz Teacher:",
        "date": "Date:",
        "time": "Time:",
        "name": "Full Name:",
        "class": "Group:", 
        "absen": "Roll Number:",
        "q_header": "Self-Evaluation Form",
        "q_feel": "How would you rate the fluency of your recitation today?",
        "q1": "1. Today I recited (Juz/Surah/Ayah):",
        "q2": "2. Ayahs/Surahs that are already fluent:",
        "q3": "3. Difficulties I faced (Tajweed / Forgetting Ayahs etc):",
        "q4": "4. How I overcame those difficulties:",
        "q5": "5. What I am most grateful for in today's session:",
        "q6": "6. My next memorization/murojaah target:",
        "btn_submit": "Submit Tahfidz Record",
        "warn_name": "Please enter your full name!",
        "success": "Alhamdulillah, {}! Your record has been saved. Stay consistent!",
        
        # --- TEKS PORTAL ORANG TUA ---
        "parent_header": "👨‍👩‍👧 Parent's Download Portal",
        "parent_desc": "Parents/Guardians can monitor the student's memorization progress by downloading the International Tahfidz Report below. Enter the student's Full Name and Roll Number to access.",
        "p_name": "Student's Full Name:",
        "p_absen": "Roll Number:",
        "p_btn": "Access Tahfidz Report",
        "p_error": "Sorry, data not found. Please ensure the name and roll number are correct.",
        "p_success": "Data found! Please download the PDF document below.",
        "btn_dl_rapor": "📥 Download Tahfidz Progress Report ({})",

        "board_header": "🕌 Teacher's Area & Reports",
        "chart_header": "📊 Halaqoh Fluency Analytics - {}",
        "pass_header": "🔒 Tahfidz Teacher Access",
        "pass_desc": "Enter your password to view and download data specific to your halaqoh.",
        "pass_input": "Password:",
        "pass_success": "Password accepted! Ahlan wa sahlan, displaying data for: **{}**",
        "pass_error": "Afwan, incorrect password. Please try again.",
        "filter_time_header": "⏳ Time Range Filter",
        "filter_time_desc": "Select a date range to recap reports weekly or monthly.",
        "start_date": "From Date:",
        "end_date": "To Date:",
        "no_date_data": "No data found for this date range.",
        "print_header": "👤 Print Individual Logbook",
        "print_desc": "Download detailed student track records including notes on difficulties.",
        "select_name": "Select Student Name:",
        "graph_mood": "**Fluency Graph: {}**",
        "last_entry": "**Last Entry:**",
        "difficulty": "Difficulty:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Logbook (Detailed)",
        "gallery_header": "📌 Students' Notes Gallery",
        "gallery_desc": "Click on a student's name to read their detailed notes and targets.",
        "export_header": "💾 Export Full Reports",
        "export_desc": "Download all data and submission recaps for your halaqoh.",
        "btn_dl_all": "📥 Download Report (PDF)",
        "btn_dl_csv": "📥 Download Excel Data (CSV)",
        "btn_dl_rank": "📥 Download Submission Count (CSV)",
        "no_data": "No students have submitted records in this halaqoh yet.",
        "pdf_class_title": "Tahfidz Journal Report - {}", 
        "pdf_ind_title": "Tahfidz Logbook: {}",
        "change_pass_header": "Change Access Password",
        "change_pass_desc": "Change the default password to your own secret password.",
        "new_pass_input": "Enter New Password:",
        "btn_save_pass": "Save New Password",
        "pass_changed_success": "Success! Your password has been changed. Please log in again.",
        "pass_changed_error": "Failed! This password is already in use by another halaqoh."
    }

# ==========================================
# BAGIAN 3: MESIN PEMBUAT PDF (TERMASUK RAPOR INTERNASIONAL PORTRAIT)
# ==========================================

# 1. RAPOR INTERNASIONAL (KHUSUS ORANG TUA - PORTRAIT)
def generate_international_report_card(student_name, student_data):
    pdf = FPDF(orientation='P', unit='mm', format='A4') # PORTRAIT A4
    pdf.add_page()
    
    pdf.set_text_color(25, 135, 84) # Hijau Zamrud
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, txt="TAHFIDZ PROGRESS REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, txt="International Quranic Mutaba'ah Program", ln=True, align='C')
    pdf.ln(8)
    
    info_terbaru = student_data.iloc[-1]
    kelas = str(info_terbaru['kelas'])
    absen = str(info_terbaru['absen'])
    halaqoh = str(info_terbaru['mata_pelajaran'])
    
    # Kotak Identitas Santri
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(240, 248, 245) # Hijau sangat muda
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(45, 8, " Student Name", border=1, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f" {student_name.title()}", border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(45, 8, " Group / Class", border=1, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(50, 8, f" {kelas}", border=1)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(45, 8, " Roll Number", border=1, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f" {absen}", border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(45, 8, " Mentor / Halaqoh", border=1, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f" {halaqoh}", border=1, ln=True)
    
    pdf.ln(10)
    
    # Tabel Riwayat (Header)
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(25, 135, 84) # Hijau pekat
    pdf.set_text_color(255, 255, 255)
    
    # Lebar Kolom: Tgl(30), Surah(65), Kelancaran(35), Target(60)
    pdf.cell(30, 8, "Date", border=1, fill=True, align='C')
    pdf.cell(65, 8, "Memorization (Surah/Ayah)", border=1, fill=True, align='C')
    pdf.cell(35, 8, "Fluency Level", border=1, fill=True, align='C')
    pdf.cell(60, 8, "Next Target", border=1, fill=True, align='C')
    pdf.ln()
    
    # Tabel Riwayat (Isi)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(0, 0, 0)
    
    for idx, row in student_data.iterrows():
        date_str = str(row['waktu_lengkap']).split()[0]
        # Memotong teks kepanjangan & menghilangkan karakter emoji agar PDF tidak error
        surah = str(row['belajar_tentang']).encode('ascii', 'ignore').decode('ascii')[:35]
        target = str(row['target_berikutnya']).encode('ascii', 'ignore').decode('ascii')[:30]
        
        raw_feeling = str(row['feeling']).encode('ascii', 'ignore').decode('ascii').strip()
        # Membersihkan spasi berlebih peninggalan emoji
        fluency_clean = raw_feeling[:20]
        
        pdf.cell(30, 8, f"{date_str}", border=1, align='C')
        pdf.cell(65, 8, f" {surah}", border=1)
        pdf.cell(35, 8, f"{fluency_clean}", border=1, align='C')
        pdf.cell(60, 8, f" {target}", border=1)
        pdf.ln()
        
    pdf.ln(15)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, txt="* This document is computer-generated and serves as an official progress tracker.", ln=True, align='C')
    pdf.cell(0, 5, txt="May Allah bless the journey of memorizing the Holy Quran.", ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1')

# 2. BUKU MUTABAAH DETAIL (GURU) & LAPORAN KELAS
def generate_pdf_report(df, feeling_counts, teks, nama_mapel, tgl_mulai, tgl_akhir):
    pdf = FPDF()
    pdf.add_page()
    clean_mapel = str(nama_mapel).encode('ascii', 'ignore').decode('ascii')
    judul_dinamis = teks["pdf_class_title"].format(clean_mapel)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=judul_dinamis, ln=True, align='C')
    pdf.set_font("Arial", "I", 11)
    teks_periode = f"Periode: {tgl_mulai.strftime('%d/%m/%Y')} - {tgl_akhir.strftime('%d/%m/%Y')}"
    pdf.cell(200, 8, txt=teks_periode, ln=True, align='C')
    pdf.ln(5)

    fig, ax = plt.subplots(figsize=(6, 4))
    clean_labels = [label.encode('ascii', 'ignore').decode('ascii').strip() for label in feeling_counts.index]
    ax.bar(clean_labels, feeling_counts.values, color=['#198754', '#0d6efd', '#ffc107', '#dc3545'])
    ax.set_title(teks["chart_header"].format(clean_mapel).replace("📊 ", ""))
    ax.set_ylabel("Total")
    fig.savefig("temp_chart.png", bbox_inches='tight')
    plt.close(fig) 
    pdf.image("temp_chart.png", x=30, w=150)
    pdf.ln(100) 
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=teks["gallery_header"].replace("📌 ", ""), ln=True)
    for idx, row in df.iterrows():
        name = str(row['name']).encode('ascii', 'ignore').decode('ascii')
        kelas = str(row['kelas']).encode('ascii', 'ignore').decode('ascii')
        absen = str(row['absen']).encode('ascii', 'ignore').decode('ascii')
        waktu = str(row['waktu_lengkap'])
        feeling = str(row['feeling']).encode('ascii', 'ignore').decode('ascii')
        belajar = str(row['belajar_tentang']).encode('ascii', 'ignore').decode('ascii')
        paham = str(row['sudah_paham']).encode('ascii', 'ignore').decode('ascii')
        sulit = str(row['kesulitan']).encode('ascii', 'ignore').decode('ascii')
        atasi = str(row['cara_atasi']).encode('ascii', 'ignore').decode('ascii')
        suka = str(row['hal_disukai']).encode('ascii', 'ignore').decode('ascii')
        target = str(row['target_berikutnya']).encode('ascii', 'ignore').decode('ascii')
        
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 8, txt=f"{idx+1}. {name} ({teks['class']} {kelas} - {absen}) | {waktu} | Kelancaran: {feeling}")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, txt=f"   - {teks['q1']} {belajar}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['q2']} {paham}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['q3']} {sulit}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['q4']} {atasi}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['q5']} {suka}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['q6']} {target}")
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

def generate_individual_pdf(student_name, student_data, grafik_siswa, teks):
    pdf = FPDF()
    pdf.add_page()
    clean_name = str(student_name).encode('ascii', 'ignore').decode('ascii').strip()
    info_terbaru = student_data.iloc[-1]
    clean_kelas = str(info_terbaru['kelas']).encode('ascii', 'ignore').decode('ascii')
    clean_absen = str(info_terbaru['absen']).encode('ascii', 'ignore').decode('ascii')
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=teks["pdf_ind_title"].format(clean_name), ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 8, txt=f"{teks['class']} {clean_kelas} | {teks['absen']} {clean_absen}", ln=True, align='C')
    pdf.ln(5)

    fig, ax = plt.subplots(figsize=(6, 4))
    clean_labels = [label.encode('ascii', 'ignore').decode('ascii').strip() for label in grafik_siswa.index]
    ax.bar(clean_labels, grafik_siswa.values, color='#198754')
    ax.set_title(teks["graph_mood"].format(clean_name).replace("**", ""))
    fig.savefig("temp_ind_chart.png", bbox_inches='tight')
    plt.close(fig) 
    pdf.image("temp_ind_chart.png", x=30, w=150)
    pdf.ln(100) 
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=teks["last_entry"].replace("**", ""), ln=True)
    pdf.ln(2)
    
    for idx, row in student_data.iterrows():
        waktu = str(row['waktu_lengkap'])
        mapel_murid = str(row['mata_pelajaran']).encode('ascii', 'ignore').decode('ascii')
        feeling = str(row['feeling']).encode('ascii', 'ignore').decode('ascii')
        belajar = str(row['belajar_tentang']).encode('ascii', 'ignore').decode('ascii')
        paham = str(row['sudah_paham']).encode('ascii', 'ignore').decode('ascii')
        sulit = str(row['kesulitan']).encode('ascii', 'ignore').decode('ascii')
        atasi = str(row['cara_atasi']).encode('ascii', 'ignore').decode('ascii')
        suka = str(row['hal_disukai']).encode('ascii', 'ignore').decode('ascii')
        target = str(row['target_berikutnya']).encode('ascii', 'ignore').decode('ascii')
        
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 6, txt=f"[{waktu}] {mapel_murid} | Kelancaran: {feeling}")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, txt=f"{teks['q1']} {belajar}")
        pdf.multi_cell(0, 5, txt=f"{teks['q2']} {paham}")
        pdf.multi_cell(0, 5, txt=f"{teks['q3']} {sulit}")
        pdf.multi_cell(0, 5, txt=f"{teks['q4']} {atasi}")
        pdf.multi_cell(0, 5, txt=f"{teks['q5']} {suka}")
        pdf.multi_cell(0, 5, txt=f"{teks['q6']} {target}")
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

def generate_guide_pdf(lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    if lang == "Indonesia":
        pdf.cell(200, 10, txt="Panduan Penggunaan Jurnal Tahfidz", ln=True, align='C')
    else:
        pdf.cell(200, 10, txt="Tahfidz Journal - User Guide", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# BAGIAN 4: ANTARMUKA PENGGUNA (UI) & CSS ISLAMI
# ==========================================
with st.sidebar:
    st.header(t["teacher_settings"])
    bg_color = st.color_picker(t["bg_color"], "#F4FAF5")
    st.divider()
    st.header(t["help_center"])
    pdf_panduan = generate_guide_pdf(language)
    st.download_button(
        label=t["btn_dl_guide"],
        data=pdf_panduan,
        file_name='User_Guide_Jurnal_Tahfidz.pdf',
        mime='application/pdf'
    )

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .quote-box {{
        background-color: #ffffff; border-left: 6px solid #198754;
        padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px; text-align: center;
    }}
    .arabic-text {{ font-size: 28px; color: #198754; margin-bottom: 15px; line-height: 1.8; }}
    .translation-text {{ font-size: 16px; font-style: italic; color: #4a4a4a; }}
    </style>
""", unsafe_allow_html=True)

col_logo, col_judul = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", use_column_width=True)
    elif os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
with col_judul:
    st.title(t["title"])
    st.write(t["subtitle"])

st.markdown(f"""
<div class="quote-box">
    <div class="arabic-text">{quote_arab}</div>
    <div class="translation-text">"{quote_arti}"</div>
</div>
""", unsafe_allow_html=True)

# FORMULIR SANTRI
with st.form("pennant_form", clear_on_submit=True):
    st.subheader(t["student_profile"])
    daftar_mapel = [
        "Halaqoh Ustadz Mursanto", "Halaqoh Ustadz M. Tohir Asyhuri", 
        "Halaqoh Ustadz Arif Subkhan", "Halaqoh Ustadz Ach. Jalilul Chakam", 
        "Halaqoh Ustadz Ach. Wahyu Zakariya", "Lainnya"
    ]
    pilihan_mapel = st.selectbox(t["subject"], daftar_mapel)
    
    col_date, col_time = st.columns(2)
    with col_date: tanggal = st.date_input(t["date"])
    with col_time: waktu = st.time_input(t["time"])
        
    name = st.text_input(t["name"])
    
    col_kelas, col_absen = st.columns(2)
    with col_kelas:
        daftar_kelas = ["7A", "7B", "7C", "7D", "7E", "7F", "8A", "8B", "8C", "8D", "8E", "8F", "9A", "9B", "9C", "9D", "9E", "9F"]
        kelas = st.selectbox(t["class"], daftar_kelas)
    with col_absen:
        absen = st.number_input(t["absen"], min_value=1, max_value=50, step=1)
    
    st.divider()
    st.subheader(t["q_header"])
    
    pilihan_kelancaran = ["🟢 Sangat Lancar", "🔵 Lancar", "🟡 Cukup", "🔴 Perlu Bimbingan"] if language == "Indonesia" else ["🟢 Very Fluent", "🔵 Fluent", "🟡 Fair", "🔴 Needs Guidance"]
        
    feeling = st.radio(t["q_feel"], pilihan_kelancaran, horizontal=True)
    belajar_tentang = st.text_area(t["q1"])
    sudah_paham = st.text_area(t["q2"])
    kesulitan = st.text_area(t["q3"])
    cara_atasi = st.text_area(t["q4"])
    hal_disukai = st.text_area(t["q5"])
    target_berikutnya = st.text_input(t["q6"])
    
    if st.form_submit_button(t["btn_submit"]):
        if name.strip() == "":
            st.warning(t["warn_name"])
        else:
            waktu_lengkap_str = f"{tanggal.strftime('%Y-%m-%d')} {waktu.strftime('%H:%M')}"
            insert_data(waktu_lengkap_str, pilihan_mapel, name, kelas, str(absen), feeling, belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya)
            st.success(t["success"].format(name))

# ==========================================
# BAGIAN 5: PORTAL ORANG TUA & RUANG GURU
# ==========================================
st.divider()
df_students_master = get_all_data()

if not df_students_master.empty:
    
    # --- FITUR BARU: PORTAL ORANG TUA ---
    with st.expander(t["parent_header"], expanded=False):
        st.write(t["parent_desc"])
        with st.form("form_ortu"):
            col_ortu1, col_ortu2 = st.columns([3, 1])
            with col_ortu1:
                input_nama_ortu = st.text_input(t["p_name"])
            with col_ortu2:
                input_absen_ortu = st.number_input(t["p_absen"], min_value=1, max_value=50, step=1)
            
            submit_ortu = st.form_submit_button(t["p_btn"])
            
        if submit_ortu:
            if input_nama_ortu.strip() == "":
                st.warning("Mohon masukkan nama santri.")
            else:
                # Memeriksa kecocokan nama (mengabaikan huruf besar/kecil) dan nomor absen
                mask_ortu = (df_students_master['name'].str.lower() == input_nama_ortu.strip().lower()) & (df_students_master['absen'] == str(input_absen_ortu))
                df_anak = df_students_master[mask_ortu]
                
                if not df_anak.empty:
                    st.success(t["p_success"])
                    pdf_rapor_ortu = generate_international_report_card(input_nama_ortu.strip(), df_anak)
                    st.download_button(
                        label=t["btn_dl_rapor"].format(input_nama_ortu.strip()),
                        data=pdf_rapor_ortu,
                        file_name=f'Tahfidz_Report_{input_nama_ortu.strip()}.pdf',
                        mime='application/pdf'
                    )
                else:
                    st.error(t["p_error"])
    
    st.divider()

    # --- RUANG GURU ---
    st.header(t["board_header"])
    st.write(t["pass_desc"])
    password_guru = st.text_input(t["pass_input"], type="password")
    mapel_terkunci = get_mapel_by_password(password_guru)
    
    if mapel_terkunci:
        st.success(t["pass_success"].format(mapel_terkunci))
        st.divider()
        
        tab_laporan, tab_pengaturan = st.tabs(["📊 Dashboard Laporan Halaqoh", "⚙️ Pengaturan Akun"])
        
        with tab_laporan:
            if mapel_terkunci == "Semua Halaqoh":
                df_students_mapel = df_students_master
                judul_analitik = "Seluruh Sekolah"
            else:
                df_students_mapel = df_students_master[df_students_master['mata_pelajaran'] == mapel_terkunci]
                judul_analitik = mapel_terkunci
                
            if df_students_mapel.empty:
                st.info(t["no_data"])
            else:
                st.subheader(t["filter_time_header"])
                st.write(t["filter_time_desc"])
                
                df_students_mapel['tanggal_asli'] = pd.to_datetime(df_students_mapel['waktu_lengkap']).dt.date
                tanggal_terawal = df_students_mapel['tanggal_asli'].min()
                tanggal_terakhir = df_students_mapel['tanggal_asli'].max()
                
                col_start, col_end = st.columns(2)
                with col_start: start_date = st.date_input(t["start_date"], tanggal_terawal)
                with col_end: end_date = st.date_input(t["end_date"], tanggal_terakhir)
                
                mask = (df_students_mapel['tanggal_asli'] >= start_date) & (df_students_mapel['tanggal_asli'] <= end_date)
                df_filtered = df_students_mapel.loc[mask]
                
                if df_filtered.empty:
                    st.warning(t["no_date_data"])
                else:
                    st.divider()
                    st.subheader(t["chart_header"].format(judul_analitik))
                    feeling_counts = df_filtered['feeling'].value_counts()
                    st.bar_chart(feeling_counts)
                    
                    st.divider()
                    st.header(t["print_header"])
                    st.write(t["print_desc"])
                    
                    daftar_nama = df_filtered['name'].unique()
                    pilihan_siswa = st.selectbox(t["select_name"], daftar_nama)
                    
                    data_siswa = df_filtered[df_filtered['name'] == pilihan_siswa]
                    grafik_siswa = data_siswa['feeling'].value_counts()
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.write(t["graph_mood"].format(pilihan_siswa))
                        st.bar_chart(grafik_siswa, color="#198754") 
                        
                    with col2:
                        st.write(t["last_entry"])
                        if len(data_siswa) > 0:
                            info_terakhir = data_siswa.iloc[-1]
                            st.info(f"📅 {info_terakhir['waktu_lengkap']} | **{info_terakhir['mata_pelajaran']}**\n\n**{t['difficulty']}** {info_terakhir['kesulitan']}\n\n**{t['target']}** {info_terakhir['target_berikutnya']}")
                    
                    pdf_individu = generate_individual_pdf(pilihan_siswa, data_siswa, grafik_siswa, t)
                    st.download_button(
                        label=t["btn_dl_ind"],
                        data=pdf_individu,
                        file_name=f'Buku_Mutabaah_{pilihan_siswa}.pdf',
                        mime='application/pdf'
                    )
                    
                    st.divider()
                    st.subheader(t["gallery_header"])
                    st.write(t["gallery_desc"])
                    for idx, row in df_filtered.iterrows():
                        with st.expander(f"📖 {row['name']} ({t['class']} {row['kelas']} - {t['absen']} {row['absen']}) | {row['mata_pelajaran']}"):
                            st.write(f"**{t['time']}** {row['waktu_lengkap']} | **Kelancaran:** {row['feeling']}")
                            st.write(f"**{t['q1']}** {row['belajar_tentang']}")
                            st.write(f"**{t['q2']}** {row['sudah_paham']}")
                            st.write(f"**{t['q3']}** {row['kesulitan']}")
                            st.write(f"**{t['q4']}** {row['cara_atasi']}")
                            st.write(f"**{t['q5']}** {row['hal_disukai']}")
                            st.write(f"**{t['q6']}** {row['target_berikutnya']}")
                                
                    st.divider()
                    st.subheader(t["export_header"])
                    st.write(t["export_desc"])
                    
                    col_pdf, col_csv, col_rank = st.columns(3)
                    with col_pdf:
                        pdf_data = generate_pdf_report(df_filtered, feeling_counts, t, judul_analitik, start_date, end_date)
                        st.download_button(
                            label=t["btn_dl_all"],
                            data=pdf_data,
                            file_name=f'Laporan_Tahfidz_{judul_analitik}.pdf',
                            mime='application/pdf'
                        )
                    with col_csv:
                        csv_export = df_filtered.drop(columns=['tanggal_asli'])
                        csv_data = csv_export.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=t["btn_dl_csv"],
                            data=csv_data,
                            file_name=f'Data_Tahfidz_{judul_analitik}_{start_date}_hingga_{end_date}.csv',
                            mime='text/csv'
                        )
                    with col_rank:
                        df_filtered['nama_kelas'] = df_filtered['name'] + " (" + df_filtered['kelas'] + ")"
                        peringkat_df = df_filtered['nama_kelas'].value_counts().reset_index()
                        peringkat_df.columns = ['Nama Santri (Kelompok)', 'Jumlah Setoran']
                        peringkat_df.index = peringkat_df.index + 1
                        
                        csv_peringkat = peringkat_df.to_csv(index_label='Peringkat').encode('utf-8')
                        st.download_button(
                            label=t["btn_dl_rank"],
                            data=csv_peringkat,
                            file_name=f'Rekap_Setoran_{judul_analitik}_{start_date}_hingga_{end_date}.csv',
                            mime='text/csv'
                        )
        
        with tab_pengaturan:
            st.subheader(t["change_pass_header"])
            st.info(t["change_pass_desc"])
            with st.form("form_ubah_sandi"):
                new_pass = st.text_input(t["new_pass_input"], type="password")
                if st.form_submit_button(t["btn_save_pass"]):
                    if new_pass.strip() == "":
                        st.error("Kata sandi tidak boleh kosong!")
                    else:
                        berhasil_diubah = update_password(mapel_terkunci, new_pass)
                        if berhasil_diubah:
                            st.success(t["pass_changed_success"])
                        else:
                            st.error(t["pass_changed_error"])

    elif password_guru != "":
        st.error(t["pass_error"])
else:
    st.info("Aplikasi siap digunakan. Silakan masukkan data setoran pertama.")
