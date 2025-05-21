#!/usr/bin/env python3
"""
check_websites.py: Vérifie périodiquement la disponibilité de sites web.

Usage:
    python check_websites.py --file sites.txt
    - "sites.txt" doit contenir une URL par ligne.

Le script exécute une vérification toutes les 10 heures.
"""
import argparse
import requests
import schedule
import time
import logging

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("site_check.log"), logging.StreamHandler()]
)


def sendMail(mails,site,etat):

    for mail in mails:
        expediteur= "contact@codingagain.com"
        sujet = "Etat off pour: "+site
        message = MIMEMultipart()
        message['From'] = expediteur
        message['To'] = mail
        message['Subject'] = sujet
        corps_du_message = etat
        message.attach(MIMEText(corps_du_message, 'plain'))
        serveur_smtp = "mail.codingagain.com"
        port_smtp = 465
        nom_utilisateur = "contact@codingagain.com"
        mot_de_passe = "2885351Aristide12@"
        s = smtplib.SMTP_SSL(host=serveur_smtp, port=port_smtp)
        s.login(nom_utilisateur, mot_de_passe)
        texte = message.as_string()
        s.sendmail(expediteur, mail, texte)
        s.quit()


def load_urls_from_file(filepath):
    """Charge les URLs depuis un fichier, une par ligne."""
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def check_sites(urls, timeout=10):
    """Vérifie chaque URL et logge le statut HTTP."""
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout)
            if response.ok:
                logging.info(f"{url} est en ligne (HTTP {response.status_code})")
            else:
                logging.warning(f"{url} est en ligne mais renvoie HTTP {response.status_code}")
                sendMail(["ouedraogoaris@gmail.com"],url,"Le site "+url+" est off et renvoie du HTTP "+str(response.status_code))
        except requests.RequestException as e:
            sendMail(["ouedraogoaris@gmail.com"],url,"Le site "+url+" est hors ligne")

            logging.error(f"Impossible d'atteindre {url}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Vérification périodique de sites web.")
    parser.add_argument(
        '--file', '-f', required=True,
        help='Chemin vers le fichier contenant la liste d\u2019URLs, une par ligne'
    )
    args = parser.parse_args()

    urls = load_urls_from_file(args.file)
    if not urls:
        logging.error("Aucune URL chargée. Vérifiez votre fichier.")
        return

    # Planification de la tâche 
    #schedule.every(10).hours.do(check_sites, urls)
    tempEnMinute=1
    schedule.every(tempEnMinute).minutes.do(check_sites, urls)

    logging.info("Démarrage de la vérification toutes les "+str(tempEnMinute)+"mn ..... ")
    # Exécution continue
    while True:
        schedule.run_pending()
        time.sleep(60)  # On dort 60 secondes entre chaque vérification des tâches planifiées


if __name__ == '__main__':
    main()
