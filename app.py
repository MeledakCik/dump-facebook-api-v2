from flask import Flask, request, jsonify
from googlesearch import search
from bs4 import BeautifulSoup
import os
import re
import requests

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
            print(f"[+] {url}")
            profile_id = ambil_id_facebook(url)
            nama_fb = ambil_nama_dari_facebook(url)

            if profile_id and nama_fb and "facebook" not in nama_fb.lower():
                hasil.append({"id": profile_id, "name": nama_fb})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": True, "data": hasil})


def ambil_id_facebook(url):
    match = re.search(r"id=(\d+)", url)
    return match.group(1) if match else None

def ambil_nama_dari_facebook(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "Unknown"
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        nama = title.split('|')[0].strip()
        if nama:
            return nama
        return "Unknown"
    except Exception as e:
        print(f"Error scraping FB: {e}")
        return "Unknown"

if __name__ == "__main__":
    app.run(debug=True)
