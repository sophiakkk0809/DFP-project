# Welcome to SaveMart!

Welcome to Savemart! Your one stop shop for finding the cheapest items within Pittsburgh. Are you tired of having to search multiple store retailers for low cost items? Do you want the ability to seemlessly find the cheapest available options for a desired grocery product?  Then you have found your answer. SaveMart app was desighned to provide Pittsburgh students with a better grocery shopping experience, by helping them save money and time in one application.


# Files

 - **TJ_Scraping.py :** Scrapes Data from Trader Joes (can load data into csv file).
 -  **target_scraping.py :** Scrapes Data from Target  (can load data into csv file).
 - **Aldi_Scraping.py:** Scrapes Data from Aldi (can load data into csv file).
 -  **journey.py:** Does a Google API call to get information for the distance and travel time for an origin to a destination.
 -  **model.py:** Main function for extracting the store that has the cheapest item amongst all the stores and passes that value to `gui_experiment.py`.
 - **gui_experiment.py:** Main function for getting data from each store. Extract the store that has the cheapest item for the store.
 - **requirements.txt:** Text file containing all required dependecies needed for this project to work. 


# Installation

 1. Clone the directory. Run the following command: `git clone https://github.com/sophiakkk0809/DFP-project.git `
 2. Navigate to the directory where the project was cloned. 
 3. Run the command `make setup` this will install all of the required dependecies.
     > **Note:** Ensure that you are in your python environment when running `make setup`. 
 4. Run the command `make run` this will run the program. You should see the application launch within a window on your screen. 

# Future Updates