# Gravity Shift

Gravity Shift is a small puzzle-platformer built with Pygame. You move through each stage by changing the direction of gravity and using a limited number of switches to reach the exit.

## Controls

- `Enter`: start game / continue
- `A` / `D` hold: move
- `A` / `D` tap: switch gravity left / right
- `W` / `S`: switch gravity up / down
- `R`: restart current level
- `Esc`: quit

## Project Layout

- `main.py`: minimal entrypoint
- `gravity_shift/game.py`: game loop, state handling, drawing
- `gravity_shift/player.py`: player movement and collision logic
- `gravity_shift/level.py`: level data model
- `gravity_shift/levels/data.py`: level definitions
- `gravity_shift/settings.py`: shared constants

## Setup

Create a virtual environment, install dependencies, then run the game:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If the virtual environment already exists, you can run it directly:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Notes

- The final level contains the Gravity Core ending sequence.
- Level data is separated from gameplay code to keep the project easier to extend.

## Dev Notes
- You can add levels on your own as well
- Create a PR for levels that you build and i'll include it if i like your level. 

### Just a fun vibe coded game, enjoy and extend levels if you like, might add some more code documentation if i found some time and interest in this project.
