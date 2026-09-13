import csv
import xml.etree.ElementTree as ET

import requests

descriptors_url = "https://ratings.food.gov.uk/open-data-resources/lookupData/ScoreDescriptors.xml"

field_map = {
    "description": "Description",
    "id": "Id",
    "score": "Score",
    "scorecategory": "ScoreCategory"
}

response = requests.get(descriptors_url)
print(f"Response status: {response.status_code}")

root = ET.fromstring(response.content)
descriptors = root.findall("./scoreDescriptors/scoreDescriptors")

with open(
    "score_descriptors.csv", mode="w", newline="", encoding="utf-8"
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_map.keys())
    writer.writeheader()
    for descriptor in descriptors:
        row = {
            col: (descriptor.findtext(path) or "").strip()
            for col, path in field_map.items()
        }
        writer.writerow(row)
print(f"Scraping done. {len(descriptors)} total rows.")