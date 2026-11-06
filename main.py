from microbit import *

# Connect your circuit to P0 and P1, with GND as the return.
# These pins output a 0–3.3 V square wave (not a higher voltage).
OUT_A = pin0
OUT_B = pin1

speed = 1
running = False
combo_latched = False


def stop_outputs():
    OUT_A.write_digital(0)
    OUT_B.write_digital(0)


def start_outputs():
    # PWM gives a steady square wave without relying on Python timing loops.
    # Level 1 is about 50 Hz; level 9 is about 500 Hz.
    period_us = 10000 - ((speed - 1) * 1125)
    OUT_A.set_analog_period_microseconds(period_us)
    OUT_B.set_analog_period_microseconds(period_us)
    OUT_A.write_analog(512)  # approximately 50% duty cycle
    OUT_B.write_analog(512)


stop_outputs()
display.show(str(speed))

while True:
    # Consume button press events each pass. A+B takes precedence over A or B.
    a_pressed = button_a.was_pressed()
    b_pressed = button_b.was_pressed()
    both_pressed = button_a.is_pressed() and button_b.is_pressed()

    if both_pressed:
        if not combo_latched:
            running = not running
            combo_latched = True
            if running:
                start_outputs()
                display.show(str(speed))
            else:
                stop_outputs()
                display.show(Image.NO)
    else:
        combo_latched = False
        if a_pressed:
            speed = max(1, speed - 1)
            display.show(str(speed))
        if b_pressed:
            speed = min(9, speed + 1)
            display.show(str(speed))

        # Apply a changed speed immediately while output is running.
        if running and (a_pressed or b_pressed):
            start_outputs()

    sleep(10)
