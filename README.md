<div align="center">

# bandwidth-python-quickstart

<img src="https://s3.amazonaws.com/bwdemos/BW_Voice_Messaging.png"/>
Simple Quickstart for Bandwidth and Python 3 using Flask
</div>

## Pre-reqs

* [Bandwidth Account](http://dev.bandwidth.com)
* [ngrok](https://ngrok.com/) Installed with account
* [Python 3](https://www.python.org/downloads/)
* [VirtualEnv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Setup Environment Variables

| Environment Variable   | Description                                                    | Example                |
|:-----------------------|:---------------------------------------------------------------|:-----------------------|
| `BANDWIDTH_USER_ID`    | [Bandwidth user-id](http://dev.bandwidth.com/security.html)    | `u-123sdaf9834sd`      |
| `BANDWIDTH_API_TOKEN`  | [Bandwidth API Token](http://dev.bandwidth.com/security.html)  | `t-asdg920358askdf`    |
| `BANDWIDTH_API_SECRET` | [Bandwidth API Secret](http://dev.bandwidth.com/security.html) | `asdfkljasd2305jsdlkf` |

## Video Walk Through

[![](readme_images/play_file.png)](http://www.youtube.com/watch?v=MttOYzV6xK4 "Click to play on Youtube.com")


## Installation



### Clone this repo

```bash
git clone https://github.com/dtolb/bandwidth-python-quickstart.git

cd bandwidth-python-quickstart
```


### Create [Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

```bash
virtualenv -p {location_of_python3} bandwidth-python-quickstart

source bandwidth-python-quickstart/bin/activate
```

❗❗❗ When you're done be sure to `deactivate` ❗❗❗

```bash
deactivate
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Launch the App

```bash
FLASK_APP=app.py flask run
```

### Setup with ngrok

[Ngrok](https://ngrok.com) is an awesome tool that lets you open up local ports to the internet.

Once you have ngrok installed, open a new terminal tab and navigate to it's location on the file system and run:

```bash
./ngrok http 5000
```

You'll see the terminal show you information

![ngrok terminal](https://s3.amazonaws.com/bw-demo/ngrok_terminal.png)

### Create a bandwidth application

Head to [http://app.bandwidth.com](http://app.bandwidth.com) to create a new application

Set the application type to:

* Name: `bandwidth-python-quickstart`
* HTTP Method: `POST`
* App Type: `BOTH` : Both voice and messaging
* Voice callback URL: `http://your_ngrok.ngrok.io/inbound-voice-callbacks`
* Messaging callback URL: `http://your_ngrok.ngrok.io/inbound-message-callbacks`

![create app](readme_images/create_application.png)

### Assign a phone number to the application

If you don't already have a phone number, order one from the dashboard.

![Assign number](readme_images/add_number.gif)

### 👍👍 Then call that or text that number 👍👍
