# Parktake
#### Cause the Outdoors Await
---
![alt text](https://raw.githubusercontent.com/sabellachan/parks-map/master/static/readme/homepagescreenshot.png "Homepage")
Parktake was inspired by a love of adventure. Recreation areas overseen by The National Parks Service are presented on an easy-to-use map for users to discover, explore, and check off that they've visited. This app is intended for users who love to go outdoors and would like a visual record of where they've been.

## Technical Stack
---
* Python
* Javascript
* SQLAlchemy
* Jinja2
* HTML
* jQuery
* Flask
* SQLite
* Bootstrap
* Chart.js
* CSS
* Unittest

## APIs Used
---
* [Recreation Information Database](https://ridb.recreation.gov)
* Google Maps
* Google Maps Geocode

## Feature List
---
#### User Accounts
Users can sign up, login, and logout, as well as update their profiles.

#### Search
![alt text](https://raw.githubusercontent.com/sabellachan/parks-map/master/static/readme/03-search.gif "Search")
Users can search for different geographic areas using Google Maps Autocomplete and the recreation areas nearby are marked on a customized Google Map.

#### Check Off Parks
![alt text](https://raw.githubusercontent.com/sabellachan/parks-map/master/static/readme/01-addingparks.gif "Adding Parks")
Users can click on recreation areas, indicated by markers on the Google Map, to find the name, description, and what activities are offered. Click a button to mark it as visited.

#### View Visit History
![alt text](https://raw.githubusercontent.com/sabellachan/parks-map/master/static/readme/02-viewparks.gif "View History")
A list of visited recreation areas is recorded, giving the name and location of where each one is. A Chart.js doughtnut chart represents a summary of what states the visits took place in. 

#### Discover A New Park
Based on the user's visit history, a new recreation area is suggested using machine learning with an implementation of the Pearson's correlation coefficient.

## Favorite Challenges
---
* Google Maps API
* Utilizing Pearson's algorithm for suggestion engine
* Figuring out how to collect visit history data to be read by Chart.js
* Integration testing the app

## About the Developer
---
Jacqueline Huynh is a software developer living in the San Francisco Bay Area.
