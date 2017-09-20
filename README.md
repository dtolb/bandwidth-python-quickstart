# bandwidth-python-quickstart
Simple Quickstart for Bandwidth and Python 3 using Flask

## Pre-reqs

* [Bandwidth Account](http://dev.bandwidth.com)
* `userId`, `token`, & `secret` set as environment variables
* [ngrok](https://ngrok.com/) Installed with account

## Deploying Locally with ngrok

[Ngrok](https://ngrok.com) is an awesome tool that lets you open up local ports to the internet.

![Ngrok how](https://s3.amazonaws.com/bw-demo/ngrok_how.png)

Once you have ngrok installed, open a new terminal tab and navigate to it's location on the file system and run:

```bash
./ngrok http 5000
```

You'll see the terminal show you information

![ngrok terminal](https://s3.amazonaws.com/bw-demo/ngrok_terminal.png)

