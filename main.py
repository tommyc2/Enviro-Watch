import threading
import os

def run_script(script_name):
    os.system(f"python3 {script_name}")

if __name__ == "__main__":
    try:
        script1_thread = threading.Thread(target=run_script, args=("flask_server.py",))
        script2_thread = threading.Thread(target=run_script, args=("bme680_sensor.py",))

        script1_thread.start()
        script2_thread.start()

    except Exception as error:
        print("Error:", error)