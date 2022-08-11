#include <pico/stdlib.h>

#include <demi/ws2812.hpp>

static const int PIXELS = 32;

int
main()
{
    ws2812 ws{pio::state_machine{pio0, 0}};
    ws.initialize(11, 800000, false);

    uint32_t c = 0;
    while (1)
    {
        for (int i = 0; i < PIXELS; i++)
        {
            ws.put_pixel(c);
            c += 16;
        }
        sleep_ms(125);
    }
}
