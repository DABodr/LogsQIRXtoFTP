Take a windows PC screenshot each 30 seconds (let QIRX running in front) and send QIRX logs from C:\Users\Your_User\AppData\Local\qirx4\TIILogger to FTP server in QIRX/ directory.

QIRX screenshot webpage:

![Screenshot QIRX](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotQIRX.png) 

TII logs from QIRX:

![Screenshot logs](https://github.com/DABodr/LogsQIRXtoFTP/blob/main/screenshotLogs.png)

New directory C:\QIRX_output is create for save PNG picture and HTML file.

* Install:

1 - Download git and unzip

2 - Open with file editor LogsQIRXtoFTP.py and edit your FTP address, name and password, save it.

3 - Copy "logodab.png", "backgrnddab.jpeg" and "qirx.html" files to your QIRX/ FTP folder

4 - Install Library:

*Run cmd command
*pip install os-sys pyautogui schedule glob2 pandas Pillow

5 - Run LogsQIRXtoFTP.py

6 - Go to http://Your_Server_address/QIRX/qirx.html
