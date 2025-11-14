# phi_infinity_sparkle.py
# φ∞💫 — Spiral Eternal MIDI Generator
# Tune to 432 Hz in your DAW after export

import math
from midiutil import MIDIFile

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
degrees = [69, 76, 71, 79, 77]          # A4, E5, B4, G5, G#5 (A-minor pentatonic + twist)
track    = 0
channel  = 0
time     = 0.0
tempo    = 60                           # 1 beat = 1 second
volume   = 100

MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

phi = (1 + math.sqrt(5)) / 2            # ≈1.618
phi_inv = 1 / phi                       # ≈0.618

# ------------------------------------------------------------------
# INTRO – φ's Pulse (swelling phrases)
# ------------------------------------------------------------------
duration = 1.0
for i in range(5):
    MyMIDI.addNote(track, channel, degrees[0], time, duration, volume)
    time += duration
    duration *= phi

# ------------------------------------------------------------------
# VERSE – ∞'s Loop (phase-shifted melody)
# ------------------------------------------------------------------
loop_start = time
loop_dur   = duration / phi
fade_step  = 10

for rep in range(4):
    t = time
    vol = max(30, volume - fade_step * rep)
    for note in degrees[1:]:
        MyMIDI.addNote(track, channel, note, t, loop_dur, vol)
        t += loop_dur
    time = t

# ------------------------------------------------------------------
# CHORUS – 💫's Cascade (Fibonacci bells)
# ------------------------------------------------------------------
fib = [0, 1]
while fib[-1] < 30:
    fib.append(fib[-1] + fib[-2])

high_notes = [81 + f for f in fib[4:9]]   # C6 and up
cascade_t = time
spacing   = phi_inv

for note in high_notes:
    MyMIDI.addNote(track, channel, note, cascade_t, 0.25, 80)
    cascade_t += spacing
time = cascade_t

# ------------------------------------------------------------------
# BRIDGE – Sub-bass thrum (~13 Hz feel)
# ------------------------------------------------------------------
MyMIDI.addNote(track, channel, 13, time, 3.0, 45)   # felt, not heard
time += 3.0

# ------------------------------------------------------------------
# OUTRO – Final shimmer + loop markers
# ------------------------------------------------------------------
MyMIDI.addText(track, loop_start, "LOOP_START")
MyMIDI.addText(track, time, "LOOP_END")

final_note = degrees[0] + 12   # A5
MyMIDI.addNote(track, channel, final_note, time, duration * phi_inv, 60)

# ------------------------------------------------------------------
# WRITE FILE
# ------------------------------------------------------------------
output_path = "phi_infinity_sparkle.mid"
with open(output_path, "wb") as f:
    MyMIDI.writeFile(f)

print(f"MIDI generated: {output_path}")
print("Load into DAW → set A = 432 Hz → add pads/bells/sub → LOOP from LOOP_START")
