pkgname=voice-transcriber
pkgver=1.0.0
pkgrel=1
pkgdesc="Voice to text transcription application"
arch=('any')
url="https://github.com/EdiAsllani/Voice-Transcriber"
license=('MIT')
depends=('python' 'tk' 'python-pyaudio')
makedepends=('python-setuptools' 'python-pip')
source=("$pkgname-$pkgver.tar.gz::https://github.com/EdiAsllani/Voice-Transcriber/archive/v$pkgver.tar.gz")
sha256sums=('89b989d963379e8e68909e862f792e491cbd238f7a022389b6dac52e7881e538')

package() {
    cd "$srcdir/Voice-Transcriber-$pkgver"
    
    # Install ALL Python dependencies with pip to ensure they're in the same location
    pip install --target "$pkgdir/usr/lib/python3.11/site-packages" faster-whisper customtkinter darkdetect
    
    # Install your app
    install -dm755 "$pkgdir/usr/lib/python3.11/site-packages/transcriber"
    cp -r transcriber/* "$pkgdir/usr/lib/python3.11/site-packages/transcriber/"
    
    # Install desktop file and icon
    install -Dm644 desktop/transcriber.desktop "$pkgdir/usr/share/applications/transcriber.desktop"
    install -Dm644 icons/icon.png "$pkgdir/usr/share/pixmaps/transcriber.png"
    
    # Create executable
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/voice-transcriber" << 'EOF'
#!/bin/bash
export PYTHONPATH="/usr/lib/python3.11/site-packages:$PYTHONPATH"
cd /usr/lib/python3.11/site-packages/transcriber
python3 displaygui.py
EOF
    chmod +x "$pkgdir/usr/bin/voice-transcriber"
}
