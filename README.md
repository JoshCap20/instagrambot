# instagrambot
Python bot that demonstrates Selenium capabilities for Instagram. Like and comment on accounts by hashtag or account named with related account features.

# Configuration
1. Add login information to settings.py.  
2. Configure the comments and accounts to comment on in settings.py.   
3. In main.py, either use AccountInstagramBot() to comment on specified accounts or HashtagInstagramBot("HASHTAG_HERE") to like and comment on posts with this hashtag.  


# Setup
If you don't know how to install the requirements, I'm not gonna help you. There's too many bots on Instagram already; this is just for the Python community.

# Features
Class HashtagInstagramBot: Comments and likes on images with a specified hashtag. Initialize objects with hashtag.  
Example: <code>Bot1 = HashtagInstagramBot("softwaredeveloper")</code>.  
Class AccountInstagramBot: Comments on accounts with certain words in name or from specified list in settings.py. Not initialized with any arguments.  
Example: <code> Bot2 = AccountInstagramBot() </code>.  
