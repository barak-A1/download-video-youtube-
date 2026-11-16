"""
YouTube Downloader 720p MP4 (audio jernih AAC 192 kbps)

Jalankan:
    pip install -r requirements.txt
    python app.py
Lalu buka http://127.0.0.1:5000

Wajib terpasang: FFmpeg (untuk menggabungkan video + audio).
Gunakan hanya untuk video milik Anda, berlisensi bebas, atau yang
diizinkan pemiliknya. Patuhi Ketentuan Layanan YouTube dan hukum hak cipta.
"""
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

ALLOWED_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "music.youtube.com", "youtu.be",
}

# Prioritas: video H.264 <=720p + audio terbaik (kompatibel luas),
# lalu fallback ke codec lain, lalu ke file tunggal <=720p.
FORMAT = (
    "bestvideo[height<=720][vcodec^=avc1]+bestaudio"
    "/bestvideo[height<=720]+bestaudio"
    "/best[height<=720]"
)


def valid_youtube_url(url: str) -> bool:
    try:
        p = urlparse(url)
    except ValueError:
        return False
    return p.scheme in ("http", "https") and (p.hostname or "").lower() in ALLOWED_HOSTS


def safe_filename(title: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", title).strip()
    return (name[:120] or "video") + ".mp4"


INDEX_HTML = """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>YouTube Downloader 720p</title>
<style>
  :root { --bg:#f6f7f9; --card:#fff; --text:#1c1e21; --muted:#65676b;
          --accent:#d93025; --border:#dcdfe3; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#16181b; --card:#222529; --text:#e8eaed; --muted:#9aa0a6;
            --accent:#ff5a4d; --border:#3a3e43; }
  }
  * { box-sizing:border-box; }
  body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
         background:var(--bg); color:var(--text); min-height:100vh;
         display:flex; align-items:center; justify-content:center; padding:16px; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:14px;
          padding:24px; width:100%; max-width:560px; }
  h1 { font-size:1.3rem; margin:0 0 4px; }
  p.sub { color:var(--muted); margin:0 0 18px; font-size:.9rem; }
  .row { display:flex; gap:8px; }
  input { flex:1; padding:11px 12px; border-radius:8px; border:1px solid var(--border);
          background:transparent; color:var(--text); font-size:1rem; min-width:0; }
  button { padding:11px 16px; border:0; border-radius:8px; background:var(--accent);
           color:#fff; font-size:1rem; cursor:pointer; }
  button:disabled { opacity:.55; cursor:wait; }
  .preview { display:none; margin-top:18px; }
  .preview img { width:100%; border-radius:10px; display:block; }
  .preview h2 { font-size:1rem; margin:10px 0 2px; }
  .meta { color:var(--muted); font-size:.85rem; margin-bottom:12px; }
  .badge { display:inline-block; font-size:.75rem; padding:2px 8px; border-radius:99px;
           border:1px solid var(--border); margin-right:6px; }
  .status { margin-top:14px; font-size:.9rem; min-height:1.2em; }
  .error { color:var(--accent); }
  .note { margin-top:18px; font-size:.75rem; color:var(--muted); }
</style>
</head>
<body>
<div class="card">
  <h1>YouTube Downloader</h1>
  <p class="sub">Video 720p, format MP4, audio AAC 192 kbps.</p>

  <div class="row">
    <input id="url" type="url" placeholder="Tempel link YouTube di sini" autocomplete="off">
    <button id="check">Cek</button>
  </div>

  <div class="preview" id="preview">
    <img id="thumb" alt="">
    <h2 id="title"></h2>
    <div class="meta" id="meta"></div>
    <span class="badge">720p</span><span class="badge">MP4</span><span class="badge">AAC 192k</span>
    <div style="margin-top:12px"><button id="dl">Unduh MP4</button></div>
  </div>

  <div class="status" id="status"></div>
  <div class="note">Gunakan hanya untuk konten milik Anda atau yang diizinkan pemiliknya.</div>
</div>

<script>
const $ = id => document.getElementById(id);
let current = { url:"", title:"video" };

function setStatus(msg, isError=false) {
  const s = $("status");
  s.textContent = msg;
  s.className = "status" + (isError ? " error" : "");
}
function fmtDuration(sec) {
  if (!sec) return "";
  const h = Math.floor(sec/3600), m = Math.floor(sec%3600/60), s = sec%60;
  return (h ? h + ":" + String(m).padStart(2,"0") : m) + ":" + String(s).padStart(2,"0");
}

$("check").onclick = async () => {
  const url = $("url").value.trim();
  if (!url) return setStatus("Masukkan link YouTube dulu.", true);
  $("check").disabled = true; $("preview").style.display = "none";
  setStatus("Mengambil info video...");
  try {
    const r = await fetch("/api/info", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ url })
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error || "Gagal mengambil info.");
    current = { url, title: d.title };
    $("thumb").src = d.thumbnail || "";
    $("title").textContent = d.title;
    $("meta").textContent = [d.uploader, fmtDuration(d.duration)].filter(Boolean).join(" • ");
    $("preview").style.display = "block";
    setStatus(d.duration > 3600 ? "Video cukup panjang, proses bisa lama." : "");
  } catch (e) { setStatus(e.message, true); }
  $("check").disabled = false;
};

$("dl").onclick = async () => {
  $("dl").disabled = true;
  setStatus("Mengunduh dan memproses di server... mohon tunggu, jangan tutup halaman.");
  try {
    const r = await fetch("/api/download?url=" + encodeURIComponent(current.url));
    if (!r.ok) {
      let msg = "Unduhan gagal.";
      try { msg = (await r.json()).error || msg; } catch {}
      throw new Error(msg);
    }
    const blob = await r.blob();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = current.title.replace(/[\\\\/:*?"<>|]/g, "") + ".mp4";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 10000);
    setStatus("Selesai. File sudah tersimpan.");
  } catch (e) { setStatus(e.message, true); }
  $("dl").disabled = false;
};

$("url").addEventListener("keydown", e => { if (e.key === "Enter") $("check").click(); });
</script>
</body>
</html>"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.post("/api/info")
def info():
    url = (request.get_json(silent=True) or {}).get("url", "").strip()
    if not valid_youtube_url(url):
        return jsonify(error="Link harus berupa URL YouTube yang valid."), 400
    opts = {"quiet": True, "no_warnings": True, "noplaylist": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            d = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        return jsonify(error=f"Tidak bisa membaca video: {str(e)[:200]}"), 400
    return jsonify(
        title=d.get("title", "video"),
        thumbnail=d.get("thumbnail"),
        duration=d.get("duration"),
        uploader=d.get("uploader"),
    )


@app.get("/api/download")
def download():
    url = request.args.get("url", "").strip()
    if not valid_youtube_url(url):
        return jsonify(error="Link harus berupa URL YouTube yang valid."), 400
    if shutil.which("ffmpeg") is None:
        return jsonify(error="FFmpeg belum terpasang di server."), 500

    tmpdir = Path(tempfile.mkdtemp(prefix="ytdl_"))
    opts = {
        "format": FORMAT,
        "merge_output_format": "mp4",
        "outtmpl": str(tmpdir / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        # Video disalin tanpa re-encode; audio diubah ke AAC 192 kbps
        # agar jernih dan kompatibel dengan semua pemutar MP4.
        "postprocessor_args": {"merger": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]},
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            d = ydl.extract_info(url, download=True)
        files = list(tmpdir.glob("*.mp4"))
        if not files:
            raise RuntimeError("File hasil tidak ditemukan.")
        out = files[0]
        title = d.get("title", "video")
    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return jsonify(error=f"Unduhan gagal: {str(e)[:200]}"), 500

    resp = send_file(out, mimetype="video/mp4", as_attachment=True,
                     download_name=safe_filename(title))
    resp.call_on_close(lambda: shutil.rmtree(tmpdir, ignore_errors=True))
    return resp


if __name__ == "__main__":
    # Hanya lokal. Jangan buka ke internet tanpa autentikasi dan pembatasan.
    app.run(host="127.0.0.1", port=5000, debug=False)
