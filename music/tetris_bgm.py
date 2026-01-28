"""
Tetris Background Music - PC Beep Version
Korobeiniki (Russian folk song) theme
"""

import sys
import time
import threading
import os

# Note frequencies (Hz)
NOTES = {
    'REST': 0,
    'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784,
    'A5': 880, 'B5': 988,
    'C6': 1047,
}

# Korobeiniki melody (note, duration in beats)
TETRIS_THEME = [
    # Line 1
    ('E5', 1), ('B4', 0.5), ('C5', 0.5), ('D5', 1), ('C5', 0.5), ('B4', 0.5),
    ('A4', 1), ('A4', 0.5), ('C5', 0.5), ('E5', 1), ('D5', 0.5), ('C5', 0.5),
    ('B4', 1.5), ('C5', 0.5), ('D5', 1), ('E5', 1),
    ('C5', 1), ('A4', 1), ('A4', 1), ('REST', 1),
    # Line 2
    ('D5', 1.5), ('F5', 0.5), ('A5', 1), ('G5', 0.5), ('F5', 0.5),
    ('E5', 1.5), ('C5', 0.5), ('E5', 1), ('D5', 0.5), ('C5', 0.5),
    ('B4', 1), ('B4', 0.5), ('C5', 0.5), ('D5', 1), ('E5', 1),
    ('C5', 1), ('A4', 1), ('A4', 1), ('REST', 1),
]


def _generate_beep_wav(freq, duration_sec, sample_rate=22050):
    """Generate a simple sine wave beep as WAV bytes"""
    import struct
    import math

    n_samples = int(sample_rate * duration_sec)

    # Generate sine wave samples
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        # Sine wave with fade in/out to reduce clicks
        fade_samples = min(int(sample_rate * 0.01), n_samples // 4)
        amplitude = 16000
        if i < fade_samples:
            amplitude = int(16000 * (i / fade_samples))
        elif i > n_samples - fade_samples:
            amplitude = int(16000 * ((n_samples - i) / fade_samples))

        sample = int(amplitude * math.sin(2 * math.pi * freq * t))
        samples.append(struct.pack('<h', sample))

    # Build WAV file in memory
    data = b''.join(samples)
    wav = b'RIFF'
    wav += struct.pack('<I', 36 + len(data))
    wav += b'WAVEfmt '
    wav += struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
    wav += b'data'
    wav += struct.pack('<I', len(data))
    wav += data
    return wav


class BeepPlayer:
    """Cross-platform beep player"""

    def __init__(self, tempo=140):
        self.tempo = tempo
        self.playing = False
        self.thread = None
        self._setup_player()

    def _setup_player(self):
        """Setup platform-specific player"""
        self._temp_file = '/tmp/tetris_beep.wav'

        if sys.platform == 'win32':
            try:
                import winsound
                self._play_method = 'winsound'
                return
            except ImportError:
                pass

        if sys.platform == 'darwin':
            self._play_method = 'afplay'
            return

        # Linux or fallback
        self._play_method = 'bell'

    def _beep(self, freq, duration_ms):
        """Play a beep at given frequency and duration"""
        if freq <= 0:
            time.sleep(duration_ms / 1000)
            return

        duration_sec = duration_ms / 1000

        if self._play_method == 'winsound':
            import winsound
            winsound.Beep(int(freq), int(duration_ms))

        elif self._play_method == 'afplay':
            # Generate WAV and play with afplay
            wav_data = _generate_beep_wav(freq, duration_sec)
            with open(self._temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'afplay "{self._temp_file}" 2>/dev/null &')
            time.sleep(duration_sec * 0.95)

        else:
            # Terminal bell fallback
            print('\a', end='', flush=True)
            time.sleep(duration_sec)

    def _beat_to_ms(self, beats):
        """Convert beats to milliseconds based on tempo"""
        return (60000 / self.tempo) * beats

    def _play_loop(self, melody):
        """Play melody in loop"""
        while self.playing:
            for note, duration in melody:
                if not self.playing:
                    break
                freq = NOTES.get(note, 0)
                duration_ms = self._beat_to_ms(duration)
                self._beep(freq, duration_ms)

    def start(self, melody=None):
        """Start playing background music"""
        if melody is None:
            melody = TETRIS_THEME

        if self.playing:
            return

        self.playing = True
        self.thread = threading.Thread(target=self._play_loop, args=(melody,), daemon=True)
        self.thread.start()

    def stop(self):
        """Stop playing"""
        self.playing = False
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None
        # Clean up temp file
        if os.path.exists(self._temp_file):
            try:
                os.remove(self._temp_file)
            except:
                pass


# Global player instance
_player = None

def start_bgm(tempo=140):
    """Start tetris background music"""
    global _player
    if _player is None:
        _player = BeepPlayer(tempo=tempo)
    _player.start()

def stop_bgm():
    """Stop background music"""
    global _player
    if _player:
        _player.stop()

def play_once(tempo=140):
    """Play theme once (blocking)"""
    player = BeepPlayer(tempo=tempo)
    for note, duration in TETRIS_THEME:
        freq = NOTES.get(note, 0)
        duration_ms = player._beat_to_ms(duration)
        player._beep(freq, duration_ms)
    player.stop()


if __name__ == '__main__':
    print("Playing Tetris theme (Korobeiniki) with PC beep...")
    print("Press Ctrl+C to stop")
    try:
        play_once(tempo=120)
        print("\nDone!")
    except KeyboardInterrupt:
        print("\nStopped")
