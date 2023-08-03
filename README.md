## Http routes

- `/:room/connect?name=<name to check>` - check if the name 
- `/:room/names`

## WS Events
```json
{
  "event": "string",
  "data": "stringified data object"
}
```
Data objects must be stringified:
```
WRONG ❌

"data": {
  "detail": "connected",
  "name": "qwe"             // only for "connected"
}
```

↓ 

```
RIGHT ✅

"data":"{\"detail\":\"connected\",\"name\":\"qwe\"}"
```

### Message
```json
{
  "event": "message",
  "data": "\"text\":\"message text goes here\"}"
}
```

### Connection
examples:
```json
{
  "event": "connection",
  "data": "{\"detail\": \"connected\", \"name\": \"qwe\"}"
}
```
```json
{
  "event": "connection",
  "data": "{\"detail\":\"disconnected\", \"name\":\"qwe\"}"
}
```
