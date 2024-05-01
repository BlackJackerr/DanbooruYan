from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np

# Inisialisasi Flask
app = Flask(__name__)

# Fungsi untuk memproses meme
def process_meme(image_path, text1, text2):
    # Membaca gambar
    image = cv2.imread(image_path)

    # Mengubah gambar menjadi RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Menambahkan teks atas
    if text1:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        font_color = (0, 0, 0)  # Hitam
        text_position = (10, 20)  # Posisi teks atas
        cv2.putText(image, text1, text_position, font, font_size, font_color, thickness=2)

    # Menambahkan teks bawah
    if text2:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        font_color = (0, 0, 0)  # Hitam
        text_position = (10, image.shape[0] - 20)  # Posisi teks bawah
        cv2.putText(image, text2, text_position, font, font_size, font_color, thickness=2)

    # Mengubah gambar kembali ke BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Mengembalikan gambar yang telah diproses
    return image

@app.route("/")
def runhome():
	return "Created By Yan"

# Route untuk upload gambar
@app.route("/smeme", methods=["POST"])
def create_meme():
    # Membaca file gambar
    image_file = request.files["image"]
    if image_file:
        # Menyimpan gambar dengan nama aman
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join("uploads", image_filename)
        image_file.save(image_path)

        # Membaca teks atas dan bawah
        text1 = request.form.get("teks1")
        text2 = request.form.get("teks2")

        # Memproses meme
        processed_image = process_meme(image_path, text1, text2)

        # Mengubah gambar menjadi format PNG
        _, encoded_image = cv2.imencode(".png", processed_image)

        # Mengembalikan respon
        return send_from_directory("uploads", image_filename, mimetype="image/png")
    else:
        return jsonify({"message": "Tidak ada gambar yang diupload"})

# Menjalankan API
if __name__ == "__main__":
    app.run(host="0.0.0.0")
	    
