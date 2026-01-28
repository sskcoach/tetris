"""
Tetris Background Music - PC Beep Version
Korobeiniki (Russian folk song) Theme A
Based on: https://github.com/lambdaloop/NXT_tunes/tree/master/tetris
"""

import sys
import time
import threading
import os
import struct
import math

# Note frequencies (Hz) - accurate values
NOTES = {
    'REST': 0, 'R': 0,
    # Octave 2
    'C2': 65, 'D2': 73, 'E2': 82, 'F2': 87, 'G2': 98, 'G#2': 104, 'A2': 110, 'B2': 123,
    # Octave 3
    'C3': 131, 'D3': 147, 'E3': 165, 'G#3': 208, 'A3': 220, 'B3': 247,
    # Octave 4
    'C4': 262, 'D4': 294, 'E4': 330, 'G#4': 415, 'A4': 440, 'B4': 494,
    # Octave 5
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880,
    # Octave 6
    'C6': 1047,
}

# Theme A - Main melody (note, duration in beats) @ 140 BPM
# More accurate transcription from NXT_tunes
THEME_A_MELODY = [
    # Section 1-8 (main theme)
    ('E5', 1), ('B4', 0.5), ('C5', 0.5), ('D5', 0.5), ('E5', 0.25), ('D5', 0.25),
    ('C5', 0.5), ('B4', 0.5), ('A4', 1), ('A4', 0.5), ('C5', 0.5),
    ('E5', 1), ('D5', 0.5), ('C5', 0.5), ('B4', 1.5), ('C5', 0.5),
    ('D5', 1), ('E5', 1), ('C5', 1), ('A4', 1), ('A4', 2),
    ('REST', 0.5),
    # Section 5-8
    ('D5', 1), ('F5', 0.5), ('A5', 1), ('G5', 0.5), ('F5', 0.5),
    ('E5', 1.5), ('C5', 0.5), ('E5', 1), ('D5', 0.5), ('C5', 0.5),
    ('B4', 1), ('B4', 0.5), ('C5', 0.5), ('D5', 1), ('E5', 1),
    ('C5', 1), ('A4', 1), ('A4', 1), ('REST', 1),
]

# Theme A - Lower section (bridge)
THEME_A_BRIDGE = [
    ('E4', 2), ('C4', 2), ('D4', 2), ('B3', 2),
    ('C4', 2), ('A3', 2), ('G#3', 2), ('B3', 2),
    ('E4', 2), ('C4', 2), ('D4', 2), ('B3', 2),
    ('C4', 1), ('E4', 1), ('A4', 2), ('G#4', 4),
]

# Bass line (accompaniment)
BASS_LINE = [
    # E minor pattern
    ('E2', 0.5), ('E3', 0.5), ('E2', 0.5), ('E3', 0.5),
    ('E2', 0.5), ('E3', 0.5), ('E2', 0.5), ('E3', 0.5),
    # A minor pattern
    ('A2', 0.5), ('A3', 0.5), ('A2', 0.5), ('A3', 0.5),
    ('A2', 0.5), ('A3', 0.5), ('A2', 0.5), ('A3', 0.5),
    # G# diminished
    ('G#2', 0.5), ('G#3', 0.5), ('G#2', 0.5), ('G#3', 0.5),
    ('G#2', 0.5), ('G#3', 0.5), ('G#2', 0.5), ('G#3', 0.5),
    # B pattern
    ('B2', 0.5), ('B3', 0.5), ('B2', 0.5), ('B3', 0.5),
    ('B2', 0.5), ('B3', 0.5), ('B2', 0.5), ('B3', 0.5),
]

# Full Tetris Theme (melody + bridge, then repeat)
TETRIS_THEME = THEME_A_MELODY + THEME_A_MELODY + THEME_A_BRIDGE

# Simple version for quick play
TETRIS_SIMPLE = THEME_A_MELODY


