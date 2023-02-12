# Demistar API

## Endpoints

### Display effects
| Method    | URL                       | Request           | Response          | Description
|-----------|---------------------------|-------------------|-------------------|-------------------
| `GET`     | /effects                  | -                 | Effects           | Get supported effects

### Local time settings
| Method    | URL                       | Request           | Response          | Description
|-----------|---------------------------|-------------------|-------------------|-------------------
| `GET`     | /wallclock                | -                 | WallclockSettings | Get device local time
| `POST`    | /wallclock                | WallclockSettings | `{}`              | Set device local time

### Timeline programming
| Method    | URL                       | Request           | Response          | Description
|-----------|---------------------------|-------------------|-------------------|-------------------
| `GET`     | /timeline                 | -                 | Timeline          | Get all timeline items
| `POST`    | /timeline                 | TimelineItem      | IdResponse        | Add a new timeline item
| `DELETE`  | /timeline                 | -                 | CountResponse     | Empty the timeline
| `DELETE`  | /timeline/`{itemid}`      | -                 | TimelineItem      | Remove an item from the timeline

## Types

### CountResponse (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| count         | int                   | Number of processed items

### DateTime (str)
`{year}-{month:02}-{day:02}T{hour:02}:{minute:02}:{second:02}`
| Part          | Description
|---------------|-------------------------------------------
| year          | Year
| month         | Month (01-12)
| day           | Day (01-31)
| hour          | Hour (00-23)
| minute        | Minute (00-59)
| second        | Second (00-59)

### Effects (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| display       | str[]                 | List of supported text display effects
| ring          | str[]                 | List of supported ring effects

### IdResponse (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| id            | int                   | Item unique identifier

### ManualStage (Stage)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| *name*        | str                   | *manual*
| top           | str                   | Top text
| bottom        | str                   | Bottom text
| inner         | RingAnimation         | **Ticker:** Inner ring animation; **Hub:** Background
| outer         | RingAnimation         | **Ticker:** Outer ring animation; **Hub:** Foreground

### MeetingStage (Stage)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| *name*        | str                   | *meeting*
| title         | str                   | Title of the meeting
| host          | str                   | Host of the meeting

### RingAnimation (obj[])
`[ "blink", r:int, g:int, b:int, interval_ms:int ]` - cyclic switching between a selected color (RGB channels 0-255) and the default one, every `interval_ms` milliseconds

`[ "breath", r:int, g:int, b:int, cycle_ms:int ]` - cyclic smooth transition between a selected color (RGB channels 0-255) and the default one, over `cycle_ms` milliseconds

`[ "color", r:int, g:int, b:int ]` - static color (RGB channels 0-255)

### Stage (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| name          | str                   | Name of the stage type (*manual*, *meeting* or *wallclock*)

### Timeline (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| backlog       | TimelineItem[]        | List of all incoming items
| cycle         | TimelineItem[]        | List of all items within the current cycle; **Hub:** Empty

### TimelineItem (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| id            | int                   | Timeline item unique identifier
| room          | int \| null           | Room identifier; **Ticker:** Ignored
| start         | DateTime              | Date and time of the begin
| duration      | int                   | Total duration in seconds
| screentime    | int                   | Number of seconds reserved for an item within one display cycle; **Hub:** Ignored
| stage         | Stage                 | Stage definition

### WallclockStage (Stage)
**Hub:** Ignored
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| *name*        | str                   | *wallclock*

### WallclockSettings (dict)
| Member        | Type                  | Description
|---------------|-----------------------|---------------------------------------
| time          | DateTime              | Date and time info
