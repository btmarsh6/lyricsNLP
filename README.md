# Topic Modeling in Rap Lyrics

## Goals
The goal of this project is to apply topic modeling to lyrics from rap albums in order to discover trends in topics. This could be used to group artists who rap about similar content together and discover what trends in topics might exist either across different regions or over time.

## Process:
I started by compiling a list of albums by influential/successful artists to build my library of songs from. I wanted to ensure I had rappers from different cities, looking to get a balance between East Coast, West Coast, Midwest and Southern rappers. I also wanted to make sure I was including albums from the 80s through to the present day. There is a bit of an imbalance towards more East Coast rappers, especially from earlier years, as the birthplace of the music was in the Bronx and many of the earliest recording artists were from that region.

I then used the lyricsgenius API to download a JSON of each album containing the lyrics for each track and other meta-data. From the JSON files, I extracted the lyrics, track titles, album title, artist and release year, then stored that information in a SQL database. With lyrics coming from web scraping, there was significant cleaning needed to remove extraneous labels, song structure markers, and in-line advertisements.

I used BERTopic to perform the topic modeling. Initially, I passed the full string of each song to the model. The model was clustering nearly all of the songs into a single topic cluster. I then attempted to break each song into smaller chunks of 4 or 8 lines and run the topic modeling on smaller chunks of songs. The hope is that will improve the model's ability to create distinct clusters. Once I have satisfactory clustering, topics for each song will then be determined by the highest probability cluster for each of the chunks of the song.

## Current Status
Working on improving the clusters formed by the model running on smaller song chunks and adjusting BERTopic hyperparameters.
Most songs are being clustered into one topic group. Currently, I am exploring this group and the 3 other small clusters to understand better why the clustering is happening like this. Also exploring finetuning Sentence Transformer on this dataset.

## Challenges and Future Work
This project is currently based primarily on studio albums and occasionally some mixtapes. In the age of music streaming, many artists are now focusing less on putting out full albums and instead just releasing one off songs as singles. These songs are not included in the data unless they also appear on an album. Additionally, my methodology does not account for features and collaborations. All words from a song are attributed to the artist on whose album the song appears.

A major challenge in this project comes from the nature of rap lyrics. The texts I am analyzing are full of metaphors, similes, slang and wordplay. That means often times songs can talk about the same topics while using very different language, making it more difficult for the model to recognize similarities.

Cleaning the song lyrics has also been difficult as the lyrics were collected from a website where users submit lyrics. This means lyrics are not all formatted exactly the same. I have spent a lot of time going back and forth between running the model and cleaning the data and revising the preprocessing steps.