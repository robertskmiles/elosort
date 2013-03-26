# `elosort`
## A simple python tool to sort files by Elo Rating

`elosort` lets you sort your photos by quality, based on 'a or b' preference questions.

## The idea

The [Elo rating system](http://en.wikipedia.org/wiki/Elo_rating_system) was developed to rate chess players. The players' scores are adjusted with each game, depending on both the outcome of the game and the relative ratings of the players.

`elosort` applies this algorithm to a set of files (only image files are currently supported) on you hard drive.

## Usage

Run `elosort.py` in the directory with the photos, and then point your browser at `http://localhost:8080`. Click the image you prefer (or press the left or right arrow key). The vote is registered, and a new pair of images will appear. After you've done some voting, you can look at the rankings at the `http://localhost:8080/results` page.

Run `elosort.py --help` to get information about command-line options.

## Notes

This is pre-alpha software, i.e. unfinished and unfit for normal use. Expect problems, and please do report any bugs you find.

