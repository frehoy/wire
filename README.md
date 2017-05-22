# wire

A small python script to get the latest news from [Reuters TheWire](http://www.reuters.com/theWire).
The script does two things: 
* Displays the latest news in terminal as it comes through
* Stores each article and some metadata to a json file, named after the articles id from Reuters.

It refreshes once a minute by default. 
All the articles are stored in a directory where the script is run.
