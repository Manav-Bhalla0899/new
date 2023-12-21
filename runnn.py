import pyaudio
import socket
import threading

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
PORT = 12345  # You can change the port number if needed

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', PORT))

# Store the client addresses
client_addresses = set()

def audio_sender():
    stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            stream_out.write(data)
        except Exception as e:
            print("Error sending audio:", e)
            break

def audio_receiver():
    stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        try:
            audio_data = stream_in.read(CHUNK)
            for address in client_addresses:
                server_socket.sendto(audio_data, address)
        except Exception as e:
            print("Error receiving audio:", e)
            break

def client_listener():
    while True:
        data, addr = server_socket.recvfrom(1024)
        client_addresses.add(addr)

# Start threads for sending, receiving, and listening for clients
sender_thread = threading.Thread(target=audio_sender, daemon=True)
receiver_thread = threading.Thread(target=audio_receiver, daemon=True)
listener_thread = threading.Thread(target=client_listener, daemon=True)

sender_thread.start()
receiver_thread.start()
listener_thread.start()

# Wait for KeyboardInterrupt (Ctrl+C) to terminate the script
try:
    while True:
        continue
except KeyboardInterrupt:
    pass
finally:
    # Close the audio stream and socket
    audio.terminate()
    server_socket.close()
