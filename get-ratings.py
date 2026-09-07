import csv
import xml.etree.ElementTree as ET
import requests

headers = {"x-api-version": "2"}
fields = [
    "BusinessName",
    "BusinessType",
    "AddressLine1",
    "AddressLine2",
    "AddressLine3",
]

page = 1
total_pages = 1
total_rows = 0

with open(
    "reading_food_ratings_all.csv", mode="w", newline="", encoding="utf-8"
) as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    while page <= total_pages:
        url = (
            f"https://api1-ratings.food.gov.uk/search/en-gb/^/reading/{page}/xml"
        )
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching page {page}. Stopping.")
            break

        root = ET.fromstring(response.content)

        # Retrieve total page count from metadata on first request
        if page == 1:
            total_pages = int(root.findtext(".//PageCount", default="1"))

        # Extract and count establishments
        establishments = root.findall(".//EstablishmentDetail")
        for establishment in establishments:
            row = {
                field: (establishment.findtext(field) or "").strip()
                for field in fields
            }
            writer.writerow(row)

        total_rows += len(establishments)
        # print(f"Scraped {page}/{total_pages} pages | Total Rows: {total_rows}")
        page += 1

print(f"Scraping completed. Extracted {total_rows} total rows across {total_pages} pages into 'reading_food_ratings_all.csv'.")