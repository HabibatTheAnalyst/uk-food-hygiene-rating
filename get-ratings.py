import csv
import xml.etree.ElementTree as ET
import requests

headers = {"x-api-version": "2"}

# Mapping CSV column names to their XML paths
field_map = {
    "BusinessName": "BusinessName",
    "BusinessType": "BusinessType",
    "AddressLine1": "AddressLine1",
    "AddressLine2": "AddressLine2",
    "AddressLine3": "AddressLine3",
    "PostCode": "PostCode",
    "RatingValue": "RatingValue",
    "RatingDate": "RatingDate",
    "LocalAuthorityName": "LocalAuthorityName",
    "Hygiene": ".//Scores/Hygiene",
    "Structural": ".//Scores/Structural",
    "ConfidenceInManagement": ".//Scores/ConfidenceInManagement",
    "Longitude": ".//Geocode/Longitude",
    "Latitude": ".//Geocode/Latitude",
}

fields = list(field_map.keys())

page = 1
total_pages = 1
total_rows = 0

with open(
    "reading_food_ratings.csv", mode="w", newline="", encoding="utf-8"
) as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    print("Starting scraping process...")

    while page <= total_pages:
        url = (f"https://api1-ratings.food.gov.uk/search/en-gb/^/reading/{page}/xml")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching page {page}. Stopping.")
            break

        root = ET.fromstring(response.content)

        # Retrieve total page count on the first request
        if page == 1:
            total_pages = int(root.findtext(".//PageCount", default="1"))
            print(f"Total pages to scrape: {total_pages}")

        establishments = root.findall(".//EstablishmentDetail")
        for establishment in establishments:
            row = {}
            for col_name, xml_path in field_map.items():
                text = establishment.findtext(xml_path)
                row[col_name] = text.strip() if text else ""
            writer.writerow(row)

        total_rows += len(establishments)
        # print(f"Scraped {page}/{total_pages} pages | Total Rows: {total_rows}")
        page += 1

print(f"Scraping completed. Extracted {total_rows} total rows across {total_pages} pages into 'reading_food_ratings.csv'.")