# MyrtDesk API

Library for controlling smart table functions with my own [firmware](https://github.com/mishamyrt/myrt_desk_firmware).

* **Fully asynchronous**
* Automatic detection
* Cool CLI tool

## API Example
This code will wait for the lights to turn off, then flash the backlight controller and then turn on the rainbow effect:

```py
from myrt_desk_api import MyrtDesk, Effect
from asyncio import run

async def main():
    desk_host = await discover()
    desk = MyrtDesk(desk_host)
    await desk.backlight.set_power(False)
    with open(args.path, mode="rb") as file:
        await desk.system.update_firmware(file.read())
    await desk.backlight.set_effect(Effect.RAINBOW)

if __name__ == '__main__':
    run(main())
```