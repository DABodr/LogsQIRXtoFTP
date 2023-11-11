import ftplib
import os
import pyautogui
import schedule
import time
import glob

# Paramètres FTP
ftp_server = "Your_FTP_URL"
ftp_username = "username"
ftp_password = "password"

# Dossier unifié pour les sorties (captures d'écran et fichiers HTML)
dossier_sortie_local = r"C:\QIRX_output"

# Nom du fichier image local
nom_fichier_image = "qirx.png"

# Dossier distant sur le serveur FTP où copier l'image
dossier_FTP_distant = "/QIRX/"

# Chemin du dossier pour la fonction txt_to_html
chemin_dossier_txt_to_html = r'C:\Users\Your_User\AppData\Local\qirx4\TIILogger'

# Nom du fichier HTML à créer
nom_fichier_html = "qirxtiilogs.html"

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

        with open(latest_txt_file, 'r') as txt_file, open(output_path, 'w') as html_file:
            html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>QIRX Logs</title>\n")
            html_file.write("<style>td:nth-child(1) { width: auto; white-space: nowrap; }</style>\n")
            html_file.write("<style>td:nth-child(6), td:nth-child(7) { background-color: #FFFF00; }</style>\n")
            html_file.write("</head>\n<body>\n")
            html_file.write("<table border='1' style='table-layout: fixed;'>\n")

            line_count = 0
            for line in txt_file:
                line = line.strip()
                cells = line.split('\t')

                if line_count > 2:
                    html_file.write("<tr>\n")
                    for idx, cell in enumerate(cells, 1):
                        if idx not in (6, 7, 10) and not (13 <= idx <= 17):
                            if 2 <= idx <= 5:
                                cell = f"<b>{cell}</b>"
                            html_file.write(f"<td>{cell}</td>\n")
                    html_file.write("</tr>\n")
                line_count += 1

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
        chemin_FTP_distant = f"/QIRX/{nom_fichier_html}"

        with open(fichier_local, "rb") as f:
            ftp.storbinary("STOR " + chemin_FTP_distant, f)

        print(f"Fichier HTML copié : {nom_fichier_html}")

        ftp.quit()
        print("Fichier HTML envoyé en FTP avec succès.")
    except Exception as e:
        print("Erreur envoi FTP du fichier HTML : " + str(e))

# Initialisation du script
print("Démarrage du script. Première action dans 30 secondes.")

# Planification des tâches
schedule.every(30).seconds.do(capture_ecran_et_enregistrer)
schedule.every(30).seconds.do(envoyer_image_ftp)
schedule.every(30).seconds.do(txt_to_html)
schedule.every(30).seconds.do(envoyer_fichier_ftp)

# Boucle principale
while True:
    schedule.run_pending()
    time.sleep(1)
