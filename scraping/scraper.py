# scraping/scraper.py
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import json
import csv
from scraping.config import EDGE_DRIVER_PATH, BASE_URL 


def scrape_annonces():
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    
    driver.get(BASE_URL)
    time.sleep(5)  # Laisser le temps à la page de charger

    annonces = []
    elements = driver.find_elements(By.CLASS_NAME, "DernieresAnnonces")  # Adapter selon le site

    for element in elements:
        titre = element.find_element(By.CLASS_NAME, "titre").text
        prix = element.find_element(By.CLASS_NAME, "prix").text
        localisation = element.find_element(By.CLASS_NAME, "localisation").text
        lien = element.find_element(By.TAG_NAME, "a").get_attribute("href")

        annonces.append({
            "titre": titre,
            "prix": prix,
            "localisation": localisation,
            "lien": lien
        })

    driver.quit()

    with open("data/annonces.json", "w", encoding="utf-8") as f:
        json.dump(annonces, f, indent=4)

    with open("data/annonces.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["titre", "prix", "localisation", "lien"])
        writer.writeheader()
        writer.writerows(annonces)

    return annonces
