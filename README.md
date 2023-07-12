# Topic Modeling in Rap Lyrics

## Goals
The goal of this project is to apply topic modeling to lyrics from rap albums in order to discover trends in topics. This could be used to group artists who rap about similar content together and discover what trends in topics might exist either across different regions or over time.

## Process:
I started by compiling a list of albums to build my library of songs from. I tried to build this list by thinking of influential or successful rappers from different cities, looking to get a balance between East Coast, West Coast, Midwest and Southern rappers. I also wanted to make sure I was including albums from the 80s through to the present day.

I then used the lyricsgenius API to download a JSON of each album containing the lyrics for each track and other meta-data.

Once I had the lyrics, I did some pre-processing to get them ready to feed into the LDA Model.