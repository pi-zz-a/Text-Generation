# Part of this code is written by Thomas van Tussenbroek and obtained from
# https://github.com/thomasvant/Character-classification/blob/master/transcriptParser.py


import re
from bs4 import BeautifulSoup
import os

scriptPath = os.path.abspath(__file__)  # path to python script
scriptDir = os.path.dirname(os.path.split(scriptPath)[0])  # path to python script dir
transcriptsDir = os.path.join(scriptDir, "Data\\transcripts")  # path to transcripts dir
parsedTranscriptsDir = os.path.join(scriptDir, "Data\\parsedTranscripts")

if not os.path.exists(parsedTranscriptsDir):
    os.makedirs(parsedTranscriptsDir)

parsedEpisodePath = os.path.join(parsedTranscriptsDir, 'allEpisodes.txt')
with open(parsedEpisodePath, 'w', newline='') as txtfile:
    for dir in os.listdir(transcriptsDir):  # for each season
        seasonDir = os.path.join(transcriptsDir, dir)  # path to season dir

        # for each episode in an individual file:
        # parsedSeasonDir = os.path.join(parsedTranscriptsDir, dir)
        # if not os.path.exists(parsedSeasonDir):
        #     os.mkdir(parsedSeasonDir)

        for filename in os.listdir(seasonDir):  # for each episode in season
            episodePath = os.path.join(seasonDir, filename)  # path to episode
            # for each episode in an individual file:
            # parsedEpisodePath = os.path.join(parsedSeasonDir, os.path.splitext(filename)[0] + '.txt')  # path to parsed file

            curFile = open(episodePath)
            soup = BeautifulSoup(curFile, 'html.parser')
            text = soup.getText()
            text = text.splitlines()

            # for each episode in an individual file:
            # with open(parsedEpisodePath, 'w', newline='') as txtfile:

            # fileWriter = csv.writer(txtfile, delimiter=':')
            started = False
            character = ""
            sentence = ""
            output = []

            # Every episode (with some exceptions) start with a scene, indicated within square brackets
            for line in text:
                if not started:
                    start = re.search('\\[.*', line)
                    if start is not None:
                        started = True
                        continue

                if started:
                    line = str(line).replace('\n', ' ')
                    # nonBreakSpace = u'\xa0'
                    # line = line.replace(nonBreakSpace, ' ')
                    line = re.sub(r'[\t\n\v\f\r\xa0\s\u2014]', ' ', line)
                    line = re.sub(r'[^\w?!:,. ]|[À-ú]', '', line)

                    # REMOVE DIRECTIONS
                    line = re.sub(r'\(.*\)?', '', line)  # remove everything between ()
                    line = re.sub(r'\(?.*\)', '', line)  # remove everything between ()
                    # REMOVE SCENE
                    # Sometimes one dialog is split over multiple lines, so there might be only [ or ]
                    line = re.sub(r'\[.*\]?', '', line)  # remove everything between []
                    line = re.sub(r'\[?.*\]', '', line)  # remove everything between []

                    # Separate character from their lines
                    if re.search(':', line) is not None:
                        if not sentence == "" and not character == "":
                            output.append(sentence)
                            output.append("\n\n")
                            txtfile.writelines(output)
                            output = []
                            character, sentence = "", ""
                        character, sentence = line.split(':', 1)
                        if character == "CHAN":
                            character = "CHANDLER"
                        if character == "MNCA":
                            character = "MONICA"
                        if character == "RACH":
                            character = "RACHEL"
                        if character == "PHOE":
                            character = "PHOEBE"
                        # if character == "RACHEL" or character == "CHANDLER" or character == "JOEY" \
                        #         or character == "PHOEBE" or character == "ROSS" or character == "MONICA":
                        output.append(character + ":\n")

                    # If lines belong together but are split over multiple lines, concatenate them
                    else:
                        if sentence == "end":
                            break
                        if not "commercial break" in line.lower():
                            sentence += " " + line
    txtfile.close()
