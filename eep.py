from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Fungsi untuk membaca data akun dari data.txt
def read_accounts():
    with open('data.txt', 'r') as file:
        data = file.read()
        accounts = json.loads(data)
    return accounts

# Variabel global untuk menyimpan data akun dan indeks akun saat ini
accounts = read_accounts()
current_account_index = 0

@app.route('/tap', methods=['GET'])
def tap():
    global current_account_index
    
    # Mengambil akun yang saat ini digunakan
    current_account = accounts[current_account_index]
    
    # URL dasar login
    base_login_url = "https://mc.yandex.ru/clmap/97646772?page-url=https%3A%2F%2Fclicker.spin.fi%2F%23tgWebAppData%3D"
    
    # URL lengkap login dengan query string dari data.txt
    login_url = base_login_url + current_account['query_string']
    
    # Mengirim permintaan GET untuk login
    login_response = requests.get(login_url)
    
    if login_response.status_code == 200:
        # URL untuk verifikasi tap
        verify_url = 'https://clicker-backend.spin.fi/api/clicks/apply?clicks=21'
        
        # Data untuk verifikasi tap
        query_data = current_account['query_data']
        
        # Mengirim permintaan POST untuk verifikasi tap
        response = requests.post(verify_url, json=query_data)
        
        if response.status_code == 200:
            return jsonify({'status': 'success', 'account': current_account['username'], 'account_index': current_account_index + 1, 'total_accounts': len(accounts)})
        else:
            return jsonify({'status': 'failed', 'message': 'Verification failed'})
    else:
        return jsonify({'status': 'failed', 'message': 'Login failed'})

@app.route('/next_account', methods=['POST'])
def next_account():
    global current_account_index
    
    # Pindah ke akun berikutnya
    current_account_index = (current_account_index + 1) % len(accounts)
    
    return jsonify({'status': 'success', 'new_account': accounts[current_account_index]['username'], 'account_index': current_account_index + 1, 'total_accounts': len(accounts)})

if __name__ == '__main__':
    app.run(debug=False)

