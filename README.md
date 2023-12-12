Take a windows PC screenshot each 30 seconds (let QIRX running in front) and send QIRX modified logs from C:\Users\Your_User\AppData\Local\qirx4\TIILogger to FTP server in QIRX/ directory.

QIRX screenshot webpage:

![Screenshot QIRX](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotQIRX.png) 

TII modified logs from QIRX:

![Screenshot logs](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotLogs.png)

New directory C:\QIRX_output is create for save PNG picture and HTML file.

* Install:

1 - Download and install latest python software: https://www.python.org/downloads/

2 - Download git: https://github.com/DABodr/LogsQIRXtoFTP/archive/refs/heads/main.zip and unzip

3 - Install pip: Run install-pip.bat

4 - Install dependecy: pip install pyautogui schedule glob2 pandas Pillow

5 - Open with file editor LogsQIRXtoFTP.py and edit your FTP address, name and password, save it.

6 - Copy "logodab.png", "backgrnddab.jpeg" and "qirx.html" files to your QIRX/ FTP folder

7 - Run LogsQIRXtoFTP.py

8 - Go to http://Your_Server_address/QIRX/qirx.html

* Uncomment lines 164 to 170 for show all TII (Even those that are not available in the database.)
