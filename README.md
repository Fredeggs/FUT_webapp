# FUT (FIFA Ultimate Team) Web App

## What does this app do?
The FUT Web App is a tool for people who like to play the latest FIFA games, specifically in the Ultimate Team game mode. This app will allow users to build and share teams with other users on the app. Teams are made up of players and each player has his own stats, nationality and club. All player data is updated and managed through the futdb API (https://futdb.app/api/doc).

## App Features
### Team Building
Users can go to a blank team sheet, select a formation, and individually add players by clicking an empty slot. Once completed, the team can be named and shared to other users on the app. 

### Team Filtering
Users can easily filter through teams on the '/teams' route by selecting a dropdown box to filter by date, rating, price, etc. This feature allows users to gain inspiration from others and even copy/tweek existing teams.

## Like and Comment on Teams
Users can like or comment on teams made by the user or other users. This can provide feedback or compliments to the creator of the team. This can also improve the filtering tool by filtering for the most liked team or the most commented team.

### Player Search
Users can go to the '/players' route to search for specific players based on their name. This is simply done by typing a name into a text input box and submitting. Results will be sent back from the futdb API (https://futdb.app/api/doc) and will populate the page. The user can then click the players and be brought to their player page where they can view a more detailed breakdown of the player's stats and information.

## User flow
1. Unauthenticated users will be directed to the landing page where they will be prompted to login or signup
2. Once logged in, user will be routed to the '/teams' page where they will see teams created by other users.
3. Users can go anywhere from there. They could click on a team and view that team's individual team page.
4. Users could instead go to the player search page using the toolbar at the top of the page
5. Users could also select their profile and make edits such as changing their avatar or changing their bio. Users can also navigate to other user profiles to view information such as their liked teams or teams they created.
6. Lastly, users could navigate to the 'Create Team' page and start building a team of their own. 

## Tech stack
This app was built with the Flask web framework and utilizes Postgres and SQLAlchemy to communicate with and maintain a database. The frontend is made with vanilla Javascript and jQuery. The majority of the styling for this website comes from themeforest's "BlockBuster - Film Review & Movie Database HTML Template" built by username: leehari.
