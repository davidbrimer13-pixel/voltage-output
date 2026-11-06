# Microsoft MakeCode Python (not BBC MicroPython).
# Connect the circuit to P0 and P1, with GND as the return.
# These pins output a 0–3.3 V square wave.

speed = 5
playing = False
sequence_index = 0

# More precise approximation of the "Lost Woods" melody.
# Each entry is: (frequency_hz, duration_ms)
melody = [
    (392, 200), (392, 200), (494, 200), (494, 200), (523, 300), (494, 200), (440, 200), (392, 300),
    (330, 200), (330, 200), (392, 200), (440, 200), (494, 300), (440, 200), (392, 200), (330, 300),
    (392, 200), (440, 200), (494, 200), (523, 200), (494, 200), (440, 200), (392, 300), (440, 200),
    (494, 200), (523, 200), (587, 300), (523, 200), (494, 200), (440, 200), (392, 400)
]


def stop_outputs():
    pins.analog_write_pin(AnalogPin.P0, 0)
    pins.analog_write_pin(AnalogPin.P1, 0)


def set_tone(freq):
    if freq <= 0:
        stop_outputs()
        return
    # Convert note frequency to PWM period for a square wave tone.
    period_us = 1000000 // freq
    pins.analog_set_period(AnalogPin.P0, period_us)
    pins.analog_set_period(AnalogPin.P1, period_us)
    pins.analog_write_pin(AnalogPin.P0, 512)
    pins.analog_write_pin(AnalogPin.P1, 512)


def play_melody_once():
    global sequence_index, playing
    if not playing:
        return
    if sequence_index >= len(melody):
        playing = False
        sequence_index = 0
        stop_outputs()
        basic.clear_screen()
        return

    freq, ms = melody[sequence_index]
    # Speed sets the tempo scale: lower = slower, higher = faster.
    tempo = 1.0 + ((speed - 5) * 0.09)
    note_time = max(60, int(ms / tempo))

    set_tone(freq)
    basic.pause(note_time)
    stop_outputs()
    basic.pause(25)
    sequence_index += 1


def on_button_a_pressed():
    global speed
    if not input.button_is_pressed(Button.AB):
        speed = max(1, speed - 1)
        basic.show_number(speed)


def on_button_b_pressed():
    global speed
    if not input.button_is_pressed(Button.AB):
        speed = min(9, speed + 1)
        basic.show_number(speed)


def on_button_ab_pressed():
    global playing, sequence_index
    playing = not playing
    if playing:
        sequence_index = 0
        basic.show_number(speed)
    else:
        stop_outputs()
        basic.clear_screen()


def on_forever():
    if playing:
        play_melody_once()
    else:
        basic.pause(15)


stop_outputs()
basic.show_number(speed)
input.on_button_pressed(Button.A, on_button_a_pressed)
input.on_button_pressed(Button.B, on_button_b_pressed)
input.on_button_pressed(Button.AB, on_button_ab_pressed)
basic.forever(on_forever)
