# PythonAdvanceKeylogger
This project involves the creation of an advanced keylogger written in Python. The keylogger captures keystrokes, browser history, and screenshots. The captured data is periodically sent to a specified email address for analysis or monitoring.

## Warning: This project is intended for educational and security research purposes only. Unauthorized access to others' data without their explicit consent is illegal and unethical. Ensure compliance with legal guidelines before using or deploying this tool.

## Features
* Keystroke Logging: Captures all keystrokes from the keyboard, recording them with timestamps.
* Browser History Tracking: Extracts browsing history from common web browsers (Chrome, Firefox, edge).
* Screenshot Capturing: Periodically takes screenshots of the screen at user-defined intervals.
* Email Reporting: Sends captured logs, browser history, and screenshots to a specified email address.

## Requirements
* Python 3.7 or higher

### Standard Libraries (included with Python, so no installation needed):

* os
* time
* datetime
* threading
* smtplib
* email (for MIMEMultipart, MIMEText, MIMEBase, and encoders)

### External Libraries (require installation):

* Pillow (PIL): Used for capturing screenshots with ImageGrab.
* browser_history: Specifically for accessing browser history from Chrome, Firefox, and Edge.
* keyboard: Used to capture keystrokes.

## Installation
Clone the repository:
```bash
https://github.com/Anurag0218/PythonAdvanceKeylogger.git
```

Install dependencies:
```bash
pip install pillow browser-history keyboard
```
## Email Configuration:
Configuration
Before using the keylogger, you need to configure the email settings to ensure that logs can be sent to the desired email address.
Open the main.py file.

### Set your email server details:
```
sender: Your email address.
password: Your email password (ensure secure handling, especially if stored locally).
receivers: The recipient email address where logs will be sent.
```

## Run the Keylogger:
```bash
python main.py
```
Logs and screenshots will be automatically emailed to the specified address at regular intervals.

An example of the email report include:
* Keystroke Log: A record of all keystrokes captured.
* Browser History Log: URLs visited in the user's browsers.
* Screenshots: Image files capturing the screen at intervals.

## Legal Disclaimer
This keylogger project is for educational purposes only. Unauthorized use of this tool to collect information from devices without the owner’s consent is a violation of privacy and is illegal. Always obtain explicit permission before using this tool on any device that you do not own.

