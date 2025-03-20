from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
import os
import json
import csv
import io
import uvicorn

from scraping.scraper import scrape_annonces

app = FastAPI()

# Ensure the 'data' folder exists before scraping
DATA_DIR = "data"
JSON_FILE = os.path.join(DATA_DIR, "annonces.json")
CSV_FILE = os.path.join(DATA_DIR, "annonces.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.get("/")
async def welcome():
    return JSONResponse(content={"message": "Welcome to the FastAPI application for web scraping and data conversion."})

@app.get("/scrape")
async def scrape():
    try:
        annonces = scrape_annonces()  # Scrape data
        if not annonces:
            return JSONResponse(content={"status": "error", "message": "No data scraped."}, status_code=404)
        
        # Save to JSON file
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(annonces, file, indent=4, ensure_ascii=False)
        
        # Save to CSV file
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["region", "nature", "type", "text_annonce", "prix", "modified_date", "lien"])
            writer.writeheader()
            writer.writerows(annonces)

        return JSONResponse(content={"status": "success", "data": annonces})
    
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/download_json")
async def download_json():
    if os.path.exists(JSON_FILE):
        return FileResponse(JSON_FILE, media_type="application/json", filename="annonces.json")
    return JSONResponse(content={"status": "error", "message": "JSON file not found."}, status_code=404)

@app.get("/download_csv")
async def download_csv():
    if os.path.exists(CSV_FILE):
        return FileResponse(CSV_FILE, media_type="text/csv", filename="annonces.csv")
    return JSONResponse(content={"status": "error", "message": "CSV file not found."}, status_code=404)

@app.get("/listings")
async def get_listings(format: str = "json"):
    """
    Endpoint to display the listings in JSON or CSV format.
    Pass the query parameter format=csv to get the data in CSV format.
    By default, it returns the data in JSON format.
    """
    try:
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if format == "csv":
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=["region", "nature", "type", "text_annonce", "prix", "modified_date", "lien"])
                writer.writeheader()
                writer.writerows(data)
                
                return StreamingResponse(io.StringIO(output.getvalue()), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=annonces.csv"})

            return JSONResponse(content={"status": "success", "data": data})

        return JSONResponse(content={"status": "error", "message": "No listings found (JSON file missing)."}, status_code=404)
    
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
