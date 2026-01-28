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
import select

# For non-blocking keyboard input
if sys.platform != 'win32':
    import termios
    import tty

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

# Bass line (accompaniment) - accurate from NXT_tunes
# Pattern matches melody sections
BASS_LINE_A = [
    # Measure 1-2: E pattern (4 beats)
    ('E2', 0.5), ('E2', 0.5), ('E2', 0.5), ('E2', 0.5),
    ('E2', 0.5), ('E2', 0.5), ('E2', 0.5), ('E2', 0.5),
    # Measure 3-4: A pattern (4 beats)
    ('A2', 0.5), ('A2', 0.5), ('A2', 0.5), ('A2', 0.5),
    ('A2', 0.5), ('A2', 0.5), ('A2', 0.5), ('A2', 0.5),
    # Measure 5-6: G# pattern (4 beats)
    ('G#2', 0.5), ('G#2', 0.5), ('G#2', 0.5), ('G#2', 0.5),
    ('G#2', 0.5), ('G#2', 0.5), ('G#2', 0.5), ('G#2', 0.5),
    # Measure 7-8: A -> B pattern (4 beats)
    ('A2', 0.5), ('A2', 0.5), ('A2', 0.5), ('B2', 0.5),
    ('A2', 0.5), ('A2', 0.5), ('A2', 1),
]

BASS_LINE_B = [
    # Measure 1-2: D -> A -> F (4 beats)
    ('D2', 0.5), ('D2', 0.5), ('D2', 0.5), ('A2', 0.5),
    ('F2', 0.5), ('F2', 0.5), ('F2', 0.5), ('F2', 0.5),
    # Measure 3-4: C -> G (4 beats)
    ('C2', 0.5), ('C2', 0.5), ('G2', 0.5), ('G2', 0.5),
    ('G2', 0.5), ('G2', 0.5), ('G2', 0.5), ('G2', 0.5),
    # Measure 5-6: B pattern (4 beats)
    ('B2', 0.5), ('B2', 0.5), ('B2', 0.5), ('B2', 0.5),
    ('B2', 0.5), ('B2', 0.5), ('B2', 0.5), ('B2', 0.5),
    # Measure 7-8: A pattern (4 beats)
    ('A2', 0.5), ('A2', 0.5), ('A2', 0.5), ('A2', 0.5),
    ('A2', 0.5), ('A2', 0.5), ('A2', 1),
]

# Combined bass for full melody
BASS_LINE = BASS_LINE_A + BASS_LINE_B

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


