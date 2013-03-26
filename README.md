# `elosort`
## A simple python tool to sort files by Elo Rating

`elosort` lets you sort your photos by quality, based on 'a or b' preference questions.

## The idea

The [Elo rating system](http://en.wikipedia.org/wiki/Elo_rating_system) was developed to rate chess players. The players' scores are adjusted with each game, depending on both the outcome of the game and the relative ratings of the players.

`elosort` applies this algorithm to a set of files (only image files are currently supported) on you hard drive.

## Prerequisites

- Python (written for version 2.7)
- [CherryPy](http://cherrypy.org/)

## Usage

Run `elosort` in the directory with the photos, and then point your browser at `http://localhost:8080`. Click the image you prefer (or press the left or right arrow key). The vote is registered, and a new pair of images will appear. After you've done some voting, you can look at the rankings at the `http://localhost:8080/results` page.

Run `elosort --help` to get information about command-line options.

## Notes

This is pre-alpha software, i.e. unfinished and unfit for normal use. Expect problems, and please be sure to report any bugs you find.

It's also appallingly inefficient software right now, particularly in the hashing and database handling, but this is actually all a cunning ruse: The plan is that someone will read the source and be unable to resist correcting it, thus giving me an opportunity to learn about collaborating with strangers over GitHub.