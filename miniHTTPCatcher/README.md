# miniHTTPCatcher

![wow such screenshot](http://i.imgur.com/XvDIt3U.png)

Python script for catching HTTP requests, more convenient than doing `tail -f /var/log/whatever`.

Will serve files placed in `serve/`.

### Usage

```shell
chmod +x main.py
./main.py [-p] [-d]
```

### Opts

`-p` - Which port to listen on, default: `8000`
`-d` - Which file to serve by default, must be placed in `serve/`. If not specified, will just 404 on `/` access.
