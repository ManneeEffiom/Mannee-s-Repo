from flask import Flask, render_template, request, jsonify
import secrets
import string

app = Flask(__name__)

def generate_password(length, use_upper, use_lower, use_digits, use_special, avoid_ambiguous, words):
    chars = []
    ambiguous = {'l', '1', 'I', '0', 'O'}
    
    # Define character pools based on user input
    if use_upper:
        chars += [c for c in string.ascii_uppercase if c not in ambiguous] if avoid_ambiguous else string.ascii_uppercase
    if use_lower:
        chars += [c for c in string.ascii_lowercase if c not in ambiguous] if avoid_ambiguous else string.ascii_lowercase
    if use_digits:
        chars += [c for c in string.digits if c not in ambiguous] if avoid_ambiguous else string.digits
    if use_special:
        chars += string.punctuation
    
    if not chars:
        return "At least one character type must be selected.", 400

    # Split words into chunks and shuffle
    word_chars = []
    if words:
        for word in words.split():
            word_chars.extend(list(word))
        secrets.SystemRandom().shuffle(word_chars)
    
    # Calculate remaining characters needed
    remaining = max(0, length - len(word_chars))
    password = word_chars + [secrets.choice(chars) for _ in range(remaining)]
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def check_strength(password):
    length = len(password)
    diversity = sum([
        1 if any(c.islower() for c in password) else 0,
        1 if any(c.isupper() for c in password) else 0,
        1 if any(c.isdigit() for c in password) else 0,
        1 if any(c in string.punctuation for c in password) else 0
    ])
    
    if length < 8 or diversity < 2:
        return "Weak"
    elif 8 <= length < 12 or diversity == 2:
        return "Medium"
    else:
        return "Strong"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.form
        try:
            length = int(data.get('length', 8))  # Default to 8 if not provided
            if length < 8 or length > 128:
                return "Password length must be between 8 and 128.", 400
            
            password = generate_password(
                length=length,
                use_upper='upper' in data,
                use_lower='lower' in data,
                use_digits='digits' in data,
                use_special='special' in data,
                avoid_ambiguous='avoid' in data,
                words=data.get('words', '')
            )
            if not password:
                return "Failed to generate password.", 500
            
            strength = check_strength(password)
            return render_template('index.html', password=password, strength=strength)
        except ValueError:
            return "Invalid input for password length.", 400
    return render_template('index.html', password='', strength='')

if __name__ == '__main__':
    app.run(debug=True)
    
    