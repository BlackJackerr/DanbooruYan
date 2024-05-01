from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route('/smeme', methods=['POST'])
def generate_meme():
    # Mendapatkan teks dan gambar dari request
    teks1 = request.form.get('teks1')
    teks2 = request.form.get('teks2')
    image_file = request.files['image']

    # Memvalidasi teks dan gambar
    if not teks1 and not teks2:
        return jsonify({'error': 'Teks atas atau bawah tidak boleh kosong'})
    if image_file.filename == '':
        return jsonify({'error': 'Tidak ada gambar yang diunggah'})

    # Menyimpan gambar yang diunggah
    image_path = os.path.join(app.config['STATIC_FOLDER'], 'images', image_file.filename)
    image_file.save(image_path)

    # Membuka gambar dan membuat objek ImageDraw
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Menambahkan font
    font = ImageFont.truetype('static/fonts/Arial.ttf', 24)

    # Menambahkan teks atas (jika ada)
    if teks1:
        text_width, text_height = draw.textsize(teks1, font=font)
        draw.text((image.width - text_width // 2, 10), teks1, fill='black', font=font)

    # Menambahkan teks bawah (jika ada)
    if teks2:
        text_width, text_height = draw.textsize(teks2, font=font)
        draw.text((image.width - text_width // 2, image.height - text_height - 10), teks2, fill='black', font=font)

    # Menyimpan gambar yang sudah dimodifikasi
    modified_image_path = os.path.join(app.config['STATIC_FOLDER'], 'images', 'meme.jpg')
    image.save(modified_image_path)

    # Mengembalikan URL gambar yang sudah dimodifikasi
    return jsonify({'meme_url': f'/static/images/meme.jpg'})

if __name__ == '__main__':
    app.run(debug=False)
	
