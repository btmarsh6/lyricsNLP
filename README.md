# Topic Modeling in Rap Lyrics

## Goals
The goal of this project is to apply topic modeling to lyrics from rap albums in order to discover trends in topics. This could be used to group artists who rap about similar content together and discover what trends in topics might exist either across different regions or over time.

## Process:
I started by compiling a list of albums to build my library of songs from. I tried to build this list by thinking of influential or successful rappers from different cities, looking to get a balance between East Coast, West Coast, Midwest and Southern rappers. I also wanted to make sure I was including albums from the 80s through to the present day.

I then used the lyricsgenius API to download a JSON of each album containing the lyrics for each track and other meta-data. From the JSON files, I extracted the lyrics, track titles, album title, artist and release year, then stored that information in a SQL database.

Once I had the lyrics, I did some pre-processing to get them ready to feed into the LDA Model.

## Current Status
Working on preprocessing data to prepare it for LDA topic modeling.

## Challenges and Future Work
This project is currently based primarily on studio albums and occasionally some mixtapes. In the age of music streaming, many artists are now focusing less on putting out full albums and instead just releasing one off songs as singles. These songs are not included in the data unless they also appear on an album.

Additionally, my methodology does not account for features and collaborations. All words from a song are attributed to the artist on whose album the song appears.