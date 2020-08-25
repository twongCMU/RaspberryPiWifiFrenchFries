# RaspberryPiWifiFrenchFries
LED status bars for a Raspberry Pi OpenWRT router

![Code in action](/img/animated.gif)

## Hardware:
  * Raspberry Pi 4B
  * Some kind of LED display
    * https://shop.pimoroni.com/products/unicorn-hat
    * https://www.waveshare.com/product/raspberry-pi/hats/rgb-led-hat.htm

## Difficulties
Getting Raspaberry Pi things to work right on OpenWRT instead of Raspbian was quite difficult. Here's some problems I encountered

  * OpenWRT stable releases don't support Raspberry Pi 4B yet. I had to install using a snapshot build
  * Installing the unicornhat Python3 module would fail on the compile. The problem is that openWRT's version of gcc is too old so pip would try to compile using command line switches that didn't exist. I was unable to get a newer version of gcc compiled inside openWRT
  * I tried to use Docker but there was a bug in the snapshot kernel where Docker wouldn't run
    * https://github.com/openwrt/packages/issues/13052
  * I copied an Ubuntu tree and used chroot to compile a new gcc for openWRT but that failed. Ubuntu uses glibc and OpenWRT uses musl libc so that was never going to work, but I didn't know that at the time. It took something like 2 hours for the Pi to compile gcc
  * I built the Python modules in a wheel in the Ubuntu chroot for use in OpenWRT but that also failed, probably because of the glibc/musl difference. The compile made a .so file in the wheel and Python on OpenWRT would just ignore it
  
## Solution
I finally got this to work after 3 days. Here are some steps. I'm not going to go into too much detail since it's such a mess and hopefully we get support for some of this in a full working release

  * Compile a OpenWRT snapshot from scratch. In particular, we need to enable CONFIG_KERNEL_DEVKMEM=y and CONFIG_KERNEL_DEVMEM=y
  * Install and boot OpenWRT on your Pi and configure it as your router
  * Copy all of the / directory from an Ubuntu install image to your Pi's storage
  * From the host system, mount /dev, /proc, and /sys into the chroot system:
    * mount --bind /proc /home/chroot/proc/
    * mount --bind /sys /home/chroot/sys
    * mount --bind /dev /home/chroot/dev
  * Chroot into the chroot system
  * install everything you need to run the Python code here. It should interface correctly with the LED display now
    * python3-venv python3-dev python3-wheel python-wheel-common libffi-dev make gcc
