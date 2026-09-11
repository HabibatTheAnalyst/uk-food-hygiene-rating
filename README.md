# UK Food Hygiene Rating Data
[Link]{https://ratings.food.gov.uk/open-data}

The data was gotten from the Food hygiene ratings site [here]{https://ratings.food.gov.uk/}. There are [guidelines]{https://ratings.food.gov.uk/open-data-resources/documents/FHRS_APIv1_guidance_april24.pdf} on the site on how to use the API to access the food hygiene rating data. 

----------

### About the data
The data provides the food hygiene rating or inspection result given to a business and reflect the standards of food hygiene found on the date of inspection or visit by the local authority. Businesses include restaurants, pubs, cafés, takeaways, hotels and other places consumers eat, as well as supermarkets and other food shops.

as at when collected or the last rating date ....

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