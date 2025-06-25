from flask import Flask, send_file, abort
import barcode
from barcode.writer import ImageWriter
import io

print("→ barcode-Modul geladen von:", barcode.__file__)

app = Flask(__name__)

@app.route('/<ean>')
def generate_barcode(ean):
    if not ean.isdigit() or len(ean) > 13:
        return abort(400, description="Ungültige EAN-13 Nummer")

    try:
        EAN = barcode.get_barcode_class('ean13')
        ean13 = EAN(ean, writer=ImageWriter())

        buffer = io.BytesIO()
        ean13.write(buffer)
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')
    except Exception as e:
        return abort(500, description=f"Fehler beim Generieren: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
