# very cool clipper, thanks

This is just an audio threshold autoclipper which exclusively checks track 1.
I made it so I wouldn't have to manually sift through 30-50 hours of workout videos monthly.

If you find it useful, great!
I will more than likely not consider PRs or update this ever.
Feel free to fork.

Requires MoviePy, and requires you to have Local scripting enabled and DaVinci Resolve in your PYTHON_PATH.

No .env or settings conf, just modify the variables at the top of script.py.

## Usage

While DaVinci resolve is open, and the movie clips you want to chop are in your Media Pool:

`python script.py`

That's it. 