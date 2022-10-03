# RaspberryPiWifiFrenchFries
LED status bars for a Raspberry Pi OpenWRT router

![Code in action](/img/animated2.gif)

## Hardware:
  * Raspberry Pi 4 Compute Module (Wifi, 8GB RAM, 16GB storage)
  * 52Pi Router Board https://wiki.52pi.com/index.php/EP-0146
  * Unicorn Hat Mini https://shop.pimoroni.com/products/unicorn-hat-mini?variant=31657688498259

## Pros:
  * Dual ethernet, no USB Ethernet dongle required. On a Pi4, I had to replug the USB Ethernet dongle every few days
  * Pi4 is now supported by OpenWRT, which it wasn't in 2020 when I built the first version of this
  * Large heatsink and thermal pads included in 52Pi Router Board package
  * Onboard Wifi is stable, which it wasn't in 2020 on the beta OpenWRT. It only seems to do 2.4ghz wifi but that's fine for my needs (my desktop is plugged into the ethernet, and my phones use wifi)
  * The eMMC storage on the Pi CM4 is supposedly better than an SD card

## Cons:
 * Getting OpenWRT installed was a huge pain and I had to recompile the OpenWRT image many times
 * As of mid 2022, getting a Pi CM4 is really difficult. I got one with 8GB of ram but 1GB is enough for everything I'm running and the 8GB model costs much more