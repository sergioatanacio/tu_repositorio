[app]
# (str) Título de tu aplicación
title = TranscriptionApp

# (str) Nombre del paquete
package.name = transcriptionapp

# (str) Dominio del paquete (identificador único)
package.domain = org.tudominio

# (str) Directorio de origen donde se encuentra main.py
source.dir = .

# (str) Archivo principal de la aplicación
source.main = main.py

# (list) Extensiones de archivos a incluir
source.include_exts = py,png,jpg,kv,atlas

# (str) Versión de la aplicación
version = 1.0

# (list) Requisitos de la aplicación
requirements = python3,kivy,requests,pydub,plyer,python-dotenv

# (str) Icono de la aplicación
icon = assets/icons/app_icon.png

# (str) Orientación de la pantalla (portrait, landscape o all)
orientation = portrait

# (bool) Si la aplicación debe estar en pantalla completa
fullscreen = 0

# (list) Permisos necesarios
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Tema de la aplicación
android.theme = '@android:style/Theme.NoTitleBar'

[buildozer]
log_level = 2
warn_on_root = 1

[platforms]
android = 1
