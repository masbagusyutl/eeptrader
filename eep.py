from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Baca query string dari file data.txt
def read_query_string():
    with open('data.txt', 'r') as file:
        query_string = file.read().strip()
    return query_string

query_string = read_query_string()

@app.route('/tap', methods=['GET'])
def tap():
    # URL dasar login
    base_login_url = "https://mc.yandex.ru/clmap/97646772?page-url=https%3A%2F%2Fclicker.spin.fi%2F%23tgWebAppData%3D"
    
    # URL lengkap login dengan query string dari data.txt
    login_url = base_login_url + query_string
    
    # Mengirim permintaan GET untuk login
    login_response = requests.get(login_url)
    
    if login_response.status_code == 200:
        # URL untuk verifikasi tap
        verify_url = 'https://clicker-backend.spin.fi/api/clicks/apply?clicks=21'
        
        # Waktu sekarang
        current_time = datetime.utcnow()
        
        # Hitung waktu 6 jam mundur
        six_hours_ago = current_time - timedelta(hours=6)
        
        # Format waktu sesuai kebutuhan
        formatted_time = six_hours_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Data untuk verifikasi tap
        query_data = {
            'timestamp': formatted_time,
            # tambahkan data tambahan sesuai kebutuhan
        }
        
        # Mengirim permintaan POST untuk verifikasi tap
        response = requests.post(verify_url, json=query_data)
        
        if response.status_code == 200:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed', 'message': 'Verification failed'})
    else:
        return jsonify({'status': 'failed', 'message': 'Login failed'})

if __name__ == '__main__':
    app.run(debug=True)
