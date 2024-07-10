import requests

# URL for GET request (partial)
base_url = 'https://mc.yandex.ru/clmap/97646772?page-url=https%3A%2F%2Fclicker.spin.fi%2F%23tgWebAppData%3D'

# URL for POST request
url_post = 'https://clicker-backend.spin.fi/api/clicks/apply'

# Read additional parameters from data.txt
with open('data.txt', 'r') as file:
    additional_params = file.read().strip()  # Read data.txt content as string

# Combine base_url and additional_params
url_get = base_url + additional_params

# Perform GET request
response_get = requests.get(url_get)

if response_get.status_code == 200:
    print('GET request successful.')
    print('Response content:')
    print(response_get.text)
else:
    print(f'GET request failed with status code {response_get.status_code}.')

# Perform POST request
payload = {'clicks': '21'}  # Example payload for POST request
response_post = requests.post(url_post, data=payload)

if response_post.status_code == 200:
    print('POST request successful.')
    print('Response content:')
    print(response_post.text)
else:
    print(f'POST request failed with status code {response_post.status_code}.')
