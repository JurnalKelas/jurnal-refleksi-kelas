import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import datetime

# ==========================================
# BAGIAN 1: PENGATURAN DATABASE (SQLITE) - VERSI 6
# ==========================================
def init_db():
    conn = sqlite3.connect('kelas7_english_v6.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_lengkap TEXT,
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
    conn.commit()
    conn.close()

def insert_data(waktu_lengkap, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target):
    conn = sqlite3.connect('kelas7_english_v6.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reflections (waktu_lengkap, name, kelas, absen, feeling, belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (waktu_lengkap, name, kelas, absen, feeling, belajar, paham, sulit, atasi, suka, target))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect('kelas7_english_v6.db')
    df = pd.read_sql_query("SELECT * FROM reflections", conn)
    conn.close()
    return df

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
        "title": "📝 Learning Reflection Journal",
        "subtitle": "Mari sejenak merefleksikan apa yang sudah kita pelajari hari ini.",
        "teacher_settings": "🎨 Pengaturan Guru",
        "bg_color": "Pilih Warna Latar Web:",
        "help_center": "📖 Pusat Bantuan",
        "btn_dl_guide": "📥 Download Panduan Penggunaan",
        "student_profile": "Profil Siswa",
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
        "chart_header": "📊 Analitik Suasana Kelas",
        "print_header": "👤 Cetak Portofolio Individu",
        "print_desc": "Pilih nama siswa untuk mengunduh rekam jejak jurnalnya secara utuh.",
        "select_name": "Pilih Nama Siswa:",
        "graph_mood": "**Grafik Perasaan: {}**",
        "last_entry": "**Riwayat Entri Terakhir:**",
        "difficulty": "Kesulitan:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Portofolio {} (PDF)",
        "gallery_header": "📌 Galeri Jurnal Kelas",
        "gallery_desc": "Klik pada nama siswa untuk membaca detail refleksinya.",
        "export_header": "💾 Export Laporan Kelas",
        "export_desc": "Unduh rangkuman singkat jurnal refleksi seluruh siswa hari ini.",
        "btn_dl_all": "📥 Download Rangkuman Kelas (PDF)",
        "no_data": "Belum ada jurnal yang masuk hari ini.",
        "pdf_class_title": "Laporan Jurnal Refleksi Kelas",
        "pdf_ind_title": "Portofolio Jurnal: {}"
    }
else:
    t = {
        "title": "📝 Learning Reflection Journal",
        "subtitle": "Let's take a moment to reflect on what we have learned today.",
        "teacher_settings": "🎨 Teacher Settings",
        "bg_color": "Select Web Background Color:",
        "help_center": "📖 Help Center",
        "btn_dl_guide": "📥 Download User Guide",
        "student_profile": "Student Profile",
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
        "chart_header": "📊 Class Mood Analytics",
        "print_header": "👤 Print Individual Portfolio",
        "print_desc": "Select a student's name to download their full journal track record.",
        "select_name": "Select Student Name:",
        "graph_mood": "**Mood Graph: {}**",
        "last_entry": "**Last Entry History:**",
        "difficulty": "Struggling with:",
        "target": "Target:",
        "btn_dl_ind": "📥 Download Portfolio of {} (PDF)",
        "gallery_header": "📌 Class Journal Gallery",
        "gallery_desc": "Click on a student's name to read their reflection details.",
        "export_header": "💾 Export Class Report",
        "export_desc": "Download a brief summary of all students' reflection journals today.",
        "btn_dl_all": "📥 Download Class Summary (PDF)",
        "no_data": "No journals submitted today.",
        "pdf_class_title": "Class Reflection Journal Report",
        "pdf_ind_title": "Journal Portfolio: {}"
    }

# ==========================================
# BAGIAN 3: MESIN PEMBUAT PDF
# ==========================================
def generate_pdf_report(df, feeling_counts, teks):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=teks["pdf_class_title"], ln=True, align='C')
    pdf.ln(10)

    fig, ax = plt.subplots(figsize=(6, 4))
    clean_labels = [label.encode('ascii', 'ignore').decode('ascii').strip() for label in feeling_counts.index]
    ax.bar(clean_labels, feeling_counts.values, color=['#007BFF', '#28A745', '#FFC107', '#DC3545'])
    ax.set_title(teks["chart_header"].replace("📊 ", ""))
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
        feeling = str(row['feeling']).encode('ascii', 'ignore').decode('ascii')
        kesulitan = str(row['kesulitan']).encode('ascii', 'ignore').decode('ascii')
        target = str(row['target_berikutnya']).encode('ascii', 'ignore').decode('ascii')
        
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 8, txt=f"{idx+1}. {name} ({kelas} - {absen}) | Mood: {feeling}")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, txt=f"   - {teks['difficulty']} {kesulitan}")
        pdf.multi_cell(0, 6, txt=f"   - {teks['target']} {target}")
        pdf.ln(3)

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
        feeling = str(row['feeling']).encode('ascii', 'ignore').decode('ascii')
        belajar = str(row['belajar_tentang']).encode('ascii', 'ignore').decode('ascii')
        paham = str(row['sudah_paham']).encode('ascii', 'ignore').decode('ascii')
        sulit = str(row['kesulitan']).encode('ascii', 'ignore').decode('ascii')
        atasi = str(row['cara_atasi']).encode('ascii', 'ignore').decode('ascii')
        suka = str(row['hal_disukai']).encode('ascii', 'ignore').decode('ascii')
        target = str(row['target_berikutnya']).encode('ascii', 'ignore').decode('ascii')
        
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 6, txt=f"[{waktu}] Mood: {feeling}")
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
        pdf.cell(200, 8, txt="BAGIAN A: Panduan Untuk Siswa (Cara Mengisi Jurnal)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Buka aplikasi dan pilih bahasa di menu samping (kiri atas).")
        pdf.multi_cell(0, 6, txt="2. Isi profil: Tanggal, Waktu, Nama, Kelas, dan Nomor Absen.")
        pdf.multi_cell(0, 6, txt="3. Pilih emoji yang paling menggambarkan perasaanmu.")
        pdf.multi_cell(0, 6, txt="4. Jawab 6 pertanyaan refleksi (kamu bebas mengetik panjang).")
        pdf.multi_cell(0, 6, txt="5. Klik tombol 'Kirim Jurnal Refleksiku!' hingga muncul pesan berhasil.")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="BAGIAN B: Panduan Untuk Guru (Cara Mengelola Data)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Ubah warna latar di menu 'Pengaturan Guru' di sidebar.")
        pdf.multi_cell(0, 6, txt="2. Gulir ke bawah untuk melihat grafik suasana (mood) kelas terkini.")
        pdf.multi_cell(0, 6, txt="3. Di bagian 'Cetak Portofolio', pilih nama 1 siswa untuk melihat grafik pribadinya dan mengunduh riwayat lengkapnya (PDF).")
        pdf.multi_cell(0, 6, txt="4. Buka 'Galeri Jurnal Kelas' (klik nama siswa) untuk membaca detail jawabannya di layar.")
        pdf.multi_cell(0, 6, txt="5. Klik 'Download Rangkuman Kelas' di paling bawah untuk menyimpan rekap seluruh siswa ke laptop.")
    else:
        pdf.cell(200, 10, txt="Learning Reflection Journal - User Guide", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="PART A: Guide for Students (How to Fill Out the Journal)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Open the app and select your language in the sidebar (top left).")
        pdf.multi_cell(0, 6, txt="2. Fill in your profile: Date, Time, Name, Class, and Roll Number.")
        pdf.multi_cell(0, 6, txt="3. Select the emoji that best describes your mood.")
        pdf.multi_cell(0, 6, txt="4. Answer the 6 reflection questions honestly.")
        pdf.multi_cell(0, 6, txt="5. Click the 'Submit My Reflection Journal!' button.")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 8, txt="PART B: Guide for Teachers (Data Management)", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, txt="1. Change background color in 'Teacher Settings' in the sidebar.")
        pdf.multi_cell(0, 6, txt="2. Scroll down to see the real-time class mood chart.")
        pdf.multi_cell(0, 6, txt="3. In 'Print Individual Portfolio', select a student's name to see their personal graph and download their full track record (PDF).")
        pdf.multi_cell(0, 6, txt="4. Open 'Class Journal Gallery' (click a student's name) to read their detailed answers.")
        pdf.multi_cell(0, 6, txt="5. Click 'Download Class Summary' at the very bottom to save all students' data to your device.")

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# BAGIAN 4: ANTARMUKA PENGGUNA (UI) STREAMLIT
# ==========================================
with st.sidebar:
    st.header(t["teacher_settings"])
    bg_color = st.color_picker(t["bg_color"], "#F4F6F9")
    
    st.divider()
    
    # --- FITUR BARU: TOMBOL UNDUH PANDUAN PENGGUNA ---
    st.header(t["help_center"])
    pdf_panduan = generate_guide_pdf(language)
    st.download_button(
        label=t["btn_dl_guide"],
        data=pdf_panduan,
        file_name='User_Guide_Reflection_Journal.pdf',
        mime='application/pdf'
    )
    # --------------------------------------------------

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

