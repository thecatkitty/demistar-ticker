#pragma once

#include <cstdint>

struct color_rgb
{
    uint8_t r, g, b;

    inline constexpr color_rgb
    operator>>(unsigned n) const
    {
        return {r >> n, g >> n, b >> n};
    }
};
