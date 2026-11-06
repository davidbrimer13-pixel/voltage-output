# Microsoft MakeCode Python (not BBC MicroPython).
# P0 and P1 output the melody as a 0–3.3 V square wave.
# Use a suitable speaker driver/amplifier; don't connect a speaker directly
# if it draws more current than a micro:bit pin can safely provide.

speed = 5
playing = False

# Lost Woods / Saria's Song melody, represented as note frequencies in Hz.
# F#4=370, G4=392, A4=440, B4=494, C5=523, D5=587, E5=659.
notes = [370, 440, 494, 370, 440, 494, 370, 440, 494,
         659, 587, 494, 523, 494, 392, 370, 392, 370, 587, 659, 494, 440]
note_lengths = [1, 1, 2, 1, 1, 2, 1, 1, 2,
                1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2]


def stop_outputs():
    pins.analog_write_pin(AnalogPin.P0, 0)
    pins.analog_write_pin(AnalogPin.P1, 0)


def play_note(frequency):
    if frequency <= 0:
        stop_outputs()
    else:
        period_us = 1000000 // frequency
        pins.analog_set_period(AnalogPin.P0, period_us)
        pins.analog_set_period(AnalogPin.P1, period_us)
        pins.analog_write_pin(AnalogPin.P0, 512)
        pins.analog_write_pin(AnalogPin.P1, 512)


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
    global playing
    playing = not playing
    if playing:
        basic.show_number(speed)
    else:
        stop_outputs()
        basic.clear_screen()


def on_forever():
    if playing:
        # A/B choose playback speed: 1 is slowest, 9 is fastest.
        base_duration = 420 - ((speed - 1) * 35)
        for i in range(len(notes)):
            if not playing:
                break
            play_note(notes[i])
            basic.pause(base_duration * note_lengths[i])
        stop_outputs()
    else:
        basic.pause(20)


stop_outputs()
basic.show_number(speed)
input.on_button_pressed(Button.A, on_button_a_pressed)
input.on_button_pressed(Button.B, on_button_b_pressed)
input.on_button_pressed(Button.AB, on_button_ab_pressed)
basic.forever(on_forever)
