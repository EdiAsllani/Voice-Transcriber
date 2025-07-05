# Voice Transcriber

A voice-to-text transcription application with a modern GUI built using Python and CustomTkinter.

## Features

- Real-time voice recording and transcription
- File-based audio transcription
- Modern, user-friendly interface
- Powered by OpenAI's Whisper model via faster-whisper

## Installation

### Arch Linux (Recommended)

#### Prerequisites
- `base-devel` package group
- `git`
- An AUR helper like `yay` or `paru`

#### Install Dependencies
```bash
# Install system dependencies
sudo pacman -S python tk python-pyaudio python-darkdetect

# Install CustomTkinter from AUR
yay -S python-customtkinter
# OR
paru -S python-customtkinter
```

#### Build and Install from PKGBUILD
1. Download the PKGBUILD from the releases
2. Extract and navigate to the directory
3. Build and install:
```bash
makepkg -si
```

#### Alternative: Install from AUR (if available)
```bash
yay -S voice-transcriber
# OR
paru -S voice-transcriber
```

### Other Linux Distributions

#### Prerequisites
- Python 3.7+
- pip
- tkinter (usually comes with Python)
- PortAudio development files

#### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-tk portaudio19-dev

# Install Python dependencies
pip3 install --user faster-whisper customtkinter darkdetect pyaudio

# Clone and run
git clone https://github.com/EdiAsllani/Voice-Transcriber.git
cd Voice-Transcriber
python3 transcriber/displaygui.py
```

#### CentOS/RHEL/Fedora
```bash
# Install system dependencies
sudo dnf install python3 python3-pip tkinter portaudio-devel
# OR for older versions:
# sudo yum install python3 python3-pip tkinter portaudio-devel

# Install Python dependencies
pip3 install --user faster-whisper customtkinter darkdetect pyaudio

# Clone and run
git clone https://github.com/EdiAsllani/Voice-Transcriber.git
cd Voice-Transcriber
python3 transcriber/displaygui.py
```

## Usage

### Starting the Application

#### Arch Linux (if installed via PKGBUILD)
```bash
voice-transcriber
```

#### Other Systems
```bash
python3 transcriber/displaygui.py
```

### Using the Application

1. **Record Audio**: Click the "Record" button to start recording your voice. Click "Stop" to end recording.

2. **Transcribe File**: Click "Select Audio File" to choose an existing audio file for transcription.

3. **View Results**: Transcribed text will appear in the text area.

4. **Save Results**: Copy the text or save it to a file as needed.

## Supported Audio Formats

- WAV
- MP3
- FLAC
- M4A
- OGG
- And other formats supported by faster-whisper

## System Requirements

### Minimum Requirements
- 4GB RAM
- 2GB free disk space
- Microphone (for recording)

### Recommended Requirements
- 8GB RAM or more
- 4GB free disk space
- Good quality microphone
- GPU with CUDA support (for faster transcription)

## Troubleshooting

### Common Issues

#### "No module named 'faster_whisper'" Error
- Ensure all dependencies are installed correctly
- Try reinstalling: `pip install --upgrade faster-whisper`

#### Audio Recording Issues
- Check microphone permissions
- Ensure PortAudio is properly installed
- On Linux, you might need to install `pulseaudio-dev` or `alsa-dev`

#### GUI Not Appearing
- Ensure tkinter is installed
- Try: `python3 -m tkinter` to test tkinter installation

#### Slow Transcription
- Consider using a GPU-accelerated version of faster-whisper
- Close other applications to free up system resources
- Use shorter audio files for testing

### Getting Help

If you encounter issues:
1. Check the [GitHub Issues](https://github.com/EdiAsllani/Voice-Transcriber/issues) page
2. Create a new issue with detailed information about your problem
3. Include your operating system, Python version, and error messages

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Building from Source
See the installation instructions for your platform above.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

- Built with [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- GUI created using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Based on OpenAI's Whisper model

---

**Note**: This application is currently Linux-only. The PKGBUILD is specifically designed for Arch Linux. For other distributions, use the manual installation methods described above.