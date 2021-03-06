# Voice recognition server

We use Google Cloud Speech API to recognize audio files. <br>
Send a `POST` request to recognize your audio file.

### POST request
`URL`: https://vrp.eu.ngrok.io/recognize <br>
`Content-Type`: application/json

Fields:
* `url` - url to ogg file
* `user_id` - user's vk id (optional field)

### Server config structure
```
{
  "host": <host>,
  "port": <port>
}
```

### PostgreSQL config structure
```
{
  "host": <host>,
  "database": <database name>,
  "user": <user>,
  "password": <password>
}
```

### Yandex SpeechKit config structure
[Documentation](https://tech.yandex.com/speechkit/cloud/doc/guide/concepts/asr-overview-technology-docpage/)
```
{
  "api_key": <api_key>
}
```

### Related projects
* [Voice recognition bot](https://github.com/Rebryk/VRP-Bot)
* [Voice recognition extension for Chrome](https://github.com/Rebryk/VRP-Chrome-Extension/)
