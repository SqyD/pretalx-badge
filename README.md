# pretalx-badge
Exports a conference schedule in easy to parse json files, targeted at embedded systems such as the badges by badge.team

While started as using the cookie cutter template for export plugins, it's now basically a collection of views that output 3 variants of json formatted schedule data:

### Base
URL scheme: https://<hostname>/<event-slug>/schedule/badge/base.json
URL example: https://amazingevent.com/ae24/schedule/badge/base.json
A single URL per event that holds all the general event information such as it's name, dates and room information.

### Room schedule
URL scheme: https://<hostname>/<event-slug>/schedule/badge/room<room_id>_day<day>.json
URL example: https://amazingevent.com/ae24/schedule/badge/room2day1.json
A unique URL for each day of each conference room. Holds just times and titles of talks.

### Talk details
URL scheme: https://<hostname>/<event-slug>/schedule/badge/talk<talk_id>.json
URL example: https://amazingevent.com/ae24/schedule/badge/talk42.json
A URL for each talk that hold a lot of, but not all, known information about each talk.

## Example implementation
You can find a rough implementation for the badger2040w badges by Pimoroni and possibly some previous Badge Team badges at https://github.com/SqyD/upretalx

# Word of caution
Note that at this stage I would not (yet) recommend any of this software for the less brave users of either Pretalx or any of the badges. I hope to polish it (a lot) more in the near future. 
