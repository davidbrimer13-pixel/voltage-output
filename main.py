# Microsoft MakeCode Python (not BBC MicroPython).
# Connect the circuit to P0 and P1, with GND as the return.
# These pins output a 0–3.3 V square wave.

speed = 1
running = False


def update_outputs():
    if running:
        # Faster range: speed 1 = 2 ms period (500 Hz),
        # speed 9 = 200 us period (5 kHz).
        period_us = 2000 - ((speed - 1) * 225)
        pins.analog_set_period(AnalogPin.P0, period_us)
        pins.analog_set_period(AnalogPin.P1, period_us)
        # 512 of 1023 is approximately 50% duty cycle.
        pins.analog_write_pin(AnalogPin.P0, 512)
        pins.analog_write_pin(AnalogPin.P1, 512)
    else:
        pins.analog_write_pin(AnalogPin.P0, 0)
        pins.analog_write_pin(AnalogPin.P1, 0)


def on_button_a_pressed():
    global speed
    # Ignore individual button events when A+B is being used as a chord.
    if not input.button_is_pressed(Button.AB):
        speed = max(1, speed - 1)
        basic.show_number(speed)
        update_outputs()


def on_button_b_pressed():
    global speed
    if not input.button_is_pressed(Button.AB):
        speed = min(9, speed + 1)
        basic.show_number(speed)
        update_outputs()


def on_button_ab_pressed():
    global running
    running = not running
    update_outputs()
    if running:
        basic.show_number(speed)
    else:
        basic.clear_screen()


pins.analog_write_pin(AnalogPin.P0, 0)
pins.analog_write_pin(AnalogPin.P1, 0)
basic.show_number(speed)
input.on_button_pressed(Button.A, on_button_a_pressed)
input.on_button_pressed(Button.B, on_button_b_pressed)
input.on_button_pressed(Button.AB, on_button_ab_pressed)
