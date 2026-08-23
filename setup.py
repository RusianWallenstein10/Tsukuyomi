import subprocess
import sys

def install():
    print("Instalando componentes de Tsukuyomi...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
    print("¡Instalación completada con éxito!")

if __name__ == "__main__":
    install()