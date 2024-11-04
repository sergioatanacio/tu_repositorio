[app]
title = TranscriptionApp
package.name = transcriptionapp
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,pydub,plyer
orientation = portrait
icon = assets/icons/app_icon.png
fullscreen = 0

# Permisos necesarios
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Archivos a excluir
# No es necesario especificarlo aquí si se usa .gitignore

[buildozer]
log_level = 2
warn_on_root = 1

[platforms]
android = 1
