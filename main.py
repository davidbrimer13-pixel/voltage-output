# Microsoft MakeCode Python (not BBC MicroPython)
# P0 and P1 are used as the pulse output pins, with GND as the return.
# This is a better approximation of the Lost Woods melody than the earlier version.

speed = 5
playing = False
step = 0

# Approximate "Lost Woods" / Saria's Song style melody.
# Frequencies chosen to sound closer to the original tune.
melody = [
    (392, 220), (440, 220), (494, 220), (440, 220),
    (392, 220), (440, 220), (494, 220), (440, 220),
    (392, 220), (440, 220), (494, 220), (440, 220),
    (392, 220), (330, 220), (392, 220), (440, 220),
    (494, 220), (440, 220), (392, 220), (330, 220),
    (392, 220), (440, 220), (494, 220), (523, 220),
    (494, 220), (440, 220), (392, 220), (330, 220),
    (294, 220), (330, 220), (392, 220), (440, 220),
    (494, 300), (440, 220), (392, 220), (330, 220),
    (294, 300), (330, 220), (392, 220), (440, 220),
    (494, 220), (523, 220), (494, 220), (440, 220),
    (392, 220), (330, 220), (392, 220), (440, 220),
    (494, 220), (523, 220), (587, 220), (523, 220),
    (494, 220), (440, 220), (392, 220), (330, 220),
    (392, 220), (440, 220), (494, 220), (523, 220),
    (494, 220), (440, 220), (392, 220), (330, 220),
    (294, 220), (330, 220), (392, 220), (440, 220),
    (494, 300), (440, 220), (392, 220), (330, 220),
    (294, 220), (330, 220), (392, 220), (440, 220),
    (494, 220), (523, 220), (494, 220), (440, 220),
    (392, 220), (330, 220), (294, 300)
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


def play_one_step():
    global step, playing
    if not playing:
        return
    if step >= len(melody):
        playing = False
        step = 0
        stop_outputs()
        basic.clear_screen()
        return

    freq, ms = melody[step]
    tempo_scale = 1.0 + ((speed - 5) * 0.09)
    note_time = max(70, int(ms / tempo_scale))

    set_tone(freq)
    basic.pause(note_time)
    stop_outputs()
    basic.pause(26)
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
        play_one_step()
    else:
        basic.pause(10)


stop_outputs()
basic.show_number(speed)
input.on_button_pressed(Button.A, on_button_a_pressed)
input.on_button_pressed(Button.B, on_button_b_pressed)
input.on_button_pressed(Button.AB, on_button_ab_pressed)
basic.forever(on_forever)
