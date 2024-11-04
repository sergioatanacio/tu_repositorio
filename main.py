import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from pydub import AudioSegment
import requests

API_URL = "https://api.openai.com/v1/audio/transcriptions"
MAX_DURATION = 300000  # 5 minutos
OUTPUT_FILE = "transcription_result.txt"

class TranscriptionApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # API Key
        self.api_key_input = TextInput(password=True, hint_text="API Key de OpenAI", size_hint=(1, None), height=40)
        self.layout.add_widget(Label(text="API Key de OpenAI:"))
        self.layout.add_widget(self.api_key_input)

        # Audio File
        self.audio_path_input = TextInput(hint_text="Ruta del archivo de audio", size_hint=(1, None), height=40)
        self.layout.add_widget(Label(text="Archivo de Audio:"))
        self.layout.add_widget(self.audio_path_input)
        self.select_button = Button(text="Seleccionar Archivo", size_hint=(1, None), height=40)
        self.select_button.bind(on_press=self.select_audio_file)
        self.layout.add_widget(self.select_button)

        # Transcription Button
        self.transcribe_button = Button(text="Iniciar Transcripción", size_hint=(1, None), height=50)
        self.transcribe_button.bind(on_press=self.start_transcription)
        self.layout.add_widget(self.transcribe_button)

        # Result Text
        self.result_text = TextInput(readonly=True, size_hint=(1, 1))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_text)
        self.layout.add_widget(scroll)

        return self.layout

    def select_audio_file(self, instance):
        from plyer import filechooser
        file_path = filechooser.open_file(filetypes=[("Archivos de audio", "*.mp3;*.wav;*.flac;*.m4a")])
        if file_path:
            absolute_path = os.path.abspath(file_path[0])
            self.audio_path_input.text = absolute_path

    def start_transcription(self, instance):
        api_key = self.api_key_input.text.strip()
        audio_file_path = self.audio_path_input.text.strip()

        if not api_key or not audio_file_path:
            self.update_result_text("Por favor, ingresa la API Key y selecciona un archivo de audio.\n")
            return

        if not os.path.isfile(audio_file_path):
            self.update_result_text("El archivo de audio seleccionado no existe.\n")
            return

        self.update_result_text("Iniciando transcripción...\n")
        threading.Thread(target=self.process_audio, args=(api_key, audio_file_path, OUTPUT_FILE), daemon=True).start()

    def update_result_text(self, message):
        self.result_text.text += message

    def split_audio(self, file_path, max_duration):
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            raise Exception(f"Error al abrir el archivo de audio: {e}")

        duration = len(audio)
        segments = []

        for start in range(0, duration, max_duration):
            end = min(start + max_duration, duration)
            segment = audio[start:end]
            segment_path = f"segment_{start // 1000}_{end // 1000}.mp3"
            try:
                segment.export(segment_path, format="mp3")
                segments.append(segment_path)
            except Exception as e:
                self.update_result_text(f"Error al exportar el segmento {segment_path}: {e}\n")

        return segments

    def transcribe_audio(self, api_key, audio_path):
        try:
            with open(audio_path, "rb") as audio_file:
                response = requests.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {api_key}"},
                    files={"file": (os.path.basename(audio_path), audio_file, "audio/mpeg")},
                    data={"model": "whisper-1"}
                )
        except Exception as e:
            self.update_result_text(f"Error al realizar la solicitud a la API: {e}\n")
            return ""

        try:
            response_data = response.json()
        except ValueError:
            self.update_result_text(f"Respuesta no válida de la API para el archivo {audio_path}: {response.text}\n")
            return ""

        if response.status_code == 200:
            return response_data.get("text", "")
        else:
            self.update_result_text(f"Error en la API para el archivo {audio_path}: {response_data}\n")
            return ""

    def process_audio(self, api_key, audio_file_path, output_file):
        try:
            segments = self.split_audio(audio_file_path, MAX_DURATION)
        except Exception as e:
            self.update_result_text(f"Error al dividir el audio: {e}\n")
            return

        if not segments:
            self.update_result_text("No se crearon segmentos de audio.\n")
            return

        all_text = []

        for segment_path in segments:
            self.update_result_text(f"Procesando fragmento: {segment_path}\n")
            text = self.transcribe_audio(api_key, segment_path)
            if text:
                all_text.append(text)
            else:
                self.update_result_text(f"Transcripción fallida para el fragmento: {segment_path}\n")
            try:
                os.remove(segment_path)
            except Exception as e:
                self.update_result_text(f"Error al borrar el segmento {segment_path}: {e}\n")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))
            self.update_result_text(f"Transcripción completada y guardada en {output_file}\n")
        except Exception as e:
            self.update_result_text(f"Error al guardar la transcripción: {e}\n")

if __name__ == '__main__':
    TranscriptionApp().run()
