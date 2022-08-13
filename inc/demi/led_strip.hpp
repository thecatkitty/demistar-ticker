#pragma once

#include <memory>

#include <demi/periodic_task.hpp>
#include <demi/ws2812.hpp>

class led_strip : public IPeriodicTask
{
    ws2812 &_ctl;

    const unsigned               _length;
    std::unique_ptr<color_rgb[]> _frame;
    bool                         _is_modified;

  public:
    class pixel_reference
    {
        led_strip &_strip;
        unsigned   _index;

      public:
        pixel_reference(led_strip &strip, unsigned index)
            : _strip{strip}, _index{index}
        {
        }

        inline pixel_reference &
        operator=(color_rgb rgb)
        {
            _strip._frame[_index] = rgb;
            _strip._is_modified = true;
            return *this;
        }

        inline operator color_rgb() const
        {
            return _strip._frame[_index];
        }
    };

    inline led_strip(ws2812 &ctl, unsigned length)
        : _ctl{ctl}, _length{length},
          _frame{std::make_unique<color_rgb[]>(length)}, _is_modified{false}
    {
    }

    inline pixel_reference
    operator[](unsigned pixel)
    {
        return pixel_reference{*this, pixel};
    }

    virtual void
    handle() override
    {
        if (!_is_modified)
        {
            return;
        }

        _is_modified = false;
        for (unsigned pixel = 0; pixel < _length; ++pixel)
        {
            _ctl.put_pixel(_frame[pixel]);
        }
    }
};
