#include <demi/ws2812.hpp>

static const uint16_t ws2812_program_instructions[] = {
    //          .wrap_target
    0x6221, //  0: out    x, 1            side 0 [2]
    0x1123, //  1: jmp    !x, 3           side 1 [1]
    0x1400, //  2: jmp    0               side 1 [4]
    0xa442, //  3: nop                    side 0 [4]
            //  .wrap
};

const struct pio_program ws2812::_program = {
    .instructions = ws2812_program_instructions,
    .length = sizeof(ws2812_program_instructions) /
              sizeof(ws2812_program_instructions[0]),
    .origin = -1,
};
