from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto')

# Carpeta para almacenar descargas temporales
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash("Debe proporcionar una URL válida.", "danger")
            return redirect(url_for('index'))
        try:
            # Crear objeto YouTube con pytubefix
            yt = YouTube(url, on_progress_callback=on_progress)
            stream = yt.streams.get_highest_resolution()
            
            # Generar un nombre único para evitar sobreescrituras
            filename_unique = f"{uuid.uuid4().hex}_{stream.default_filename}"
            file_path = os.path.join(DOWNLOAD_FOLDER, filename_unique)

            # Descargar el video
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename_unique)
            
            flash("¡Descarga completada con éxito! Se iniciará la descarga en tu navegador.", "success")
            return send_file(
                file_path,
                as_attachment=True,
                download_name=stream.default_filename
            )

        except Exception as e:
            flash(f"Error al descargar el video: {e}", "danger")
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