def _generate_beep_wav(freq, duration_sec, sample_rate=22050, volume=0.8):
    """Generate a simple sine wave beep as WAV bytes"""
    n_samples = int(sample_rate * duration_sec)
    if n_samples == 0:
        n_samples = 1

    # Generate sine wave samples
    samples = []
    base_amplitude = int(16000 * volume)

    for i in range(n_samples):
        t = i / sample_rate
        # Fade in/out to reduce clicks
        fade_samples = min(int(sample_rate * 0.008), n_samples // 4)
        amplitude = base_amplitude

        if fade_samples > 0:
            if i < fade_samples:
                amplitude = int(base_amplitude * (i / fade_samples))
            elif i > n_samples - fade_samples:
                amplitude = int(base_amplitude * ((n_samples - i) / fade_samples))

        sample = int(amplitude * math.sin(2 * math.pi * freq * t))
        samples.append(struct.pack('<h', max(-32768, min(32767, sample))))

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
    """Cross-platform beep player for Tetris BGM"""

    def __init__(self, tempo=180):
        self.tempo = tempo  # Default 180 BPM
        self.playing = False
        self.thread = None
        self._temp_file = '/tmp/tetris_beep.wav'
        self._play_method = self._detect_play_method()
        self._note_counter = 0

    def _detect_play_method(self):
        """Detect platform-specific play method"""
        if sys.platform == 'win32':
            try:
                import winsound
                return 'winsound'
            except ImportError:
                pass

        if sys.platform == 'darwin':
            return 'afplay'

        # Linux: try aplay, paplay, or fallback
        for cmd in ['aplay', 'paplay']:
            if os.system(f'which {cmd} > /dev/null 2>&1') == 0:
                return cmd

        return 'bell'

    def _get_temp_file(self):
        """Get unique temp file to avoid conflicts"""
        self._note_counter = (self._note_counter + 1) % 2
        return f'/tmp/tetris_beep_{self._note_counter}.wav'

    def _beep(self, freq, duration_ms, volume=0.8):
        """Play a beep at given frequency and duration"""
        if freq <= 0:
            time.sleep(duration_ms / 1000)
            return

        duration_sec = duration_ms / 1000

        if self._play_method == 'winsound':
            import winsound
            winsound.Beep(int(freq), int(duration_ms))

        elif self._play_method == 'afplay':
            wav_data = _generate_beep_wav(freq, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            # Run afplay in background, control timing with sleep
            os.system(f'afplay "{temp_file}" 2>/dev/null &')
            time.sleep(duration_sec)

        elif self._play_method in ['aplay', 'paplay']:
            wav_data = _generate_beep_wav(freq, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'{self._play_method} "{temp_file}" 2>/dev/null &')
            time.sleep(duration_sec)

        else:
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
        """Start playing background music in a thread"""
        if melody is None:
            melody = TETRIS_SIMPLE

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
        self._cleanup()

    def _cleanup(self):
        """Clean up temp files"""
        for i in range(2):
            temp_file = f'/tmp/tetris_beep_{i}.wav'
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass


# Global player instance
_player = None


def start_bgm(tempo=180, full=False):
    """Start tetris background music

    Args:
        tempo: BPM (default 180)
        full: If True, play full theme with bridge. If False, play simple melody.
    """
    global _player
    if _player is None:
        _player = BeepPlayer(tempo=tempo)

    melody = TETRIS_THEME if full else TETRIS_SIMPLE
    _player.start(melody)


def stop_bgm():
    """Stop background music"""
    global _player
    if _player:
        _player.stop()


def play_once(tempo=180, full=False):
    """Play theme once (blocking)

    Args:
        tempo: BPM (default 180)
        full: If True, play full theme. If False, play simple melody.
    """
    player = BeepPlayer(tempo=tempo)
    melody = TETRIS_THEME if full else TETRIS_SIMPLE

    for note, duration in melody:
        freq = NOTES.get(note, 0)
        duration_ms = player._beat_to_ms(duration)
        player._beep(freq, duration_ms)

    player._cleanup()


def play_bridge(tempo=180):
    """Play the bridge section only (blocking)"""
    player = BeepPlayer(tempo=tempo)

    for note, duration in THEME_A_BRIDGE:
        freq = NOTES.get(note, 0)
        duration_ms = player._beat_to_ms(duration)
        player._beep(freq, duration_ms)

    player._cleanup()


if __name__ == '__main__':
    print("Tetris Theme A (Korobeiniki) - PC Beep Version")
    print("Based on: github.com/lambdaloop/NXT_tunes/tree/master/tetris")
    print("Press Ctrl+C to stop\n")

    import argparse
    parser = argparse.ArgumentParser(description='Play Tetris BGM')
    parser.add_argument('--tempo', type=int, default=180, help='BPM (default: 180)')
    parser.add_argument('--full', action='store_true', help='Play full theme with bridge')
    parser.add_argument('--bridge', action='store_true', help='Play bridge section only')
    args = parser.parse_args()

    try:
        if args.bridge:
            print("Playing bridge section...")
            play_bridge(tempo=args.tempo)
        else:
            mode = "full theme" if args.full else "main melody"
            print(f"Playing {mode} at {args.tempo} BPM...")
            play_once(tempo=args.tempo, full=args.full)
        print("\nDone!")
    except KeyboardInterrupt:
        print("\nStopped")
