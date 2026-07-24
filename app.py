import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import datetime

# ==========================================
# BAGIAN 1: PENGATURAN DATABASE (SQLITE)
# ==========================================
def init_db():
    conn = sqlite3.connect('jurnal_sekolah_v7.db')
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
            ("Matematika", "passMTK"),
            ("Bahasa Indonesia", "passBINDO"),
            ("Bahasa Inggris", "passBING"),
            ("Ilmu Pengetahuan Alam (IPA)", "passIPA"),
            ("Ilmu Pengetahuan Sosial (IPS)", "passIPS"),
            ("Pendidikan Agama", "passAGAMA"),
            ("PPKn", "passPKN"),
            ("Seni Budaya", "passSENI"),
            ("PJOK", "passPJOK"),
            ("Prakarya", "passPRAKARYA"),
            ("Bahasa Jawa", "passJAWA"),
            ("ICT", "passICT"),
            ("Bimbingan Konseling", "passBK"),
            ("Semua Mapel", "adminSUPER")
        ]
        c.executemany('INSERT OR IGNORE INTO guru_auth (mata_pelajaran, password) VALUES (?, ?)', password_bawaan)
        
    conn.commit()
    conn.close()

def insert_data(waktu_lengkap, mapel, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target):
    conn = sqlite3.connect('jurnal_sekolah_v7.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reflections (waktu_lengkap, mata_pelajaran, name, kelas, absen, feeling, belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (waktu_lengkap, mapel, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect('jurnal_sekolah_v7.db')
    df = pd.read_sql_query("SELECT * FROM reflections", conn)
    conn.close()
    return df

def get_mapel_by_password(pwd):
    conn = sqlite3.connect('jurnal_sekolah_v7.db')
    c = conn.cursor()
    c.execute('SELECT mata_pelajaran FROM guru_auth WHERE password = ?', (pwd,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def update_password(mapel, new_pwd):
    conn = sqlite3.connect('jurnal_sekolah_v7.db')
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
# BAGIAN 2: KAMUS BAHASA (TRANSLATION)
# ==========================================
st.set_page_config(page_title="Learning Reflection Journal", page_icon="📝", layout="centered")

with st.sidebar:
    language = st.selectbox("🌐 Pilih Bahasa / Language:", ["Indonesia", "English"])
    st.divider()
    
if language == "Indonesia":
    t = {
        "title": "Learning Reflection Journal",
        "subtitle": "Mari sejenak merefleksikan apa yang sudah kita pelajari hari ini.",
        "teacher_settings": "🎨 Pengaturan Guru",
        "bg_color": "Pilih Warna Latar Web:",
        "help_center": "📖 Pusat Bantuan",
        "btn_dl_guide": "📥 Download Panduan Penggunaan",
        "student_profile": "Profil Siswa",
        "subject": "Mata Pelajaran:",
        "date": "Tanggal:",
        "time": "Waktu:",
        "name": "Nama Lengkap:",
        "class": "Kelas:",
        "absen": "Nomor Absen:",
        "q_header": "6 Pertanyaan Refleksi",
        "q_feel": "Bagaimana perasaanmu setelah pembelajaran hari ini?",
        "q1": "1. Hari ini saya belajar tentang:",
        "q2": "2. Saya sudah memahami:",
        "q3": "3. Saya masih mengalami kesulitan pada:",
        "q4": "4. Cara saya mengatasinya:",
        "q5": "5. Hal yang paling saya sukai hari ini:",
        "q6": "6. Target saya untuk pembelajaran berikutnya:",
        "btn_submit": "Kirim Jurnal Refleksiku!",
        "warn_name": "Tolong masukkan nama lengkapmu!",
        "success": "Hebat, {}! Jurnal refleksimu telah tersimpan.",
        "board_header": "🏫 Papan Data Refleksi Kelas",
        "chart_header": "📊 Analitik Suasana Kelas - {}",
        "pass_header": "🔒 Area Unduh Data Guru",
        "pass_desc": "Masukkan kata sandi guru Anda untuk melihat data khusus mata pelajaran Anda.",
        "pass_input": "Kata Sandi (Password):",
        "pass_success": "Sandi diterima! Menampilkan data pelajaran: **{}**",
        "pass_error": "Kata sandi salah. Silakan coba lagi.",
        "filter_time_header": "⏳ Filter Rentang Waktu",
        "filter_time_desc": "Pilih rentang tanggal untuk merekap laporan per minggu, per bulan, atau kustom.",
        "start_date": "Dari Tanggal:",
        "end_date": "Sampai Tanggal:",
        "no_date_data": "Tidak ada data pada rentang tanggal tersebut.",
        "print_header": "👤 Cetak Portofolio Individu",
        "print_desc": "Pilih nama siswa untuk mengunduh rekam jejak jurnalnya.",
        "select_name": "Pilih Nama Siswa:",
        "graph_mood": "**Grafik Perasaan: {}**",
        "last_entry": "**Riwayat Entri Terakhir:**",
        "difficulty": "Kesulitan:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Portofolio {} (PDF)",
        "gallery_header": "📌 Galeri Jurnal Kelas",
        "gallery_desc": "Klik pada nama siswa untuk membaca detail refleksinya.",
        "export_header": "💾 Export Laporan Kelas",
        "export_desc": "Unduh seluruh data refleksi dan peringkat siswa untuk mata pelajaran Anda sesuai rentang waktu di atas.",
        "btn_dl_all": "📥 Download Laporan (PDF)",
        "btn_dl_csv": "📥 Download Data (CSV)",
        "btn_dl_rank": "📥 Download Peringkat (CSV)",
        "no_data": "Belum ada data masuk untuk mata pelajaran ini.",
        "pdf_class_title": "Laporan Jurnal Refleksi - {}", 
        "pdf_ind_title": "Portofolio Jurnal: {}",
        "change_pass_header": "⚙️ Pengaturan: Ubah Kata Sandi",
        "change_pass_desc": "Anda dapat mengganti kata sandi bawaan dengan kata sandi rahasia Anda sendiri.",
        "new_pass_input": "Masukkan Kata Sandi Baru:",
        "btn_save_pass": "Simpan Kata Sandi Baru",
        "pass_changed_success": "Berhasil! Sandi Anda telah diubah. Halaman akan dimuat ulang, silakan masukkan sandi baru Anda.",
        "pass_changed_error": "Gagal! Kata sandi ini sudah digunakan oleh mapel lain. Pilih sandi kombinasi lain."
    }
else:
    t = {
        "title": "Learning Reflection Journal",
        "subtitle": "Let's take a moment to reflect on what we have learned today.",
        "teacher_settings": "🎨 Teacher Settings",
        "bg_color": "Select Web Background Color:",
        "help_center": "📖 Help Center",
        "btn_dl_guide": "📥 Download User Guide",
        "student_profile": "Student Profile",
        "subject": "Subject:",
        "date": "Date:",
        "time": "Time:",
        "name": "Full Name:",
        "class": "Class:",
        "absen": "Roll Number:",
        "q_header": "6 Reflection Questions",
        "q_feel": "How do you feel after today's lesson?",
        "q1": "1. Today I learned about:",
        "q2": "2. I have understood:",
        "q3": "3. I am still struggling with:",
        "q4": "4. How I overcome it:",
        "q5": "5. The thing I liked most today:",
        "q6": "6. My target for the next lesson:",
        "btn_submit": "Submit My Reflection Journal!",
        "warn_name": "Please enter your full name!",
        "success": "Great job, {}! Your reflection journal has been saved.",
        "board_header": "🏫 Class Reflection Data Board",
        "chart_header": "📊 Class Mood Analytics - {}",
        "pass_header": "🔒 Teacher Download Area",
        "pass_desc": "Enter your teacher password to view data specific to your subject.",
        "pass_input": "Password:",
        "pass_success": "Password accepted! Displaying data for: **{}**",
        "pass_error": "Incorrect password. Please try again.",
        "filter_time_header": "⏳ Time Range Filter",
        "filter_time_desc": "Select a date range to recap reports weekly, monthly, or custom.",
        "start_date": "From Date:",
        "end_date": "To Date:",
        "no_date_data": "No data found for this date range.",
        "print_header": "👤 Print Individual Portfolio",
        "print_desc": "Select a student's name to download their journal track record.",
        "select_name": "Select Student Name:",
        "graph_mood": "**Mood Graph: {}**",
        "last_entry": "**Last Entry History:**",
        "difficulty": "Struggling with:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Portfolio of {} (PDF)",
        "gallery_header": "📌 Class Journal Gallery",
        "gallery_desc": "Click on a student's name to read their reflection details.",
        "export_header": "💾 Export Class Report",
        "export_desc": "Download all student reflection data and leaderboard for your subject based on the time range above.",
        "btn_dl_all": "📥 Download Report (PDF)",
        "btn_dl_csv": "📥 Download Excel Data (CSV)",
        "btn_dl_rank": "📥 Download Leaderboard (CSV)",
        "no_data": "No data submitted yet for this subject.",
        "pdf_class_title": "Reflection Journal Report - {}", 
        "pdf_ind_title": "Journal Portfolio: {}",
        "change_pass_header": "⚙️ Settings: Change Password",
        "change_pass_desc": "You can change the default password to your own secret password.",
        "new_pass_input": "Enter New Password:",
        "btn_save_pass": "Save New Password",
        "pass_changed_success": "Success! Your password has been changed. Please log in again with the new password.",
        "pass_changed_error": "Failed! This password is already in use by another subject. Please choose another combination."
    }

# ==========================================
# BAGIAN 3: MESIN PEMBUAT PDF
# ==========================================
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
    ax.bar(clean_labels, feeling_counts.values, color=['#007BFF', '#28A745', '#FFC107', '#DC3545'])
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
        pdf.multi_cell(0, 8, txt=f"{idx+1}. {name} ({kelas} - {absen}) | {waktu} | Mood: {feeling}")
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
    ax.bar(clean_labels, grafik_siswa.values, color='#FFC107')
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
        pdf.multi_cell(0, 6, txt=f"[{waktu}] {mapel_murid} | Mood: {feeling}")
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
        pdf.cell(200, 10, txt="Panduan Penggunaan Learning Reflection Journal", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="BAGIAN A: Panduan Untuk Siswa (Cara Mengisi)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Buka aplikasi dan pilih bahasa di menu samping.")
        pdf.multi_cell(0, 6, txt="2. Isi profil dan pilih Mata Pelajaran yang baru saja kamu ikuti.")
        pdf.multi_cell(0, 6, txt="3. Jawab 6 pertanyaan refleksi dan klik tombol Kirim.")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="BAGIAN B: Panduan Untuk Guru (Cara Mengelola Data)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Di area guru, masukkan kata sandi khusus mapel Anda.")
        pdf.multi_cell(0, 6, txt="2. Gunakan 'Filter Rentang Waktu' untuk merekap data per minggu/bulan.")
        pdf.multi_cell(0, 6, txt="3. Anda bisa mengunduh portofolio siswa atau laporan kelas (PDF/Excel).")
    else:
        pdf.cell(200, 10, txt="Learning Reflection Journal - User Guide", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="PART A: Guide for Students", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Open the app and select your language in the sidebar.")
        pdf.multi_cell(0, 6, txt="2. Fill in your profile and select the Subject.")
        pdf.multi_cell(0, 6, txt="3. Answer the reflection questions and submit.")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="PART B: Guide for Teachers", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. In the teacher area, enter your specific subject password.")
        pdf.multi_cell(0, 6, txt="2. Use the 'Time Range Filter' to recap data weekly/monthly.")
        pdf.multi_cell(0, 6, txt="3. You can download portfolios or class reports (PDF/Excel).")

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# BAGIAN 4: ANTARMUKA PENGGUNA (UI) STREAMLIT
# ==========================================
with st.sidebar:
    st.header(t["teacher_settings"])
    bg_color = st.color_picker(t["bg_color"], "#F4F6F9")
    
    st.divider()
    
    st.header(t["help_center"])
    pdf_panduan = generate_guide_pdf(language)
    st.download_button(
        label=t["btn_dl_guide"],
        data=pdf_panduan,
        file_name='User_Guide_Reflection_Journal.pdf',
        mime='application/pdf'
    )

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

# --- PEMBARUAN TATA LETAK: LOGO 1 DAN LOGO 2 ---
col_logo_kiri, col_judul, col_logo_kanan = st.columns([1.5, 5, 1.5])

with col_logo_kiri:
    if os.path.exists("logo1.png"):
        st.image("logo1.png", use_column_width=True)
    elif os.path.exists("logo1.jpg"):
        st.image("logo1.jpg", use_column_width=True)

with col_judul:
    st.markdown(f"<h1 style='text-align: center;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

with col_logo_kanan:
    if os.path.exists("logo2.png"):
        st.image("logo2.png", use_column_width=True)
    elif os.path.exists("logo2.jpg"):
        st.image("logo2.jpg", use_column_width=True)

st.divider()

with st.form("pennant_form", clear_on_submit=True):
    st.subheader(t["student_profile"])
    
    daftar_mapel = [
        "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Ilmu Pengetahuan Alam (IPA)", 
        "Ilmu Pengetahuan Sosial (IPS)", "Pendidikan Agama", "PPKn", 
        "Seni Budaya", "PJOK", "Prakarya", "Bahasa Jawa", "ICT", "Bimbingan Konseling", "Lainnya"
    ]
    pilihan_mapel = st.selectbox(t["subject"], daftar_mapel)
    
    col_date, col_time = st.columns(2)
    with col_date:
        tanggal = st.date_input(t["date"])
    with col_time:
        waktu = st.time_input(t["time"])
        
    name = st.text_input(t["name"])
    
    col_kelas, col_absen = st.columns(2)
    with col_kelas:
        daftar_kelas = [
            "7A", "7B", "7C", "7D", "7E", "7F",
            "8A", "8B", "8C", "8D", "8E", "8F",
            "9A", "9B", "9C", "9D", "9E", "9F"
        ]
        kelas = st.selectbox(t["class"], daftar_kelas)
    with col_absen:
        absen = st.number_input(t["absen"], min_value=1, max_value=50, step=1)
    
    st.divider()
    st.subheader(t["q_header"])
    
    feeling = st.radio(t["q_feel"], 
                       ["🤩 Sangat Antusias / Very Excited", "😊 Senang / Happy", "🤔 Bingung / Confused", "😴 Lelah / Tired"], horizontal=True)
    
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
            tanggal_str = tanggal.strftime("%Y-%m-%d")
            waktu_str = waktu.strftime("%H:%M")
            waktu_lengkap_str = f"{tanggal_str} {waktu_str}"
            
            insert_data(waktu_lengkap_str, pilihan_mapel, name, kelas, str(absen), feeling, 
                        belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya)
            st.success(t["success"].format(name))

# ==========================================
# BAGIAN 5: ANALITIK & FILTER WAKTU/MAPEL
# ==========================================
st.divider()
st.header(t["board_header"])

df_students_master = get_all_data()

if not df_students_master.empty:
    
    st.subheader(t["pass_header"])
    st.write(t["pass_desc"])
    
    password_guru = st.text_input(t["pass_input"], type="password")
    mapel_terkunci = get_mapel_by_password(password_guru)
    
    if mapel_terkunci:
        st.success(t["pass_success"].format(mapel_terkunci))
        st.divider()
        
        # 1. PENYARINGAN MATA PELAJARAN
        if mapel_terkunci == "Semua Mapel":
            df_students_mapel = df_students_master
            judul_analitik = "Seluruh Sekolah"
        else:
            df_students_mapel = df_students_master[df_students_master['mata_pelajaran'] == mapel_terkunci]
            judul_analitik = mapel_terkunci
            
        if df_students_mapel.empty:
            st.info(t["no_data"])
        else:
            # 2. PENYARINGAN RENTANG WAKTU
            st.subheader(t["filter_time_header"])
            st.write(t["filter_time_desc"])
            
            df_students_mapel['tanggal_asli'] = pd.to_datetime(df_students_mapel['waktu_lengkap']).dt.date
            tanggal_terawal = df_students_mapel['tanggal_asli'].min()
            tanggal_terakhir = df_students_mapel['tanggal_asli'].max()
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(t["start_date"], tanggal_terawal)
            with col_end:
                end_date = st.date_input(t["end_date"], tanggal_terakhir)
            
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
                    st.bar_chart(grafik_siswa, color="#28A745") 
                    
                with col2:
                    st.write(t["last_entry"])
                    if len(data_siswa) > 0:
                        info_terakhir = data_siswa.iloc[-1]
                        st.info(f"📅 {info_terakhir['waktu_lengkap']} | **{info_terakhir['mata_pelajaran']}**\n\n**{t['difficulty']}** {info_terakhir['kesulitan']}\n\n**{t['target']}** {info_terakhir['target_berikutnya']}")
                
                pdf_individu = generate_individual_pdf(pilihan_siswa, data_siswa, grafik_siswa, t)
                st.download_button(
                    label=t["btn_dl_ind"].format(pilihan_siswa),
                    data=pdf_individu,
                    file_name=f'Portfolio_{pilihan_siswa}.pdf',
                    mime='application/pdf'
                )
                
                st.divider()
                st.subheader(t["gallery_header"])
                st.write(t["gallery_desc"])
                
                for idx, row in df_filtered.iterrows():
                    with st.expander(f"📖 {row['name']} ({t['class']} {row['kelas']} - {t['absen']} {row['absen']}) | {row['mata_pelajaran']}"):
                        st.write(f"**{t['time']}** {row['waktu_lengkap']} | **Mood:** {row['feeling']}")
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
                        file_name=f'Laporan_Refleksi_{judul_analitik}.pdf',
                        mime='application/pdf'
                    )
                    
                with col_csv:
                    csv_export = df_filtered.drop(columns=['tanggal_asli'])
                    csv_data = csv_export.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=t["btn_dl_csv"],
                        data=csv_data,
                        file_name=f'Data_{judul_analitik}_{start_date}_hingga_{end_date}.csv',
                        mime='text/csv'
                    )
                    
                with col_rank:
                    df_filtered['nama_kelas'] = df_filtered['name'] + " (" + df_filtered['kelas'] + ")"
                    peringkat_df = df_filtered['nama_kelas'].value_counts().reset_index()
                    peringkat_df.columns = ['Nama Siswa (Kelas)', 'Jumlah Jurnal']
                    peringkat_df.index = peringkat_df.index + 1
                    
                    csv_peringkat = peringkat_df.to_csv(index_label='Peringkat').encode('utf-8')
                    st.download_button(
                        label=t["btn_dl_rank"],
                        data=csv_peringkat,
                        file_name=f'Peringkat_Siswa_{judul_analitik}_{start_date}_hingga_{end_date}.csv',
                        mime='text/csv'
                    )
        
        # Fitur Ubah Kata Sandi
        st.divider()
        st.subheader(t["change_pass_header"])
        st.info(t["change_pass_desc"])
        
        col_form, _ = st.columns([2, 1])
        with col_form:
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
    st.info(t["no_data"])
