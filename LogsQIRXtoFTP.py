import ftplib
import os
import pyautogui
import schedule
import time
import glob
import csv
import pandas as pd
from datetime import datetime, timedelta
import io

# Paramètres FTP
ftp_server = "FTPperso.free.fr"
ftp_username = "aurelien.picart"
ftp_password = "4d967f6c"

# Obtenir le nom d'utilisateur actuel Windows
username = os.getlogin()  # ou os.environ['USERNAME']

# Chemin d'accès base TII Locale
base_tii = rf'C:\Users\{username}\Desktop\dabtx_data.csv'

# Dossier unifié pour les sorties (captures d'écran et fichiers HTML)
dossier_sortie_local = r"C:\QIRX_output"

# Nom du fichier image local
nom_fichier_image = "qirx.png"

# Dossier distant sur le serveur FTP où copier l'image
dossier_FTP_distant = "/QIRX/"

# Chemin du dossier pour la fonction txt_to_html
chemin_dossier_txt_to_html = rf'C:\Users\{username}\AppData\Local\qirx4\TIILogger'

# Nom du fichier HTML à créer
nom_fichier_html = "qirxtiilogs.html"

# Chargement base TII en RAM
with open(base_tii, 'r', encoding='utf-8', errors='ignore') as tiiFile:
    reader = csv.reader(tiiFile , delimiter=';')
    tiiTab = list(reader)

# Vérification de l'existence du dossier, le créer si nécessaire
def verifier_et_creer_dossier():
    if not os.path.exists(dossier_sortie_local):
        os.makedirs(dossier_sortie_local)

# Fonction pour effectuer une capture d'écran et l'enregistrer
def capture_ecran_et_enregistrer():
    try:
        verifier_et_creer_dossier()
        
        # Capture d'écran
        capture = pyautogui.screenshot()

        # Enregistrement de la capture
        chemin_fichier = os.path.join(dossier_sortie_local, nom_fichier_image)
        capture.save(chemin_fichier)

        print(f"Capture d'écran enregistrée : {nom_fichier_image}")

    except Exception as e:
        print(f"Erreur capture d'écran : {e}")

# Fonction pour envoyer l'image vers le serveur FTP
def envoyer_image_ftp():
    try:
        verifier_et_creer_dossier()

        ftp = ftplib.FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        # Création du dossier distant si nécessaire
        try:
            ftp.mkd(dossier_FTP_distant)
        except ftplib.error_perm:
            pass  # Le répertoire existe déjà

        # Copie de l'image
        chemin_local = os.path.join(dossier_sortie_local, nom_fichier_image)
        chemin_distant = os.path.join(dossier_FTP_distant, nom_fichier_image)

        with open(chemin_local, "rb") as f:
            ftp.storbinary("STOR " + chemin_distant, f)

        print(f"Image copiée : {nom_fichier_image}")

        ftp.quit()
        print("Image envoyée en FTP. Prochaine capture dans 30 secondes.")

    except Exception as e:
        print("Erreur envoi image : " + str(e))
        print("Nouvelle tentative dans 30 secondes.")

