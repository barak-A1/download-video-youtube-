# download-video-youtube-
   
How to Run

    Install Python 3.9+ and FFmpeg. FFmpeg is required because YouTube video and audio are downloaded separately and then merged.

        Windows: winget install ffmpeg
        macOS: brew install ffmpeg
        Linux: sudo apt install ffmpeg

    In the project folder, run:
    Bash

    pip install -r requirements.txt
    python app.py

    Open [http://127.0.0.1:5000](http://127.0.0.1:5000), paste the YouTube link, click Check, and then click Download MP4.

How It Works

    Video: Video is captured at a maximum of 720p, prioritizing the H.264 codec so the MP4 can play on almost any device. The stream is copied without re-encoding, ensuring no loss in quality.

    Audio: The best available audio is converted to AAC 192 kbps, which is higher than standard YouTube MP4 audio (around 128 kbps).

    Security: Only YouTube links are accepted, playlists are ignored, and temporary files on the server are deleted after being sent.

Important Notes

    Audio quality cannot exceed the source. Videos with already poor audio will not improve.

    If YouTube updates its system and downloads fail, run pip install -U yt-dlp.

    This app only runs on 127.0.0.1 (your own computer). Do not publish it to the internet without login and access restrictions.

    YouTube's Terms of Service prohibit downloading videos without permission. Use it only for your own videos, freely licensed content (such as Creative Commons), or content authorized by the owner.

### Running the Application on Linux

The steps below use Ubuntu/Debian. For other distros, the installation commands are listed in the table.

**1. Install Python, pip, venv, and FFmpeg**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg

```

| Distro | Command |
| --- | --- |
| **Fedora** | `sudo dnf install python3 python3-pip ffmpeg-free` *(for full FFmpeg, enable the RPM Fusion repo then install `ffmpeg`)* |
| **Arch** | `sudo pacman -S python python-pip ffmpeg` |

Check the results:

```bash
python3 --version
ffmpeg -version

```

**2. Prepare the project folder**
Place `app.py` and `requirements.txt` in one folder, for example `~/yt-downloader`:

```bash
cd ~/yt-downloader

```

**3. Create a virtual environment and install dependencies**
Modern distros (Ubuntu 23.04+, Debian 12+) block direct `pip install` to the system with an `externally-managed-environment` message. Therefore, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

The `(venv)` indicator will appear at the beginning of your terminal prompt.

**4. Run the application**

```bash
python app.py

```

Open your browser to `[http://127.0.0.1:5000](http://127.0.0.1:5000)`. To stop the application, press `Ctrl + C`.

In subsequent sessions, simply run:

```bash
cd ~/yt-downloader
source venv/bin/activate
python app.py

```

#### Common Issues (Linux)

| Symptom | Solution |

| `externally-managed-environment` | Use `venv` as shown in step 3; do not use `--break-system-packages`. |
| `No module named venv`           | `sudo apt install python3-venv` |
| “FFmpeg is not installed on the server” | Check `ffmpeg -version`. If not found, install it using the command in step 1. |
| Download fails even though the link is valid | Update yt-dlp: `pip install -U yt-dlp` (with `venv` active). |
| Port 5000 is already in use | Change `port=5000` on the last line of `app.py` to `5001`. |

**If you are using WSL on Windows**
The steps are identical to the ones above, run inside the WSL terminal. In WSL2, `[http://127.0.0.1:5000](http://127.0.0.1:5000)` can usually be opened directly from your Windows browser. If that doesn't work, check your WSL IP address with `hostname -I`, change `host="127.0.0.1"` in `app.py` to `host="0.0.0.0"`, and open `http://<WSL-IP>:5000`. Revert it back to `127.0.0.1` afterward when no longer needed.

**Optional: Launcher script**
Create a file named `run.sh` (or `jalankan.sh`):

```bash
#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py

```

Grant execution permissions and run it:

```bash
chmod +x run.sh
./run.sh

```

---

### Running the Application on Windows

**1. Install Python**
Download from [python.org/downloads](https://www.python.org/downloads/) (version 3.9 or newer).
During installation, check **“Add python.exe to PATH”** on the first screen, then click **Install Now**.
Check in Command Prompt (press `Win + R`, type `cmd`, press Enter):

```cmd
python --version

```

If a version number appears, the installation was successful.

**2. Install FFmpeg**
The easiest way via Command Prompt:

```cmd
winget install Gyan.FFmpeg

```

Once finished, close and reopen Command Prompt, then check:

```cmd
ffmpeg -version

```

If `winget` is unavailable, download manually from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) (choose “release essentials”), extract it to `C:\ffmpeg`, and add `C:\ffmpeg\bin` to your PATH:
Start → type “Edit the system environment variables” → **Environment Variables** → select **Path** under User variables → **Edit** → **New** → enter `C:\ffmpeg\bin` → **OK**. Reopen Command Prompt and verify again with `ffmpeg -version`.

**3. Prepare the project folder**
Save `app.py` and `requirements.txt` in a single folder, for example `C:\yt-downloader`.

**4. Install dependencies**
In Command Prompt:

```cmd
cd C:\yt-downloader
pip install -r requirements.txt

```

**5. Run the application**

```cmd
python app.py

```

Keep the Command Prompt window open. Then open your browser and go to:
`[http://127.0.0.1:5000](http://127.0.0.1:5000)`

To stop the application, press `Ctrl + C` in Command Prompt.

#### Common Issues (Windows)

| Message / Symptom | Solution |
| --- | --- |
| `'python' is not recognized` | Python is not added to PATH. Reinstall and check “Add python.exe to PATH”. |
| `'pip' is not recognized` | Try `python -m pip install -r requirements.txt`. |
| “FFmpeg is not installed on the server” | FFmpeg is not in PATH. Close and reopen Command Prompt, then check `ffmpeg -version`. |
| Download fails even though the link is valid | Update yt-dlp: `pip install -U yt-dlp`. |
| Port 5000 is already in use | Change `port=5000` on the last line of `app.py` to `port=5001`, then open `[http://127.0.0.1:5001](http://127.0.0.1:5001)`. |

**Optional: Create a launcher file**
To avoid typing commands every time, create a file named `run.bat` (or `jalankan.bat`) in the same folder with the following content:

```bat
@echo off
cd /d %~dp0
python app.py
pause

```

Afterward, simply double-click the file and open `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

================================================================================

download video youtube dengan kualitas gambar 720p format mp4 dan dengan suara kualitas jelas jernih

Aplikasinya jadi: app.py (server dan tampilan web dalam satu file) dan requirements.txt.

Menjalankan Aplikasi di Linux
=================================
Langkah di bawah memakai Ubuntu/Debian. Untuk distro lain, perintah instalasinya ada di tabel.

1. Pasang Python, pip, venv, dan FFmpeg
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg
Distro	Perintah
Fedora	sudo dnf install python3 python3-pip ffmpeg-free (untuk FFmpeg penuh, aktifkan repo RPM Fusion lalu pasang ffmpeg)
Arch	sudo pacman -S python python-pip ffmpeg

Cek hasilnya:

python3 --version
ffmpeg -version
2. Siapkan folder proyek

Taruh app.py dan requirements.txt di satu folder, misalnya ~/yt-downloader:

cd ~/yt-downloader
3. Buat virtual environment dan pasang dependensi

Distro modern (Ubuntu 23.04+, Debian 12+) menolak pip install langsung ke sistem dengan pesan externally-managed-environment. Karena itu pakai virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Tanda (venv) akan muncul di awal prompt terminal.

4. Jalankan aplikasi
python app.py

Buka browser ke http://127.0.0.1:5000. Untuk menghentikan, tekan Ctrl + C.

Pada sesi berikutnya, cukup:

cd ~/yt-downloader
source venv/bin/activate
python app.py

Masalah yang sering muncul
=================================
Gejala	                            Solusi
externally-managed-environment	    Pakai venv seperti langkah 3, jangan pakai --break-system-packages.
No module named venv	              sudo apt install python3-venv
“FFmpeg belum terpasang di server”	Cek ffmpeg -version. Jika tidak ada, pasang dengan perintah di langkah 1.
Unduhan gagal padahal link benar	  Perbarui yt-dlp: pip install -U yt-dlp (dengan venv aktif).
Port 5000 sudah dipakai	            Ubah port=5000 di baris terakhir app.py menjadi 5001.
Jika Anda memakai WSL di Windows

Langkahnya sama persis dengan di atas, dijalankan di terminal WSL. Di WSL2, alamat http://127.0.0.1:5000 biasanya bisa dibuka langsung dari browser Windows. Kalau tidak bisa, cek alamat IP WSL dengan hostname -I lalu ubah host="127.0.0.1" di app.py menjadi host="0.0.0.0", dan buka http://<IP-WSL>:5000. Setelah itu kembalikan ke 127.0.0.1 kalau tidak lagi diperlukan.

Opsional: skrip peluncur

Buat file jalankan.sh:

#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py

Beri izin eksekusi lalu jalankan:

chmod +x jalankan.sh
./jalankan.sh


Menjalankan Aplikasi di Windows
=================================
1. Pasang Python
Unduh dari python.org/downloads (versi 3.9 atau lebih baru).
Saat instalasi, centang “Add python.exe to PATH” di layar pertama, lalu klik Install Now.
Cek di Command Prompt (tekan Win + R, ketik cmd, Enter):
   python --version

Kalau muncul nomor versi, berarti berhasil.

2. Pasang FFmpeg

Cara termudah lewat Command Prompt:

winget install Gyan.FFmpeg

Setelah selesai, tutup lalu buka lagi Command Prompt, kemudian cek:

ffmpeg -version

Kalau winget tidak tersedia, unduh manual dari gyan.dev/ffmpeg/builds (pilih “release essentials”), ekstrak ke C:\ffmpeg, lalu tambahkan C:\ffmpeg\bin ke PATH:
Start → ketik “Edit the system environment variables” → Environment Variables → pilih Path di bagian User → Edit → New → isi C:\ffmpeg\bin → OK. Buka ulang Command Prompt dan cek lagi dengan ffmpeg -version.

3. Siapkan folder proyek

Simpan app.py dan requirements.txt di satu folder, misalnya C:\yt-downloader.

4. Instal dependensi

Di Command Prompt:

cd C:\yt-downloader
pip install -r requirements.txt
5. Jalankan aplikasi
python app.py

Biarkan jendela Command Prompt tetap terbuka. Lalu buka browser dan akses:

http://127.0.0.1:5000

Untuk menghentikan aplikasi, tekan Ctrl + C di Command Prompt.

Masalah yang sering muncul
=================================
Pesan / gejala	                       Solusi
'python' is not recognized	           Python belum masuk PATH. Instal ulang dan centang “Add python.exe to PATH”.
'pip' is not recognized	               Coba python -m pip install -r requirements.txt.
“FFmpeg belum terpasang di server”	   FFmpeg belum ada di PATH. Tutup dan buka ulang Command Prompt, lalu cek ffmpeg -version.
Unduhan gagal padahal link benar	     Perbarui yt-dlp: pip install -U yt-dlp.
Port 5000 sudah dipakai	               Ubah port=5000 di baris terakhir app.py menjadi port=5001, lalu buka http://127.0.0.1:5001.

Opsi: buat file peluncur

Supaya tidak perlu mengetik perintah setiap kali, buat file jalankan.bat di folder yang sama dengan isi:

@echo off
cd /d %~dp0
python app.py
pause

Setelah itu cukup klik dua kali file tersebut, lalu buka http://127.0.0.1:5000 di browser.

