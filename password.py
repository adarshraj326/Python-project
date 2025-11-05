from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)


def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                     include_digits=True, include_symbols=True):
    """Generate a random password based on user preferences"""
    
    characters = ""
    
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        return "Please select at least one character type!"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            length = int(request.form.get('length', 12))
            include_uppercase = bool(request.form.get('uppercase'))
            include_lowercase = bool(request.form.get('lowercase'))
            include_digits = bool(request.form.get('digits'))
            include_symbols = bool(request.form.get('symbols'))
            
            # Validate length
            if length < 4:
                length = 4
            elif length > 50:
                length = 50
            
            password = generate_password(
                length=length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_digits=include_digits,
                include_symbols=include_symbols
            )
            
            return render_template('result.html', password=password, length=length)
        
        except ValueError:
            return render_template('index.html', error="Please enter a valid number for password length!")
    
    return render_template('index.html')


@app.route('/generate')
def generate():
    """API endpoint to generate password with default settings"""
    password = generate_password()
    return {'password': password}


if __name__ == "__main__":
    app.run(debug=True)
