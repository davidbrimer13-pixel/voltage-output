from microbit import *

# P0 and P1 are digital outputs. They switch between 0 V and about 3.3 V.
OUT_A = pin0
OUT_B = pin1

speed = 1
running = False
combo_latched = False

OUT_A.write_digital(0)
OUT_B.write_digital(0)
display.show(str(speed))

while True:
    both_pressed = button_a.is_pressed() and button_b.is_pressed()

    # A+B toggles output. Latch it so a long press toggles only once.
    if both_pressed:
        if not combo_latched:
            running = not running
            combo_latched = True
            if not running:
                OUT_A.write_digital(0)
                OUT_B.write_digital(0)
            display.show(str(speed) if running else Image.NO)
    else:
        combo_latched = False

        # A lowers the speed; B raises it. Keep the setting in the 1–9 range.
        if button_a.was_pressed():
            speed = max(1, speed - 1)
            display.show(str(speed))
        if button_b.was_pressed():
            speed = min(9, speed + 1)
            display.show(str(speed))

    if running:
        # Higher setting = shorter delay = faster square wave.
        # Approximate half-periods: level 1 = 5 ms, level 9 = 0.5 ms.
        half_period_us = 5000 - ((speed - 1) * 562)
        OUT_A.write_digital(1)
        OUT_B.write_digital(1)
        sleep_us(half_period_us)
        OUT_A.write_digital(0)
        OUT_B.write_digital(0)
        sleep_us(half_period_us)
    else:
        sleep(20)
