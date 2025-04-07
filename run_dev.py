import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_app()

    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        print(f"\n🔄 Detectado cambio en {event.src_path}")
        self.restart_app()

    def start_app(self):
        print("\n🚀 Iniciando aplicación...")
        self.process = subprocess.Popen([sys.executable, "-m", "src.main"])

    def stop_app(self):
        if self.process:
            print("⏹️ Deteniendo aplicación...")
            self.process.terminate()
            self.process.wait()
            print("✅ Aplicación detenida")

    def restart_app(self):
        self.stop_app()
        self.start_app()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    path = "src"
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    print(f"👀 Vigilando cambios en la carpeta '{path}'...")
    print("⚡ Servidor en ejecución. Presiona Ctrl+C para detener.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo vigilancia de cambios...")
        observer.stop()
        event_handler.stop_app()
    
    observer.join()
    print("👋 ¡Hasta luego!")