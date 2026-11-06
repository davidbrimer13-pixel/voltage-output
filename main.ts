//  Microsoft MakeCode Python (not BBC MicroPython).
//  Connect the circuit to P0 and P1, with GND as the return.
//  These pins output a 0–3.3 V square wave.
let speed = 1
let running = false
function update_outputs() {
    let period_us: number;
    if (running) {
        //  Faster range: speed 1 = 2 ms period (500 Hz),
        //  speed 9 = 200 us period (5 kHz).
        period_us = 2000 - (speed - 1) * 225
        pins.analogSetPeriod(AnalogPin.P0, period_us)
        pins.analogSetPeriod(AnalogPin.P1, period_us)
        //  512 of 1023 is approximately 50% duty cycle.
        pins.analogWritePin(AnalogPin.P0, 512)
        pins.analogWritePin(AnalogPin.P1, 512)
    } else {
        pins.analogWritePin(AnalogPin.P0, 0)
        pins.analogWritePin(AnalogPin.P1, 0)
    }
    
}

pins.analogWritePin(AnalogPin.P0, 0)
pins.analogWritePin(AnalogPin.P1, 0)
basic.showNumber(speed)
input.onButtonPressed(Button.A, function on_button_a_pressed() {
    
    //  Ignore individual button events when A+B is being used as a chord.
    if (!input.buttonIsPressed(Button.AB)) {
        speed = Math.max(1, speed - 1)
        basic.showNumber(speed)
        update_outputs()
    }
    
})
input.onButtonPressed(Button.B, function on_button_b_pressed() {
    
    if (!input.buttonIsPressed(Button.AB)) {
        speed = Math.min(9, speed + 1)
        basic.showNumber(speed)
        update_outputs()
    }
    
})
input.onButtonPressed(Button.AB, function on_button_ab_pressed() {
    
    running = !running
    update_outputs()
    if (running) {
        basic.showNumber(speed)
    } else {
        basic.clearScreen()
    }
    
})
