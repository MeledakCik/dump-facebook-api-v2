from flask import Flask, request, jsonify
from googlesearch import search
import os

app = Flask(__name__)

@app.route("/dork", methods=["POST"])
def dorking():
    data = request.json
    nama = data.get("nama")
    jumlah = int(data.get("jumlah", 5))
    jeda = int(data.get("jeda", 2))

    dork = f'site:facebook.com/profile.php?id= "{nama}"'
    hasil = []

    try:
        for url in search(dork, num_results=jumlah, sleep_interval=jeda):
            profile_id = ambil_id_facebook(url)
            nama_fb = ambil_nama_dari_facebook(url)

            if profile_id and nama_fb and "facebook" not in nama_fb.lower():
                hasil.append({"id": profile_id, "name": nama_fb})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": True, "data": hasil})

def ambil_id_facebook(url):
    # contoh sederhana
    import re
    match = re.search(r"id=(\d+)", url)
    return match.group(1) if match else None

def ambil_nama_dari_facebook(url):
    # dummy karena scraping facebook langsung sering diblok
    return "Unknown"

if __name__ == "__main__":
    app.run(debug=True)
