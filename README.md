# RaspberryPiWifiFrenchFries
LED status bars for a Raspberry Pi OpenWRT router. Red bars on the right are download usage, green bars in the center are uploads, and the blue bar on the left is CPU clock speed. The OLED display shows the CPU clock speed, CPU temperature, and total data downloaded since boot.

![Code in action](/img/animated2.gif)

## Hardware:
  * Raspberry Pi 4 Compute Module (Wifi, 8GB RAM, 16GB storage)
  * 52Pi Router Board https://wiki.52pi.com/index.php/EP-0146
  * Unicorn Hat Mini https://shop.pimoroni.com/products/unicorn-hat-mini?variant=31657688498259
  * PiShop UPS Hat https://www.pishop.us/product/raspberry-pi-ups-hat/
  * Some LEGO to hold it all up

## Pros:
  * Dual ethernet, no USB Ethernet dongle required. On a Pi4 Model B, I had to replug the USB Ethernet dongle every few days
  * Pi4 platform is now supported by OpenWRT, which it wasn't in 2020 when I built the first version of this
  * Large heatsink and thermal pads included in 52Pi Router Board package
  * Onboard Wifi is stable, which it wasn't in 2020 on the beta OpenWRT. It only seems to do 2.4ghz wifi but that's fine for my needs (my desktop is plugged into the ethernet, and my phones use wifi)
  * The eMMC storage on the Pi Compute Module 4 is supposedly better than an SD card

## Cons:
 * Getting OpenWRT installed was a huge pain and I had to recompile the OpenWRT image many times
 * As of mid 2022, buying a Pi Compute Module 4 is really difficult as they are out of stock everywhere