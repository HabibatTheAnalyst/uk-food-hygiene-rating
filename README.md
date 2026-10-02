# UK Food Hygiene Rating Data
[Link]{https://ratings.food.gov.uk/open-data}

The data was gotten from the Food hygiene ratings site [here]{https://ratings.food.gov.uk/}. There are [guidelines]{https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf} on the site on how to use the API to access the food hygiene rating data. 

----------

### About the data
The data provides the food hygiene rating or inspection result given to a business and reflect the standards of food hygiene found on the date of inspection or visit by the local authority. Businesses include restaurants, pubs, cafés, takeaways, hotels and other places consumers eat, as well as supermarkets and other food shops.

as at when collected or the last rating date ....

NOTE : ratings data can be empty, if this occcurs, based on fhis? thesite?-----, there was probably a rescore. these data should be handled seperately. same applies to the adress and geolocation. if its empty. its mostlikely as a result of it being private location. read below for more/ to understand better.

The scores part of the data is only applicable to scheme type FHRS (not FHIS) and are for hygiene, structure and confidence in management. These scores can be found in part 2 and 3 of Annex 1, A1.1 of the Food Law code of Practice. These scores are then used to calculate the food hygiene rating details of which can be found in the Guidance on implementation and operation of the Food Hygiene Rating Scheme: the Brand Standard and statutory guidance. When a rescore is uploaded by a local authority the scores of hygiene, structure and confidence in management will not be available in the data.

Where the establishment is in operation from a private address the address and geocoding data may not be available.

---------
Where Awaiting Publication is displayed instead of a rating, this is where the business has appealed their rating, and the local authority is in the process of determining the appeal.

NewRatingPending is displayed as true in the data where a local authority has uploaded new data for an establishment which is not yet published as this data is in the notification or appeals period. It will be published after these time periods have elapsed. Where this is displayed as false, no new data is in the workflow to be published.

-------
ai response 

What the line is saying: Sometimes a business asks for a rescore, typically after fixing problems found at the original inspection. When a local authority uploads the result of that rescore, they only submit the new overall rating. They don't submit the three component scores, because a rescore is a re-assessment of the rating rather than a full new inspection with fresh scoring.

What this means for your data:

The three score columns will be empty (null/NA) for those records, even though the business is an FHRS-scheme business with a valid rating.
A missing score doesn't mean an error or that the business wasn't rated. It just means the rating came from a rescore.
If you're analysing the scores (e.g. averaging hygiene scores, or checking how scores map to ratings), you should expect gaps and decide how to handle them, such as excluding those rows or analysing them separately from the rating-only data.
Don't treat blanks as zeros. Note that in this scoring system a lower score is actually better (0 is the best), so filling blanks with 0 would make those businesses look perfect.


-----------
### General Notes below

The *uk-food-hygiene-rating* was created locally in the *projects* folder. Then the *requirements.txt* file was created using *touch file.txt*.
This repo cannot be stagged or pushed to github directly. 
- You first need to initialize it using 'git init'
- Then you add to github
    - git remote add origin https://github.com/yourusername/uk-food-hygiene-rating.git
    - git branch -M main
    - git push -u origin main

* Remember to always create a venv for any project so all installed packages are applied only to that project 

* Also create new branch and then merge to main. In essence, so not make chnages to the main branch

- Create, activate, and deactivate a virtual environment using
    - python3 -m venv venv
    - source venv/bin/activate
    - run 'deactivate'

- run *pip list* to see all installed packages and then add them manually to the reuirements file.
- Or you can run *pip freeze > requirements.txt*. This overwrites requirements.txt with every installed package and its exact version 