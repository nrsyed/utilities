# Utilities

This repo is a collection of general purpose utilities I've created to
address various issues large and small—mostly small. Brief descriptions
follow.

## ordinal

* **C++**: [ordinal.cpp](ordinal/ordinal.cpp)
* **Python**: [ordinal.py](ordinal/ordinal.py)

Simple functions that return the ordinal suffix of an integer (e.g., the "st"
in "1st" or the "rd" in "23rd") given an integer or a string representing
an integer.

## reddit_pages

[reddit_pages.py](reddit_pages/reddit_pages.py)

Simple BeautifulSoup-based scraper that returns a list of all available
page URLs of a subreddit for a selected category ("hot", "new", etc.), so you
don't have to click "Next" several dozen times to get to the last page.

## spring

[spring.py](spring/spring.py)

A Python function that returns the (x, y) coordinates needed to draw a
sawtooth-shaped spring between any two points in 2D space. The spring width
("diameter") and the number of spring coils can be chosen.

See [spring/README.md](spring/README.md) for more information.

## tracktime

[tracktime.py](tracktime/tracktime.py)

A simple command line time tracking utility. Not fully functional. This was
the precursor to Krono Tracker.

## unique colors

[uniquecolors.py](uniquecolors/uniquecolors.py)

A generator function that returns N unique colors in the form of RGB,
HSV, or HLS 3-tuples.
