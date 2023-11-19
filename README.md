Take a windows PC screenshot each 30 seconds (let QIRX running in front) and send QIRX logs from C:\Users\Your_User\AppData\Local\qirx4\TIILogger to FTP server in QIRX/ directory.

QIRX screenshot webpage:

![Screenshot QIRX](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotQIRX.png) 

TII logs from QIRX:

![Screenshot logs](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotLogs.png)

New directory C:\QIRX_output is create for save PNG picture and HTML file.

* Install:

1- Download and install latest python software: https://www.python.org/downloads/

2 - Download git: https://github.com/DABodr/LogsQIRXtoFTP.git and unzip

3 - Install Library: Run install.bat

4 - Open with file editor LogsQIRXtoFTP.py and edit your FTP address, name and password, save it.

5 - Copy "logodab.png", "backgrnddab.jpeg" and "qirx.html" files to your QIRX/ FTP folder

6 - Run LogsQIRXtoFTP.py

7 - Go to http://Your_Server_address/QIRX/qirx.html