# Fonction pour convertir les fichiers .txt en fichiers HTML
def txt_to_html():
    verifier_et_creer_dossier()
    txt_files = sorted(glob.glob(os.path.join(chemin_dossier_txt_to_html, '*.txt')), key=os.path.getmtime, reverse=True)

    if txt_files:
        latest_txt_file = txt_files[0]
        output_path = os.path.join(dossier_sortie_local, nom_fichier_html)
        with open(latest_txt_file, 'r', encoding="UTF-8") as txt_file, open(output_path, 'w') as html_file:
            # On ignore les 3 premières lignes du fichier TII
            for _ in range(3):
                next(txt_file)

            # On supprime les espaces, et on gère la séparation par une tabulation
            column_names = next(txt_file).split("\t")
            column_names = [x.strip(' ') for x in column_names]
            next(txt_file)

            # DataFrame => Dict, on supprime les timestamp null et on trie en fonction du TII
            df = pd.read_csv(txt_file, delimiter='\t', header=None, names=column_names, skiprows=[0,1,2,3,4])
            df = df[df['Date/Time'] != '0001-01-01  00:00:00 Z']
            df['MER'] = pd.to_numeric(df['MER'])
            df['M_Id'] = pd.to_numeric(df['M_Id'])
            df['S_Id'] = pd.to_numeric(df['S_Id'])
            df['Chn'] = df['Chn'].apply(lambda x: "0" + str(x) if len(str(x)) == 2 else x) #On ajoute un 0 sur les canaux 5A->9D pour faciliter le tri
            df_sorted = df.sort_values(['Date/Time', 'MER', 'M_Id', 'S_Id', 'Chn', 'EId'], ascending=[False, True, True, True, False, False])
            result = df_sorted.groupby(['Chn','M_Id', 'S_Id']).first()
            print(result)
            
            # Génération du tableau final
            html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>QIRX Logs</title>\n")
            html_file.write("<style>table { background-color: #e0ffe0; font-family:'Arial'}</style>\n")
            html_file.write("<style>td:nth-child(1) { width: auto; white-space: nowrap; }</style>\n")
            html_file.write("<style>td:nth-child(6), td:nth-child(7), td:nth-child(10) { background-color: #FFFF00; }</style>\n")
            html_file.write("</head>\n<body>\n")
            html_file.write("<table border='1' style='table-layout: fixed;'>\n")
            html_file.write("<tr><td>Date & Heure du Scan</td><td>Bloc</td><td>EId</td><td>Label</td><td>MER</td><td>M_Id</td><td>S_Id</td><td>Dist. km</td><td>Force</td><td>TX (+ Puissance)</td></tr>")

            # Recherche du TII dans la base
            lhFound = False
            for (Chn,M_Id, S_Id), rowOrig in result.iterrows():
                if(Chn[0] == "0"):
                    Chn = Chn[1:]
                row = rowOrig.to_dict()
                color = "darkgreen"
                colorFont = "white"
                found = False
                if(row['MER'] < 15):
                    color = "darkorange"
                    colorFont = "black"
                if(row['MER'] < 10):
                    color = "red"
                    colorFont = "white"
                
                timestampUtc = datetime.strptime(row['Date/Time'], '%Y-%m-%d %H:%M:%S Z')
                timestampCet = timestampUtc + timedelta(hours=1)
                row['Date/Time'] = timestampCet.strftime('%Y-%m-%d %H:%M:%S')

                for r in tiiTab:
                    mainSub = str(M_Id).rjust(2,"0").strip() + str(S_Id).rjust(2,"0").strip()
                    if(Chn == r[2] and str(row['EId']) == r[4] and mainSub == r[5]):
                        tx = r[6]
                        try:
                            pwr = str(round(float(r[13]), 2))
                        except:
                            pwr=""  
                        html_file.write("<tr><td>" + row['Date/Time'] + "</td><td><b>" + Chn + "</b></td><td>" + str(row['EId']) + "</td><td style='font-family:courier;width:160px;' ><b>" + row['Label'][1:-1] + "</b></td><td style='background-color:"+color+"; color: "+colorFont+"'>" + str(row['MER']) + "</td><td>" + str(M_Id) +"</td><td>" + str(S_Id) + "</td><td>" + str(row['km abs']) + "</td><td>" + str(round(row['Stren']*100,2)) + " %</td><td>" + tx + " (" + pwr +" kW)</td></tr>\n")
                        found = True
                        break
                # Décommenter ces lignes pour laisser apparaitre les TII non listés dans la base de données    
                #if(found == False):
                    #if(str(row['EId']) != "F017"):
                        #html_file.write("<tr><td>" + row['Date/Time'] + "</td><td><b>" + Chn + "</b></td><td>" + str(row['EId']) + "</td><td style='font-family:courier;width:150px;' ><b>" + row['Label'][1:-1] + "</b></td><td style='background-color:"+color+"; color: "+colorFont+"'>" + str(row['MER']) + "</td><td>" + str(M_Id) +"</td><td>" + str(S_Id) + "</td><td>" + str(row['km abs']) + "</td><td>" + str(round(row['Stren']*100,2)) + " %</td><td></td></tr>\n")
                    #else:
                        #if(lhFound == False):
                            #html_file.write("<tr><td>" + row['Date/Time'] + "</td><td><b>" + Chn + "</b></td><td>" + str(row['EId']) + "</td><td style='font-family:courier;width:150px;' ><b>" + row['Label'][1:-1] + "</b></td><td style='background-color:"+color+"; color: "+colorFont+"'>" + str(row['MER']) + "</td><td>-</td><td>-</td><td>" + str(row['km abs']) + "</td><td>" + str(round(row['Stren']*100,2)) + " %</td><td>Fresnicourt-le-Dolmen (4.0 kW)</td></tr>\n")
                            #lhFound = True

            html_file.write("</table>\n</body>\n</html>")

        print(f'HTML créé : {nom_fichier_html}')
    else:
        print('Aucun fichier .txt trouvé.')

# Fonction pour envoyer le fichier HTML vers le serveur FTP
def envoyer_fichier_ftp():
    try:
        verifier_et_creer_dossier()

        ftp = ftplib.FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        fichier_local = os.path.join(dossier_sortie_local, nom_fichier_html)
        chemin_FTP_distant = f"/{dossier_FTP_distant}/{nom_fichier_html}"

        with open(fichier_local, "rb") as f:
            ftp.storbinary("STOR " + chemin_FTP_distant, f)

        print(f"Fichier HTML copié : {nom_fichier_html}")

        ftp.quit()
        print("Fichier HTML envoyé en FTP avec succès.")
    except Exception as e:
        print("Erreur envoi FTP du fichier HTML : " + str(e))

# Initialisation du script
print("Démarrage du script.")
capture_ecran_et_enregistrer()
envoyer_image_ftp()
txt_to_html()
envoyer_fichier_ftp()

# Planification des tâches
schedule.every(15).seconds.do(capture_ecran_et_enregistrer)
schedule.every(15).seconds.do(envoyer_image_ftp)
schedule.every(30).seconds.do(txt_to_html)
schedule.every(30).seconds.do(envoyer_fichier_ftp)

# Boucle principale
while True:
    schedule.run_pending()
    time.sleep(1)
tiiFile.close()
