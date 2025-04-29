from flask_frozen import Freezer
from app import app
import os

# Skapa en mapp för statiska filer om den inte finns
if not os.path.exists('data'):
    os.makedirs('data')

# Skapa en tom CSV om den inte finns
if not os.path.exists('data/responses.csv'):
    with open('data/responses.csv', 'w', encoding='utf-8') as f:
        f.write('Tidpunkt,Namn,Kommer,Antal gäster,Meddelande\n')

# Ställ in konfiguration för statisk bygg
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

# Skapa Freezer-instans
freezer = Freezer(app)

# Definiera URL:er som ska byggas
@freezer.register_generator
def url_generator():
    # Enbart statiska sidor
    yield '/'
    yield '/responses'
    yield '/thankyou.html'


if __name__ == '__main__':
    freezer.freeze()