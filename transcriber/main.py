from faster_whisper import WhisperModel
import pyaudio
import wave
import tempfile
import os
import sys
from tkinter import filedialog

def pre_download_model():
    """Pre-download the model to cache"""
    print("Pre-downloading Whisper model...")
    print("This will download the model to your cache for faster future loading.")
    print("Please wait...")
    
    try:
        # This will download and cache the model
        model = WhisperModel("small", device="cpu", compute_type="auto")
        print("✓ Model downloaded and cached successfully!")
        print("Future loads will be much faster!")
        return model
    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        return None

def initialize_model():
    """Initialize the Whisper model (should be fast if pre-downloaded)"""
    print("Loading Whisper model from cache...")
    try:
        model = WhisperModel("small", device="cpu", compute_type="auto")
        print("✓ Model loaded successfully!")
        return model
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("Try running pre-download first!")
        sys.exit(1)

def record_audio(duration=5):
    """Record audio from microphone"""
    # Audio settings
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    print(f"\n🎤 Recording for {duration} seconds...")
    print("Speak now!")
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    try:
        # Open stream
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        frames = []
        
        # Record audio
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("🔴 Recording finished!")
        
        # Close stream
        stream.stop_stream()
        stream.close()
        
    except Exception as e:
        print(f"✗ Recording error: {e}")
        return None
    finally:
        p.terminate()
    
    # Save to temporary file
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        wf = wave.open(temp_file.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return temp_file.name
    except Exception as e:
        print(f"✗ Error saving audio: {e}")
        return None

def transcribe_audio(model, audio_file):
    """Transcribe audio file to text"""
    print("🔄 Converting speech to text...")
    
    try:
        segments, info = model.transcribe(audio_file, beam_size=5)
        
        # Combine all segments into one text
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "
        
        return full_text.strip(), info.language
    except Exception as e:
        print(f"✗ Transcription error: {e}")
        return None, None

def select_audio_file():
    """Select an audio file and return path"""
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[
            ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma"),
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("M4A files", "*.m4a"),
            ("All files", "*.*")
        ]
    )
    return file_path

def transcribe_file_with_dialog(model):
    """Transcribe an audio file selected via file dialog"""
    
    # Open file dialog to select audio file
    file_path = select_audio_file()
    
    # Check if user cancelled the dialog
    if not file_path:
        print("No file selected")
        return None
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    print(f"Transcribing file: {file_path}")
    text, language = transcribe_audio(model, file_path)
    
    if text:
        print(f"🎯 Transcription (Language: {language}):")
        print(text)
        print(f"📝 " + "="*50)
        print(text)
        print("="*50)
    else:
        print("❌ Failed to transcribe file")
    
    return file_path

def transcribe_file(model, file_path):
    """Transcribe an existing audio file"""
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print(f"Transcribing file: {file_path}")
    text, language = transcribe_audio(model, file_path)
    
    if text:
        print(f"🎯 Transcription (Language: {language}):")
        print(text)
        print(f"📝 " + "="*50)
        print(text)
        print("="*50)
    else:
        print("❌ Failed to transcribe file")

def record_and_transcribe(model):
    """Record from microphone and transcribe"""
    try:
        duration = int(input("Enter recording duration in seconds (default 5): ") or "5")
    except ValueError:
        duration = 5
    
    # Record audio
    audio_file = record_audio(duration)
    if not audio_file:
        return
    
    # Transcribe
    text, language = transcribe_audio(model, audio_file)
    
    # Clean up temporary file
    try:
        os.unlink(audio_file)
    except:
        pass
    
    if text:
        print(f"\n📝 You said (Language: {language}):")
        print("-" * 50)
        print(text)
        print("-" * 50)
    else:
        print("✗ Failed to transcribe audio")

def main():
    """Main program loop"""
    print("🎙️  Simple Voice-to-Text Program")
    print("=" * 40)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Pre-download model (run this first!)")
        print("2. Record from microphone and transcribe")
        print("3. Transcribe an audio file")
        print("4. Quit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            model = pre_download_model()
            if model:
                print("Model is ready for use!")
        
        elif choice == "2":
            model = initialize_model()
            record_and_transcribe(model)
        
        elif choice == "3":
            model = initialize_model()
            file_path = input("Enter path to audio file: ").strip()
            transcribe_file(model, file_path)
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
