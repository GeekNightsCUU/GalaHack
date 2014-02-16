# GalaHack Beta 1
Strategy game based on Galactic Conquest and GalCon, but in the enviroment of Software and Hacking and turn-based.

## Prerequisites
- Python 3.3
- Pygame 1.9

## How to play
Run *galahack.py* with your Python interpreter.
Click on the Title screen to Start the game.

### Controls
In this version, the players share the same screen and mouse.
All actions are performed with a mouse or trackpad.

- If you are playing on a Desktop computer a mouse for each player is recommended.
- Playing on a Laptop, first player could use trackpad and second player could use an external mouse.

First player has blue color, and second one have green color. Blue starts

### Spaces
Every space has a color and a number of units.
Gray colors don't have an owner at that moment. You can conquer them!

You should move the units from your colored spaces to the opponent or gray spaces. Also you can strengthen your spaces moving units from your own spaces.

When you displace units from a space, the half of the units are lost in the space and begin to displace to the destination.
If the arriving units are more than the current units, the space will be conquered by the new units, and the color will change.

### How to win
When a player have no spaces conquered, the game is over.
The player with remaining spaces under control will win the glory.

## Scope for Beta 1
Version 0.1.2
A game where you can play turn-by-turn two players on seat.

## To do (For Beta 2)
- Simple support for networked games
- Add support for up to 4 players
- Replay of games (for debugging mainly)

## Credits and resources
License
http://opensource.org/licenses/MIT

Fonts
http://www.fontsquirrel.com/fonts/exo-2

Backgrounds
http://www.vector-eps.com/index.php/2009/02/digital-background/
http://www.christian-wallpaper.com/preview.asp?id=154