def _generate_chord_wav(freqs, duration_sec, sample_rate=22050, volume=0.7):
    """Generate multiple frequencies mixed together as WAV bytes"""
    n_samples = int(sample_rate * duration_sec)
    if n_samples == 0:
        n_samples = 1

    # Filter out zero frequencies
    freqs = [f for f in freqs if f > 0]
    if not freqs:
        # Generate silence
        data = b'\x00\x00' * n_samples
        wav = b'RIFF'
        wav += struct.pack('<I', 36 + len(data))
        wav += b'WAVEfmt '
        wav += struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
        wav += b'data'
        wav += struct.pack('<I', len(data))
        wav += data
        return wav

    samples = []
    # Divide amplitude by number of frequencies to prevent clipping
    base_amplitude = int(14000 * volume / len(freqs))

    for i in range(n_samples):
        t = i / sample_rate
        fade_samples = min(int(sample_rate * 0.008), n_samples // 4)
        amplitude = base_amplitude

        if fade_samples > 0:
            if i < fade_samples:
                amplitude = int(base_amplitude * (i / fade_samples))
            elif i > n_samples - fade_samples:
                amplitude = int(base_amplitude * ((n_samples - i) / fade_samples))

        # Mix all frequencies
        sample_val = 0
        for freq in freqs:
            sample_val += int(amplitude * math.sin(2 * math.pi * freq * t))

        samples.append(struct.pack('<h', max(-32768, min(32767, sample_val))))

    data = b''.join(samples)
    wav = b'RIFF'
    wav += struct.pack('<I', 36 + len(data))
    wav += b'WAVEfmt '
    wav += struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
    wav += b'data'
    wav += struct.pack('<I', len(data))
    wav += data
    return wav


def _generate_full_track_wav(melody, bass, tempo, sample_rate=22050, volume=0.7, repeats=1):
    """Generate complete track with melody and bass pre-mixed into single WAV

    This avoids note-by-note playback gaps by rendering everything upfront.

    Args:
        melody: List of (note, duration) tuples
        bass: List of (note, duration) tuples for bass line
        tempo: BPM
        sample_rate: Audio sample rate
        volume: Volume level (0-1)
        repeats: Number of times to repeat the melody (for seamless looping)
    """
    beat_to_sec = lambda beats: (60.0 / tempo) * beats

    # Repeat melody for seamless looping
    full_melody = melody * repeats

    # Calculate total duration
    melody_duration = sum(beat_to_sec(d) for _, d in full_melody)
    total_samples = int(sample_rate * melody_duration)

    # Extend bass to match melody length
    if bass:
        bass_duration = sum(beat_to_sec(d) for _, d in bass)
        full_bass = bass * (int(melody_duration / bass_duration) + 1)
    else:
        full_bass = None

    # Pre-allocate sample buffer
    samples = [0.0] * total_samples

    # Render melody track
    melody_amp = 12000 * volume
    current_sample = 0
    for note, duration in full_melody:
        freq = NOTES.get(note, 0)
        dur_sec = beat_to_sec(duration)
        n_samples = int(sample_rate * dur_sec)

        if freq > 0:
            for i in range(n_samples):
                if current_sample + i >= total_samples:
                    break
                t = i / sample_rate
                # Envelope: attack/release
                env = 1.0
                attack = min(int(sample_rate * 0.01), n_samples // 4)
                release = min(int(sample_rate * 0.02), n_samples // 4)
                if i < attack:
                    env = i / attack
                elif i > n_samples - release:
                    env = (n_samples - i) / release
                samples[current_sample + i] += melody_amp * env * math.sin(2 * math.pi * freq * t)

        current_sample += n_samples

    # Render bass track
    if full_bass:
        bass_amp = 10000 * volume
        current_sample = 0
        for note, duration in full_bass:
            if current_sample >= total_samples:
                break
            freq = NOTES.get(note, 0)
            dur_sec = beat_to_sec(duration)
            n_samples = int(sample_rate * dur_sec)

            if freq > 0:
                for i in range(n_samples):
                    if current_sample + i >= total_samples:
                        break
                    t = i / sample_rate
                    env = 1.0
                    attack = min(int(sample_rate * 0.005), n_samples // 4)
                    release = min(int(sample_rate * 0.01), n_samples // 4)
                    if i < attack:
                        env = i / attack
                    elif i > n_samples - release:
                        env = (n_samples - i) / release
                    samples[current_sample + i] += bass_amp * env * math.sin(2 * math.pi * freq * t)

            current_sample += n_samples

    # Convert to bytes
    data = b''.join(
        struct.pack('<h', max(-32768, min(32767, int(s))))
        for s in samples
    )

    # Build WAV
    wav = b'RIFF'
    wav += struct.pack('<I', 36 + len(data))
    wav += b'WAVEfmt '
    wav += struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
    wav += b'data'
    wav += struct.pack('<I', len(data))
    wav += data
    return wav, melody_duration


class KeyboardInput:
    """Non-blocking keyboard input handler"""

    def __init__(self):
        self.stopped = False
        self._old_settings = None

    def start(self):
        """Enable raw terminal mode for key detection"""
        if sys.platform != 'win32':
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def stop(self):
        """Restore terminal settings"""
        if sys.platform != 'win32' and self._old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def check_key(self):
        """Check if a key was pressed (non-blocking), return the key or None"""
        if sys.platform == 'win32':
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8', errors='ignore')
            return None
        else:
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
            return None


class BeepPlayer:
    """Cross-platform beep player for Tetris BGM"""

    def __init__(self, tempo=120):
        self.tempo = tempo  # Default 120 BPM
        self.playing = False
        self.stopped_by_user = False
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

    def _play_note(self, freq, duration_sec, volume=0.8):
        """Play a single note (non-blocking, returns immediately)"""
        if freq <= 0:
            return

        if self._play_method == 'winsound':
            import winsound
            # winsound.Beep is blocking, run in thread
            threading.Thread(
                target=lambda: winsound.Beep(int(freq), int(duration_sec * 1000)),
                daemon=True
            ).start()

        elif self._play_method == 'afplay':
            wav_data = _generate_beep_wav(freq, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'afplay "{temp_file}" 2>/dev/null &')

        elif self._play_method in ['aplay', 'paplay']:
            wav_data = _generate_beep_wav(freq, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'{self._play_method} "{temp_file}" 2>/dev/null &')

        else:
            print('\a', end='', flush=True)

    def _play_chord(self, freqs, duration_sec, volume=0.7):
        """Play multiple frequencies together (non-blocking)"""
        freqs = [f for f in freqs if f > 0]
        if not freqs:
            return

        if self._play_method == 'afplay':
            wav_data = _generate_chord_wav(freqs, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'afplay "{temp_file}" 2>/dev/null &')

        elif self._play_method in ['aplay', 'paplay']:
            wav_data = _generate_chord_wav(freqs, duration_sec, volume=volume)
            temp_file = self._get_temp_file()
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            os.system(f'{self._play_method} "{temp_file}" 2>/dev/null &')

        else:
            # Fallback: just play first frequency
            self._play_note(freqs[0], duration_sec, volume)

    def _beat_to_sec(self, beats):
        """Convert beats to seconds based on tempo"""
        return (60.0 / self.tempo) * beats

    def _play_loop(self, melody):
        """Play melody in loop with real-time sync"""
        while self.playing:
            start_time = time.time()
            for i, (note, duration) in enumerate(melody):
                if not self.playing:
                    break
                freq = NOTES.get(note, 0)
                duration_sec = self._beat_to_sec(duration)

                # Calculate absolute time for this note
                note_start = start_time + sum(self._beat_to_sec(d) for _, d in melody[:i])

                # Wait until it's time to play this note
                wait_time = note_start - time.time()
                if wait_time > 0:
                    time.sleep(wait_time)

                if not self.playing:
                    break

                # Play the note
                self._play_note(freq, duration_sec)

    def play_once_with_keys(self, melody, keyboard=None):
        """Play melody once with keyboard checking (blocking)

        Args:
            melody: List of (note, duration) tuples
            keyboard: KeyboardInput instance for key detection

        Returns:
            True if completed, False if stopped by 'q'
        """
        self.playing = True
        self.stopped_by_user = False
        start_time = time.time()

        for i, (note, duration) in enumerate(melody):
            if not self.playing:
                break

            freq = NOTES.get(note, 0)
            duration_sec = self._beat_to_sec(duration)

            # Calculate absolute time for next note
            next_note_time = start_time + sum(self._beat_to_sec(d) for _, d in melody[:i+1])

            # Play the note
            self._play_note(freq, duration_sec)

            # Wait with key checking
            while time.time() < next_note_time:
                if keyboard:
                    key = keyboard.check_key()
                    if key and key.lower() == 'q':
                        self.playing = False
                        self.stopped_by_user = True
                        # Kill any playing audio
                        os.system('pkill -9 afplay 2>/dev/null')
                        return False

                # Small sleep to avoid busy waiting
                remaining = next_note_time - time.time()
                if remaining > 0:
                    time.sleep(min(0.01, remaining))

        self.playing = False
        return True

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
        # Kill any playing audio
        if sys.platform == 'darwin':
            os.system('pkill -9 afplay 2>/dev/null')
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


def start_bgm(tempo=120, full=False):
    """Start tetris background music

    Args:
        tempo: BPM (default 120)
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


def _merge_tracks(melody, bass, beat_to_sec_func):
    """Merge melody and bass into time-aligned events

    Returns list of (time, melody_freq, bass_freq, duration) tuples
    """
    events = []

    # Build melody timeline
    melody_time = 0
    for note, duration in melody:
        freq = NOTES.get(note, 0)
        dur_sec = beat_to_sec_func(duration)
        events.append(('melody', melody_time, freq, dur_sec))
        melody_time += dur_sec

    # Build bass timeline
    bass_time = 0
    for note, duration in bass:
        freq = NOTES.get(note, 0)
        dur_sec = beat_to_sec_func(duration)
        events.append(('bass', bass_time, freq, dur_sec))
        bass_time += dur_sec

    # Sort by time
    events.sort(key=lambda x: x[1])

    # Merge overlapping events at same time
    merged = []
    i = 0
    while i < len(events):
        current_time = events[i][1]
        melody_freq = 0
        bass_freq = 0
        min_duration = float('inf')

        # Collect all events at this time
        while i < len(events) and abs(events[i][1] - current_time) < 0.001:
            track, _, freq, dur = events[i]
            if track == 'melody':
                melody_freq = freq
            else:
                bass_freq = freq
            min_duration = min(min_duration, dur)
            i += 1

        merged.append((current_time, melody_freq, bass_freq, min_duration))

    return merged


def play_once(tempo=120, full=False, check_keys=True, with_bass=False):
    """Play theme once (blocking)

    Args:
        tempo: BPM (default 120)
        full: If True, play full theme. If False, play simple melody.
        check_keys: If True, check for 'q' key to stop.
        with_bass: If True, play melody + bass together (2 tracks).

    Returns:
        True if completed, False if stopped by user
    """
    player = BeepPlayer(tempo=tempo)
    melody = TETRIS_THEME if full else TETRIS_SIMPLE

    if not with_bass:
        # Single track: note-by-note playback
        if check_keys:
            keyboard = KeyboardInput()
            keyboard.start()
            try:
                result = player.play_once_with_keys(melody, keyboard)
            finally:
                keyboard.stop()
                player._cleanup()
            return result
        else:
            start_time = time.time()
            for i, (note, duration) in enumerate(melody):
                freq = NOTES.get(note, 0)
                duration_sec = player._beat_to_sec(duration)
                next_note_time = start_time + sum(player._beat_to_sec(d) for _, d in melody[:i+1])
                player._play_note(freq, duration_sec)
                wait_time = next_note_time - time.time()
                if wait_time > 0:
                    time.sleep(wait_time)
            player._cleanup()
            return True

    # 2-track playback: pre-render entire track as single WAV
    print("Generating audio...", end=" ", flush=True)
    wav_data, duration = _generate_full_track_wav(melody, BASS_LINE, tempo)
    print("Done!")

    temp_file = '/tmp/tetris_full_track.wav'
    with open(temp_file, 'wb') as f:
        f.write(wav_data)

    keyboard = None
    if check_keys:
        keyboard = KeyboardInput()
        keyboard.start()

    try:
        # Play the pre-rendered track
        if sys.platform == 'darwin':
            os.system(f'afplay "{temp_file}" 2>/dev/null &')
        elif sys.platform == 'win32':
            import winsound
            threading.Thread(
                target=lambda: winsound.PlaySound(temp_file, winsound.SND_FILENAME),
                daemon=True
            ).start()
        else:
            os.system(f'aplay "{temp_file}" 2>/dev/null &')

        # Wait with key checking
        start_time = time.time()
        while time.time() - start_time < duration:
            if keyboard:
                key = keyboard.check_key()
                if key and key.lower() == 'q':
                    os.system('pkill -9 afplay 2>/dev/null')
                    return False
            time.sleep(0.05)

        return True

    finally:
        if keyboard:
            keyboard.stop()
        # Clean up
        time.sleep(0.1)  # Let audio finish
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
        player._cleanup()


def play_bridge(tempo=120, check_keys=True):
    """Play the bridge section only (blocking)

    Returns:
        True if completed, False if stopped by user
    """
    player = BeepPlayer(tempo=tempo)

    if check_keys:
        keyboard = KeyboardInput()
        keyboard.start()
        try:
            result = player.play_once_with_keys(THEME_A_BRIDGE, keyboard)
        finally:
            keyboard.stop()
            player._cleanup()
        return result
    else:
        start_time = time.time()
        for i, (note, duration) in enumerate(THEME_A_BRIDGE):
            freq = NOTES.get(note, 0)
            duration_sec = player._beat_to_sec(duration)
            next_note_time = start_time + sum(player._beat_to_sec(d) for _, d in THEME_A_BRIDGE[:i+1])
            player._play_note(freq, duration_sec)
            wait_time = next_note_time - time.time()
            if wait_time > 0:
                time.sleep(wait_time)
        player._cleanup()
        return True


def _visualize_note(note, freq, is_bass=False):
    """Generate visual representation of a note"""
    if freq == 0:
        return "  REST  "

    # Note to piano key position (C2=0 to C6=48)
    note_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    try:
        # Parse note name (e.g., "E5" -> "E", "5")
        if '#' in note:
            name, octave = note[:-1], int(note[-1])
        else:
            name, octave = note[:-1], int(note[-1])
        pos = note_order.index(name) + (octave - 2) * 12
    except (ValueError, IndexError):
        pos = 24  # Default middle

    # Create bar visualization (max 40 chars)
    bar_len = min(40, max(1, pos))
    if is_bass:
        bar = '░' * bar_len
        return f"{note:>4} {bar}"
    else:
        bar = '█' * bar_len
        return f"{note:>4} {bar}"


def play_with_visualization(tempo=120, full=False, with_bass=False, check_keys=True):
    """Play with real-time note visualization (pre-rendered audio)"""
    melody = TETRIS_THEME if full else TETRIS_SIMPLE
    beat_to_sec = lambda beats: (60.0 / tempo) * beats

    # Extend bass
    if with_bass:
        melody_len = sum(d for _, d in melody)
        bass_len = sum(d for _, d in BASS_LINE)
        bass = BASS_LINE * (int(melody_len / bass_len) + 1)
    else:
        bass = None

    # Pre-render entire track
    print("Generating audio...", end=" ", flush=True)
    wav_data, total_duration = _generate_full_track_wav(
        melody, BASS_LINE if with_bass else None, tempo
    )
    print("Done!")

    temp_file = '/tmp/tetris_visual.wav'
    with open(temp_file, 'wb') as f:
        f.write(wav_data)

    keyboard = None
    if check_keys:
        keyboard = KeyboardInput()
        try:
            keyboard.start()
        except Exception:
            keyboard = None

    # Header
    print("\033[2J\033[H")  # Clear screen
    print("╔════════════════════════════════════════════════════╗")
    print("║  TETRIS BGM - Press 'q' to stop                    ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║  C2        C3        C4        C5        C6        ║")
    print("║  │         │         │         │         │         ║")
    print("╚════════════════════════════════════════════════════╝")

    try:
        # Start audio playback
        os.system(f'afplay "{temp_file}" 2>/dev/null &')

        start_time = time.time()
        melody_idx = 0
        bass_idx = 0
        melody_time = 0
        bass_time = 0

        while melody_idx < len(melody):
            elapsed = time.time() - start_time

            # Check for quit
            if keyboard:
                key = keyboard.check_key()
                if key and key.lower() == 'q':
                    os.system('pkill -9 afplay 2>/dev/null')
                    return False

            # Get current notes based on time
            m_note, m_dur = melody[melody_idx]
            m_freq = NOTES.get(m_note, 0)
            m_dur_sec = beat_to_sec(m_dur)

            if bass and bass_idx < len(bass):
                b_note, b_dur = bass[bass_idx]
                b_freq = NOTES.get(b_note, 0)
                b_dur_sec = beat_to_sec(b_dur)
            else:
                b_note, b_freq = 'REST', 0

            # Visualize current notes
            print(f"\033[8;1H")  # Move cursor
            print(f"  Melody: {_visualize_note(m_note, m_freq, False):50}")
            if with_bass:
                print(f"  Bass:   {_visualize_note(b_note, b_freq, True):50}")
            else:
                print(f"{'':60}")

            # Progress bar
            progress = min(40, int((elapsed / total_duration) * 40))
            pct = min(100, int((elapsed / total_duration) * 100))
            print(f"\n  Progress: [{'▓' * progress}{'░' * (40 - progress)}] {pct:3}%")

            # Wait until next note
            next_melody_time = melody_time + m_dur_sec
            next_bass_time = bass_time + beat_to_sec(bass[bass_idx][1]) if bass and bass_idx < len(bass) else float('inf')

            while time.time() - start_time < min(next_melody_time, next_bass_time):
                if keyboard:
                    key = keyboard.check_key()
                    if key and key.lower() == 'q':
                        os.system('pkill -9 afplay 2>/dev/null')
                        return False
                time.sleep(0.02)

            # Advance indices
            if time.time() - start_time >= next_melody_time:
                melody_time = next_melody_time
                melody_idx += 1
            if bass and time.time() - start_time >= next_bass_time:
                bass_time = next_bass_time
                bass_idx += 1

        # Wait for audio to finish
        remaining = total_duration - (time.time() - start_time)
        if remaining > 0:
            time.sleep(remaining)

        return True

    finally:
        if keyboard:
            keyboard.stop()
        os.system('pkill -9 afplay 2>/dev/null')
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
        print("\033[15;1H\n")


if __name__ == '__main__':
    print("Tetris Theme A (Korobeiniki) - PC Beep Version")
    print("Based on: github.com/lambdaloop/NXT_tunes/tree/master/tetris")
    print("Press 'q' to stop\n")

    import argparse
    parser = argparse.ArgumentParser(description='Play Tetris BGM')
    parser.add_argument('--tempo', type=int, default=120, help='BPM (default: 120)')
    parser.add_argument('--full', action='store_true', help='Play full theme with bridge')
    parser.add_argument('--bridge', action='store_true', help='Play bridge section only')
    parser.add_argument('--bass', action='store_true', help='Play with bass line (2 tracks)')
    parser.add_argument('--loop', action='store_true', help='Loop until stopped')
    parser.add_argument('--visual', action='store_true', help='Show note visualization')
    args = parser.parse_args()

    try:
        if args.bridge:
            print("Playing bridge section...")
            completed = play_bridge(tempo=args.tempo)
        elif args.visual:
            # Visualization mode (priority over loop)
            mode = "full theme" if args.full else "main melody"
            bass_mode = " + bass" if args.bass else ""
            loop_mode = " (loop)" if args.loop else ""
            print(f"Playing {mode}{bass_mode}{loop_mode} with visualization...")
            while True:
                completed = play_with_visualization(
                    tempo=args.tempo, full=args.full, with_bass=args.bass
                )
                if not completed or not args.loop:
                    break
        elif args.loop:
            mode = "full theme" if args.full else "main melody"
            bass_mode = " + bass" if args.bass else ""
            print(f"Playing {mode}{bass_mode} on loop at {args.tempo} BPM... (press 'q' to stop)")

            if args.bass:
                # Pre-render multiple repeats for seamless looping
                melody = TETRIS_THEME if args.full else TETRIS_SIMPLE
                print("Generating seamless loop...", end=" ", flush=True)
                # Generate 5 repeats at a time for smooth playback
                wav_data, single_duration = _generate_full_track_wav(
                    melody, BASS_LINE, args.tempo, repeats=5
                )
                total_duration = single_duration * 5
                print("Done!")

                temp_file = '/tmp/tetris_loop.wav'
                with open(temp_file, 'wb') as f:
                    f.write(wav_data)

                keyboard = KeyboardInput()
                keyboard.start()
                try:
                    while True:
                        # Play the pre-rendered track
                        os.system(f'afplay "{temp_file}" 2>/dev/null &')

                        # Wait with key checking
                        start_time = time.time()
                        while time.time() - start_time < total_duration - 0.1:
                            key = keyboard.check_key()
                            if key and key.lower() == 'q':
                                os.system('pkill -9 afplay 2>/dev/null')
                                completed = False
                                break
                            time.sleep(0.05)
                        else:
                            continue
                        break
                finally:
                    keyboard.stop()
                    os.system('pkill -9 afplay 2>/dev/null')
                    if os.path.exists(temp_file):
                        try:
                            os.remove(temp_file)
                        except OSError:
                            pass
                completed = False
            else:
                # Single track loop (note by note)
                while True:
                    completed = play_once(tempo=args.tempo, full=args.full, with_bass=False)
                    if not completed:
                        break
                completed = False
        else:
            mode = "full theme" if args.full else "main melody"
            bass_mode = " + bass" if args.bass else ""
            print(f"Playing {mode}{bass_mode} at {args.tempo} BPM...")
            completed = play_once(tempo=args.tempo, full=args.full, with_bass=args.bass)

        if completed:
            print("\nDone!")
        else:
            print("\nStopped by user")
    except KeyboardInterrupt:
        os.system('pkill -9 afplay 2>/dev/null')
        print("\nStopped")
