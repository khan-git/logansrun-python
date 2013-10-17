## Kenneth Andersson
## Multimediaprogrammering i Python (DSV)

import os, pygame, shelve, time
from Message import *

class Scores(object):
    """Handle a score database."""
    def __init__(self):
        self.loadScoreList();

    def loadScoreList(self):
        """Load the database."""
        try:
            self.scores = shelve.open("scorelist.dat", "c");
        except IOError:
            print("Error: unable to open/create scorelist.dat");
            sys.exit();

    def saveScoreList(self):
        """Save the database."""
        try:
            self.scores.sync();
        except IOError:
            sys.exit();

    def printScores(self, map):
        """Creates a message sprite with scores of the map.
            Returns a pygame.sprite.GroupSingle"""
        scoreText = ["#   Time    Name        (Level)"];
        sList = self.scores.get(map);
        
        if(sList != None):
            i = 1;
            for score in sList:
                name, playTime, level = score;
                scoreText.append(str.format("{0}   {1}   {2}   ({3})", i, time.strftime("%M:%S", time.localtime(playTime)), name, level));
                i+=1;
        else:
            scoreText = ['No recorded scores'];

        return pygame.sprite.GroupSingle(Message(scoreText, str.format("Scores: {0}", os.path.basename(map[0:-4]))));

    def addScore(self, map, name, playTime, level):
        """Adds a score to the map."""
        if(self.scores.has_key(map) == True):
            sList = self.scores.get(map);
            sList.append((name, playTime, level));
            self.scores[map] = sList;
        else:
            self.scores[map] = [(name, playTime, level)];

        sList = self.scores.get(map);
        sList.sort(lambda x,y:cmp(x[1],y[1]));
        if(len(sList) > 10):
            sList.pop(10);
        self.scores[map] = sList;

