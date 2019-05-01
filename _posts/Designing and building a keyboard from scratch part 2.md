
# The innards of a keyboard

Conceptually a keyboard is a collection of 100 or so individual switches all connected to a circuit continuously detects their state and report it via messages sent to the computer. You press a key, a message is sent with the key's numeric code and the fact it was pressed. You release the key, another message is sent. 

Nowadays the common way to transfer these messages is through USB.

Generating USB messages with a custom built circuit is not trivial. The smart way to do it is to use a microcontroller that can natively speak USB. A chip that contains a CPU, RAM and ROM and can be programmed to continuously "read" the switches state and send these messages via the USB interface when it sees a change.

Most non commercial mechanical keyboards use one of the following microcontrollers:
 - Atmega32u4
 - Teensy
 - Stm32
 
The atmega32u4 is the heart of, for example, the Arduino Leonardo and the Arduino pro micro. Being open source, there are really cheap versions of these boards available in the usual chinese websites. The Pro micro was my choice as it is small enough I can fit it under the keyboard PCB. 

![Pro Micro](images/promicro.jpg)

This little guy has 2KB of RAM, 1KB of EEPROM and runs plenty fast for this application. 

That 1KB of EEPROM is significant because it limits the total memory for dynamic macros to about 500 characters across all 12 macro keys. More on this below.

## The matrix

The atmega32u4 has about 20 general purpose IO pins. It isn't easy to find a microcontroller with enough IO pins so that you can connect 1 switch to 1 pin. 

So the switches need to be multiplexed somehow. The usual way to this is quite interesting: we create a matrix of wires with N rows and M columns. We connect all the switches of a row together, thus creating N rows which go directly to N pins in the microcontroller.

The other end of the switches which belong to the same vertical column are also connected together. This creates M vertical wires. 

Here's a nice diagram taken from a [fantastic blog post](http://blog.komar.be/how-to-make-a-keyboard-the-matrix/) on everything you need to know about keyboard matrices:

![Matrix](images/matrix.png)



In small keyboards we can connect these M wires directly to the microcontroller, as long as the microcontroller has at least N+M free IO pins. At each switch we also connect a diode that goes from the switch to the sensing wire. This is so we don't have issues when multiple keys are pressed at the same time. There's a really nice post that explains better why we need the diodes:

To detect which key is pressed we do the following:
 - Set all the pins connected to columns as outputs and initialize them to a high value.
 - Set all pins connected to rows as input with pull-ups (meaning if nothing is connected to those pins they will be logically high as there are internal resistors the pull them up)

We set a single column as low.
We read the status of all the rows.

If all the rows read are high we Know nothing is pressed. On the other hand, the rows that read as low have the corresponding switches pressed. I e. For every low row we know that the switch in that row and column (that is currently low) is connected. This is because the switch electrically connects the low value of the column to the row.

We reset that column back to high and select another one to be low. Repeat this process as fast as possible cycling through the columns ( about 1000 times a second is more than enough and perfectly achievable on a small microcontroller). This is called the switch matrix scanning process. 
You can obviously swap rows and columns. I.e. select rows and read the state of the columns and in fact this is the most common way in other open source keyboards. 

Once we understand that a switch is closed we need to map that to an action or a key code to be sent. More on that below.

This keyboard has 17 columns and 7 rows. For this I couldn't connect directly the 17+7 wires to the microcontroller. Instead all columns are controlled with only 3 wires by using 3 cascaded shift registers.
The micro has therefore 7+3 IO pins used.

Firmware
There's a number of good software packages designed for keyboards. In my opinion the best one is the QMK, used by many 

For this project I decided to write my own. More interesting challenge and meant k didn't have to faff with a huge codebase that supports many use cases I don't care ( like multiple layers ).

The firmware is this an Arduino sketch and importable into the Arduino IDE.



