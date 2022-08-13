#pragma once

#include <demi/color.hpp>
#include <demi/pio.hpp>

class ws2812
{
    static const int _cycles_per_bit = 10;
    static const int _wrap_target = 0;
    static const int _wrap = 3;

    static const struct pio_program _program;

    pio::state_machine _sm;

  public:
    ws2812(pio::state_machine sm) : _sm{sm}
    {
    }

    inline void
    initialize(uint pin, float freq, bool rgbw)
    {
        uint offset = _sm.get_pio().add_program(&_program);

        _sm.get_pio().gpio_init(pin);
        _sm.set_consecutive_pindirs(pin, 1, true);

        pio::sm_config config;
        config.set_sideset_pins(pin)
            .set_out_shift(false, true, rgbw ? 32 : 24)
            .set_fifo_join(PIO_FIFO_JOIN_TX)
            .set_clkdiv(clock_get_hz(clk_sys) / (freq * _cycles_per_bit))
            .set_wrap(offset + _wrap_target, offset + _wrap)
            .set_sideset(1, false, false);

        _sm.initialize(offset, config);
        _sm.set_enabled(true);
    }

    inline void
    put_pixel(uint32_t grb)
    {
        _sm.put_blocking(grb << 8u);
    }

    inline void
    put_pixel(color_rgb rgb)
    {
        put_pixel(((uint32_t)(rgb.r) << 8) | ((uint32_t)(rgb.g) << 16) |
                  (uint32_t)(rgb.b));
    }
};
