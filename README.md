# `elosort`
## A simple python tool to sort files by Elo Ranking

`elosort` lets you sort your photos by quality, based on 'a or b' preference questions.

## The idea

The [Elo rating system](http://en.wikipedia.org/wiki/Elo_rating_system) was developed to rate chess players. The players' scores are adjusted with each game, depending on both the outcome of the game and the relative ratings of the players.

`elosort` applies this algorithm to a set of files (only image files are currently supported) on you hard drive.

## Usage

Run `elosort.py` in the directory with the photos, and then point your browser at `http://localhost:8080`. Click the image you prefer (or press the left or right arrow key). The vote is registered, and a new pair of images will appear.

## Notes

This is pre-alpha software, i.e. unfinished and unfit for use. For example, the system records competitions and calculates Elo Ratings, but right now there's no visualisation so if you want to see the ratings you have to look in the database yourself.

Do not expect this to work unless you are me, or a close approximation.

