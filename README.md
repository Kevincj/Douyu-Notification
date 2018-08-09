# Douyu-Notification
Send an IFTTT e-mail notification while your streamer (especially on douyu.com) starts/ends the stream.

## Dependencies

- An e-mail account linked to IFTTT
- A pair of  IFTTT triggers (#Online, #Offline) —— send an IFTTT notification to your IFTTT-linked devices once an tagged e-mail is received by 'trigger@applet.ifttt.com' from your e-mail account



## Usages

- Fill in your e-mail address, password and the room_id of the streamer in `data.json`
- Excute in Command Line: `nohup python Trigger.py &`

