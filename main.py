# Microsoft MakeCode Python (not BBC MicroPython)
# Connect the circuit to P0 and P1, with GND as the return.
# This is an original, upbeat Buddy Holly-style pop riff.

speed = 5
playing = False
step = 0

# Original riff: catchy, simple, and bright.
# Each note is (frequency_hz, duration_ms)
riff = [
    (440, 170), (440, 170), (494, 170), (554, 170),
    (494, 170), (440, 170), (392, 170), (392, 170),
    (440, 170), (440, 170), (494, 170), (554, 170),
    (494, 170), (440, 170), (392, 170), (330, 250),

    (392, 170), (392, 170), (440, 170), (494, 170),
    (554, 170), (494, 170), (440, 170), (392, 170),
    (440, 170), (440, 170), (494, 170), (554, 170),
    (494, 170), (440, 170), (392, 170), (330, 250),

    (440, 170), (494, 170), (554, 170), (494, 170),
    (440, 170), (392, 170), (440, 170), (392, 170),
    (330, 170), (392, 170), (440, 170), (494, 170),
    (440, 170), (392, 170), (330, 170), (294, 300)
]


def stop_outputs():
    pins.analog_write_pin(AnalogPin.P0, 0)
    pins.analog_write_pin(AnalogPin.P1, 0)


def set_tone(freq):
    if freq <= 0:
        stop_outputs()
        return
    period_us = 1000000 // freq
    pins.analog_set_period(AnalogPin.P0, period_us)
    pins.analog_set_period(AnalogPin.P1, period_us)
    pins.analog_write_pin(AnalogPin.P0, 512)
    pins.analog_write_pin(AnalogPin.P1, 512)


def play_one_note():
    global step, playing
    if not playing:
        return
    if step >= len(riff):
        playing = False
        step = 0
        stop_outputs()
        basic.clear_screen()
        return

    freq, ms = riff[step]
    tempo_scale = 1.0 + ((speed - 5) * 0.09)
    note_time = max(60, int(ms / tempo_scale))

    set_tone(freq)
    basic.pause(note_time)
    stop_outputs()
    basic.pause(20)
    step += 1


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
    global playing, step
    playing = not playing
    if playing:
        step = 0
        basic.show_number(speed)
    else:
        stop_outputs()
        basic.clear_screen()


def on_forever():
    if playing:
        play_one_note()
    else:
        basic.pause(10)


stop_outputs()
basic.show_number(speed)
input.on_button_pressed(Button.A, on_button_a_pressed)
input.on_button_pressed(Button.B, on_button_b_pressed)
input.on_button_pressed(Button.AB, on_button_ab_pressed)
basic.forever(on_forever)
