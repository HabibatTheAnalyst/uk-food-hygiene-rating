import csv
import xml.etree.ElementTree as ET
import requests

# Direct bulk download for Reading Local Authority
url = "https://ratings.food.gov.uk/OpenDataFiles/FHRS884en-GB.xml"
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

response = requests.get(url)
print(f"Downloaded {len(response.content)} bytes from {url}")
root = ET.fromstring(response.content)

with open(
    "reading_food_ratings.csv", mode="w", newline="", encoding="utf-8"
) as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(field_map.keys()))
    writer.writeheader()

    establishments = root.findall(".//EstablishmentDetail")
    print(f"Found {len(establishments)} establishments in the XML data.")
    for est in establishments:
        row = {
            col: (est.findtext(path) or "").strip()
            for col, path in field_map.items()
        }
        writer.writerow(row)

print(f"Done! Downloaded and parsed {len(establishments)} total records.")