import requests
from bs4 import BeautifulSoup
import time
import json
import csv

def scrape_annonces():
    all_annonces = []  # To store all the annonces across pages
    page_number = 1  # Start from page 1

    while True:
        # Construct the URL with the current page number
        url = f"http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={page_number}"
        print(f"Fetching page {page_number}...")

        # Send a GET request to the website
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}, status code: {response.status_code}")
            break
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rows in the page that are annonces
        rows = soup.find_all('tr', class_='Tableau1')

        if not rows:  # If no rows are found, break the loop (last page)
            print(f"No annonces found on page {page_number}. Ending scraping.")
            break

        # Extract data for each annonce
        for row in rows:
            try:
                # Extracting annonce details from each cell in the row
                columns = row.find_all('td')

                # Make sure we have enough columns
                if len(columns) > 10:
                    region = columns[1].get_text(strip=True)  # Region
                    nature = columns[3].get_text(strip=True)  # Nature
                    annonce_type = columns[5].get_text(strip=True)  # Type
                    text_annonce = columns[7].get_text(strip=True)  # Text annonce
                    prix = columns[9].get_text(strip=True)  # Price
                    modified_date = columns[11].get_text(strip=True)  # Modified date
                    annonce_link = columns[7].find('a')['href']  # Link to annonce

                    all_annonces.append({
                        "region": region,
                        "nature": nature,
                        "type": annonce_type,
                        "text_annonce": text_annonce,
                        "prix": prix,
                        "modified_date": modified_date,
                        "lien": annonce_link
                    })

                # Save the data after each page is processed
                with open("data/annonces.json", "w", encoding="utf-8") as f:
                    json.dump(all_annonces, f, indent=4)
                print(f"Data saved to 'data/annonces.json' after page {page_number}.")

                # Save the data in CSV format after each page is processed
                with open("data/annonces.csv", "w", encoding="utf-8", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=["region", "nature", "type", "text_annonce", "prix", "modified_date", "lien"])
                    writer.writeheader()
                    writer.writerows(all_annonces)
                print(f"Data saved to 'data/annonces.csv' after page {page_number}.")

            except Exception as e:
                print(f"Error extracting data from row: {e}")

        print(f"Found {len(rows)} annonces on page {page_number}.")
        page_number += 1  # Increment page number for the next loop

        # Add a short delay to prevent being flagged as a bot
        time.sleep(1)

    return all_annonces

if __name__ == "__main__":  # Corrected the typo here
    scrape_annonces()
