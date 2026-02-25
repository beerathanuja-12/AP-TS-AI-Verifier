import requests

# Mana API address
url = 'http://127.0.0.1:5000/validate'

# Test cheyalsina image path
image_path = 'uploads/test.jpg'

with open(image_path, 'rb') as img:
    files = {'image': img}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:", response.json())