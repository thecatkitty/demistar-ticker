#pragma once

#include <hardware/clocks.h>
#include <hardware/pio.h>

namespace pio
{
class pio
{
    pio_hw_t &_hw;

  public:
    inline pio(pio_hw_t *hw) : _hw{*hw}
    {
    }

    inline void
    gpio_init(uint pin)
    {
        pio_gpio_init(&_hw, pin);
    }

    inline uint
    add_program(const pio_program_t *program)
    {
        return pio_add_program(&_hw, program);
    }

    operator pio_hw_t *() const
    {
        return &_hw;
    }
};

class sm_config
{
    pio_sm_config _config;

  public:
    inline sm_config() : _config{pio_get_default_sm_config()}
    {
    }

    inline sm_config &
    set_sideset_pins(uint sideset_base)
    {
        sm_config_set_sideset_pins(&_config, sideset_base);
        return *this;
    }

    inline sm_config &
    set_sideset(uint bit_count, bool optional, bool pindirs)
    {
        sm_config_set_sideset(&_config, bit_count, optional, pindirs);
        return *this;
    }

    inline sm_config &
    set_clkdiv(float div)
    {
        uint16_t div_int;
        uint8_t  div_frac;
        pio_calculate_clkdiv_from_float(div, &div_int, &div_frac);
        sm_config_set_clkdiv_int_frac(&_config, div_int, div_frac);
        return *this;
    }

    inline sm_config &
    set_wrap(uint wrap_target, uint wrap)
    {
        sm_config_set_wrap(&_config, wrap_target, wrap);
        return *this;
    }

    inline sm_config &
    set_out_shift(bool shift_right, bool autopull, uint pull_threshold)
    {
        sm_config_set_out_shift(&_config, shift_right, autopull,
                                pull_threshold);
        return *this;
    }

    inline sm_config &
    set_fifo_join(enum pio_fifo_join join)
    {
        sm_config_set_fifo_join(&_config, join);
        return *this;
    }

    operator const pio_sm_config *() const
    {
        return &_config;
    }
};

class state_machine
{
    pio  _pio;
    uint _index;

  public:
    inline state_machine(pio pio, uint index) : _pio{pio}, _index{index}
    {
    }

    inline void
    initialize(uint initial_pc, const sm_config &config)
    {
        pio_sm_init(_pio, _index, initial_pc, config);
    }

    inline void
    set_enabled(bool enabled)
    {
        pio_sm_set_enabled(_pio, _index, enabled);
    }

    inline void
    set_consecutive_pindirs(uint pin_base, uint pin_count, bool is_out)
    {
        pio_sm_set_consecutive_pindirs(_pio, _index, pin_base, pin_count,
                                       is_out);
    }

    inline void
    put_blocking(uint32_t data)
    {
        pio_sm_put_blocking(_pio, _index, data);
    }

    inline pio &
    get_pio()
    {
        return _pio;
    }
};
} // namespace pio
