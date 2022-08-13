#pragma once

struct IPeriodicTask
{
    virtual void
    handle() = 0;
};
