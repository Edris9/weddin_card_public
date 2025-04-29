from flask import Flask, request, jsonify, render_template, send_from_directory
import csv
import os
import shutil
from datetime import datetime

app = Flask(__name__, static_folder='static')

# Kontrollera om data-mappen finns, annars skapa den
if not os.path.exists('data'):
    os.makedirs('data')

# Sökväg till CSV-filen
CSV_FILE = 'data/responses.csv'

# Skapa CSV-filen om den inte finns
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Tidpunkt', 'Namn', 'Kommer', 'Antal gäster', 'Meddelande'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Hämta data från formuläret
    data = request.json
    name = data.get('name', '')
    attending = 'Ja' if data.get('attending', False) else 'Nej'
    guests = data.get('guests', '1')
    message = data.get('message', '')
    
    # Tidpunkt för svaret
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Spara data i CSV-filen
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, name, attending, guests, message])
    
    # Returnera framgångsmeddelande
    return jsonify({'success': True})

@app.route('/responses')
def responses():
    """Enkel endpoint för att visa alla svar (skyddad i produktionsmiljö)"""
    all_responses = []
    
    # Läs in alla svar från CSV-filen
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Hoppa över rubriken
        for row in reader:
            all_responses.append({
                'timestamp': row[0],
                'name': row[1],
                'attending': row[2],
                'guests': row[3],
                'message': row[4]
            })
    
    # Räkna totalt antal gäster som kommer
    total_guests = sum(int(response['guests']) for response in all_responses 
                       if response['attending'] == 'Ja')
    
    # Returnera HTML-sidan med alla svar
    return render_template('responses.html', 
                          responses=all_responses, 
                          total_guests=total_guests)

# Säkerställ att images-mappen finns
@app.before_request
def before_request():
    if not os.path.exists('static/images'):
        os.makedirs('static/images')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Funktion för att ladda upp en ny bild"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'Ingen bild finns'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Inget filnamn'})
    
    # Spara bilden
    filename = 'wedding-ring-2.webp'  # Använd samma filnamn för att ersätta
    filepath = os.path.join(app.static_folder, 'images', filename)
    file.save(filepath)
    
    return jsonify({'success': True})

@app.route('/copy-background')
def copy_background():
    """Funktion för att kopiera bakgrundsbilden till projektet"""
    source_path = r"C:\Users\Edris\Desktop\Python Programmeri ng\own project\wedding card\static\images\image2.jpg"
    
    # Säkerställ att målmappen finns
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    target_path = os.path.join('static', 'images', 'image2.jpg')
    
    try:
        shutil.copyfile(source_path, target_path)
        return "Bakgrundsbilden har kopierats till projektet!"
    except Exception as e:
        return f"Det gick inte att kopiera bakgrundsbilden: {str(e)}"

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)