st.title(t["title"])
st.write(t["subtitle"])

with st.form("pennant_form", clear_on_submit=True):
    st.subheader(t["student_profile"])
    col_date, col_time = st.columns(2)
    with col_date:
        tanggal = st.date_input(t["date"])
    with col_time:
        waktu = st.time_input(t["time"])
        
    name = st.text_input(t["name"])
    
    col_kelas, col_absen = st.columns(2)
    with col_kelas:
        kelas = st.selectbox(t["class"], ["7A", "7B", "7C", "7D", "7E", "7F"])
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
            
            insert_data(waktu_lengkap_str, name, kelas, str(absen), feeling, 
                        belajar_tentang, sudah_paham, kesulitan, cara_atasi, hal_disukai, target_berikutnya)
            st.success(t["success"].format(name))

# ==========================================
# BAGIAN 5: ANALITIK & UNDUH PDF
# ==========================================
st.divider()
st.header(t["board_header"])

df_students = get_all_data()

if not df_students.empty:
    st.subheader(t["chart_header"])
    feeling_counts = df_students['feeling'].value_counts()
    st.bar_chart(feeling_counts)
    
    st.divider()
    st.header(t["print_header"])
    st.write(t["print_desc"])
    
    daftar_nama = df_students['name'].unique()
    pilihan_siswa = st.selectbox(t["select_name"], daftar_nama)
    
    data_siswa = df_students[df_students['name'] == pilihan_siswa]
    grafik_siswa = data_siswa['feeling'].value_counts()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(t["graph_mood"].format(pilihan_siswa))
        st.bar_chart(grafik_siswa, color="#28A745") 
        
    with col2:
        st.write(t["last_entry"])
        if len(data_siswa) > 0:
            info_terakhir = data_siswa.iloc[-1]
            st.info(f"📅 {info_terakhir['waktu_lengkap']}\n\n**{t['difficulty']}** {info_terakhir['kesulitan']}\n\n**{t['target']}** {info_terakhir['target_berikutnya']}")
    
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
    
    for idx, row in df_students.iterrows():
        with st.expander(f"📖 {row['name']} ({t['class']} {row['kelas']} - {t['absen']} {row['absen']})"):
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
    
    pdf_data = generate_pdf_report(df_students, feeling_counts, t)
    st.download_button(
        label=t["btn_dl_all"],
        data=pdf_data,
        file_name='Class_Reflection_Report.pdf',
        mime='application/pdf'
    )
else:
    st.info(t["no_data"])