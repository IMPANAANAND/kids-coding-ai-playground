# Kids Coding & AI Playground

A two-game, offline desktop arcade for teaching Python game logic and beginner machine learning. Artwork is drawn with Pygame shapes; there are no downloaded assets, accounts, API keys, or extra programs.

## Run in VS Code

1. Install Python 3.10 or newer from python.org and open this folder in VS Code.
2. In VS Code's integrated terminal, create/select a Python environment if desired, then run `python -m pip install -r requirements.txt`.
3. Start the app with `python main.py`.

The application opens one 1100 × 700 window. Use the HOME button (or Escape) to return to the menu. Pygame's mixer is optional; the app continues without an audio device.

## Games

### Balloon Pop Challenge

Click balloons during the 45-second round. Red, blue, green, and gold award 10, 15, 20, and 50 points. Dark bomb balloons subtract 20. Pause, replay, and return home from the game screen.

The teaching values are near the top of `balloon_game.py`: `BALLOON_SPEED`, `SPAWN_RATE`, `GAME_DURATION`, `RED_POINTS`, `GOLD_POINTS`, and `BOMB_PENALTY`.

### AI Fruit Sorting Robot

Students label eight displayed fruits as apples or oranges. The robot stores their feature vectors and labels, then predicts ten separate test fruits with a standard-Python k-nearest-neighbours classifier (`k=3`) in `ml_model.py`. Its inputs are normalized color and size measurements. Each result shows the guess, answer, score, and final accuracy. “LEARN AI” explains data, training, prediction, and accuracy.

## TEACHER GUIDE

### Python game coding

1. Show that the balloon objects are created and moved by Python every frame.
2. Point to the constants at the top of `balloon_game.py`; they make game rules easy to change.
3. A mouse event checks whether the click is inside a balloon's collision radius.
4. Conditions select the points for the balloon that was clicked.
5. The main loop processes input, updates animations, and draws the next frame.

Try these live changes, then restart a round:

- Change `BALLOON_SPEED` from `95` to `150` to make balloons rise faster.
- Change a color tuple in `BALLOONS` (for example red's `(238, 75, 92)`) to make that balloon a new color.
- Change `RED_POINTS` from `10` to `100` and notice how red balloon clicks affect the score.

### Machine learning

1. The robot starts each training round with no examples.
2. Students click APPLE or ORANGE to attach their labels to the displayed training fruit.
3. Once there are eight labeled examples, the robot is trained from those exact examples.
4. A different set of ten fruits is tested; the classifier finds nearby examples and uses their majority label.
5. Accuracy is calculated from the number of correct predictions. More varied, well-labeled examples can improve the guesses.

For an older group, open `ml_model.py` and explain `knn_predict`: each example is compared with the new fruit, the nearest three vote, and the strongest vote is returned. To see learning affect a result, label several similar-looking examples in a deliberately unhelpful way, complete training, and compare its guesses. Choose different labels for a cluster on the next training run and observe how votes change.

## Checks

Run the included classifier checks with `python -m unittest test_fruit_ai.py`. They cover nearby-example predictions, label-dependent learning, and insufficient training data.
