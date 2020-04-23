# This code is written by Thomas van Tussenbroek and obtained from
# https://github.com/thomasvant/Character-classification/blob/master/transcriptParser.py


import re
import csv
from bs4 import BeautifulSoup
import os

globalInvalidTags = ['font', 'em', 'i']
lineInvalidTags = ['b']

scriptPath = os.path.abspath(__file__)  # path to python script
scriptDir = os.path.dirname(os.path.split(scriptPath)[0])  # path to python script dir
transcriptsDir = os.path.join(scriptDir, "Data\\transcripts")  # path to transcripts dir
parsedTranscriptsDir = os.path.join(scriptDir, "Data\\parsedTranscripts")

if not os.path.exists(parsedTranscriptsDir):
    os.makedirs(parsedTranscriptsDir)

for dir in os.listdir(transcriptsDir):  # for each season
    seasonDir = os.path.join(transcriptsDir, dir)  # path to season dir

    parsedSeasonDir = os.path.join(parsedTranscriptsDir, dir)
    if not os.path.exists(parsedSeasonDir):
        os.mkdir(parsedSeasonDir)

    for filename in os.listdir(seasonDir):  # for each episode in season
        episodePath = os.path.join(seasonDir, filename)  # path to episode
        parsedEpisodePath = os.path.join(parsedSeasonDir, os.path.splitext(filename)[0] + '.csv')  # path to parsed file

        curFile = open(episodePath)
        soup = BeautifulSoup(curFile, 'html.parser')

        with open(parsedEpisodePath, 'w', newline='') as csvfile:
            fileWriter = csv.writer(csvfile, delimiter='|')
            for tag in globalInvalidTags:
                # remove invalid tags but keep content
                for match in soup.findAll(tag):
                    match.replaceWithChildren()

            for item in soup.select('p'):

                # remove \n, replace strong tags with b tags, remove &nbsp
                item = str(item).replace('\n', ' ').replace('strong>', 'b>').replace('\xa0', '').replace('b>:',
                                                                                                         'b>').replace(
                    ':<', '<')
                characterRegex = re.search('<b>(.*):?( |)</b>',
                                           item)  # obtain only the string between <b> and </b>, due to irregularities in syntax ( |) is added
                lineRegex = re.search('</b>(.*)</p>', item)  # obtain everything between </b> and </p>
                output = []

                if characterRegex is not None and lineRegex is not None:
                    characterString = str(characterRegex.group(1))
                    output.append(characterString)

                    lineRegexSoup = BeautifulSoup(str(lineRegex.group(1)), 'html.parser')
                    for tag in lineInvalidTags:
                        # remove invalid tags but keep content
                        for match in lineRegexSoup.findAll(tag):
                            match.replaceWithChildren()
                    lineNoDirectionsRegex = re.sub(r'\([^\)]*\)', '',
                                                   str(lineRegexSoup))  # remove everything between ()
                    lineNoSceneRegex = re.sub(r'\[[^\]]*\]', '',
                                              str(lineNoDirectionsRegex))  # remove everything between []
                    lineString = str(lineNoSceneRegex)
                    output.append(lineString)

                fileWriter.writerow(output)
                # if characterRegex is not None and lineRegex is not None:
                #     fileWriter.writerow(output)
