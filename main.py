from random import randint
from Crypto.Cipher import AES
from flask import Flask, request, render_template

# Define the public parameters
p = 23
g = 5

# Define the encryption and decryption functions
def pad(message):
    padding_size = AES.block_size - len(message) % AES.block_size
    padding = chr(padding_size) * padding_size
    return message + padding

def unpad(message):
    padding_size = ord(message[-1])
    return message[:-padding_size]

def encrypt(message, shared_secret):
    message = pad(message)
    cipher = AES.new(shared_secret, AES.MODE_ECB)
    return cipher.encrypt(message)

def decrypt(encrypted, shared_secret):
    cipher = AES.new(shared_secret, AES.MODE_ECB)
    message = cipher.decrypt(encrypted)
    return unpad(message)

# Define the Flask app
app = Flask(_name_)

# Define the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Generate a random secret integer for Alice and Bob
        a = randint(1, 100)
        b = randint(1, 100)

        # Calculate the public keys for Alice and Bob
        A = (g ** a) % p
        B = (g ** b) % p

        # Exchange public keys
        shared_secret_A = (B ** a) % p
        shared_secret_B = (A ** b) % p

        # Encrypt the message
        message = request.form['message']
        encrypted = encrypt(message, str(shared_secret_A))

        # Display the results
        return render_template('result.html', 
                               key=f"Shared key: {shared_secret_A}", 
                               encrypted=f"Encrypted message: {encrypted.hex()}", 
                               decrypted=f"Decrypted message: {decrypt(encrypted, str(shared_secret_B))}")
    else:
        return render_template('home.html')

# Start the Flask app
if _name_ == '_main_':
    app.run(debug=True)
