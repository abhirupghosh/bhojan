## Bhojan
_Submission for HackGSU Fall 2019 with a team of 2, Winner: Best use of Microsoft Azure_
# Inspiration
Our application has two major use cases: 
_Faster service at restaurants_
How many times have you waited on your table for a server, only to figure that the restaurant is out of your favourite dish? Bhojan looks to eliminate any manual inefficiencies in the ordering process at a restaurant. With our client-facing and business-facing dashboards, integrated with a realtime database, AI that automatically finds menu items with their corresponding prices, and hopefully NCR's kickass banking APIs soon, Bhojan solves exactly that.

_Small-scale businesses_
More often than not, small eateries tend to have amazing food. However, they barely have any online exposure and often lack the technological skills to list themselves on websites, complete with their food options and prices. With Bhojan, these restaurants can add to a centralised database of restaurants and gain a broader exposure. A win-win situation for both consumers, who can now taste some delicious, underrated food, and for the business, who has much more exposure.

# What it does
Bhojan starts off with a photo page, where you can upload images of your menu. Using Azure's Compute APIs, which include the Read API, WordCorrect API, and their NLP models, Bhojan extracts menu items with their corresponding prices. At the same time, if the enterprise isn't listed on the database, they must fill in their inventory for the items on the menu. After this process is done, the data is fed into a database and the user is taken to the order page. Here, the user enters what they want to order and it is passed onto the restaurant. They are notified of the Delivery Process by SMS, using Twilio's APIs which are hosted on Azure function containers. Finally, they are given a confirmation page with their final order and total cost.

# How we built it
We used Azure, Firebase to host data, Twilio's APIs for SMS, and NCR for a banking solution that is still in progress on the order page.

# Challenges we ran into
It was extremely difficult for us to learn and implement http requests from an html front end file. The get attribute of the HTML form didn’t post a valid URL and hence we weren’t able to successfully link the front-end to the back-end for a very long time

# What we are proud of
We managed to successfully integrate the HTML front end and the Firebase back-end to Microsoft’s Azure functions and API. We also integrated Twilio’s API

# What we learned
We learned how to use many APIs and NCRs solutions.

# What's next for Bhojan
Integration with Yelp and Zomato's APIs to provide more food menus.
