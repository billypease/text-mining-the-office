
# coding: utf-8

# In[3]:

import re
import csv
import urllib2
import operator
from os import path
import collections
import BeautifulSoup
from wordcloud import WordCloud
from stop_words import get_stop_words

# Style guide: https://google.github.io/styleguide/pyguide.html
# TODO(billypease@gmail.com): close open files (contextlib) or open "with"
# TODO(billypease@gmail.com): make Stop Words its own function
# TODO(billypease@gmail.com): run pylint over the code for formatting and bugs
# TODO(billypease@gmail.com): implement Log Likelihood to Identify Characteristic Words
# TODO(billypease@gmail.com): implement word counts and curse word counts per episode


def get_page_text(url):
    print "Getting text from... " + url
    # given a url, get page content
    data = urllib2.urlopen(url).read() 
    # parse as html structured document
    bs = BeautifulSoup.BeautifulSoup(data, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    # find character quotes (e.g. <div class="quote">) and extract text
    txt = bs.findAll(attrs={"class": "quote"})
    #txt = txt[0]
    return txt


def remove_noise(transcript):
    # clean transcript; lower case it, remove tags and punctuation
    noise = {'<br />': '', '<div class="quote">': '', '<b>': '', '</b>': '', 
                '</div>': '', '[': '', ']': '', '.': '', '?': '', ',': '',
                '!': '', '"': '', '<u>': '', '</u>': '', '<div class="spacer">': '',
                'deleted scene': '', "'": ''}
    cleanedt = str(transcript).lower()
    for x,y in noise.items():
        cleanedt = cleanedt.replace(x, y)
    return cleanedt


def print_to_text_file(txt, filename):
    # write text to a specified file
    text_file = open(filename, "w")
    text_file.write(txt)
    text_file.close()
    return


def print_user_lines_to_file(source_file, out_file, tv_character_name):
    with open(out_file, 'a') as f1:
        for line in open(source_file):
            if line.startswith(tv_character_name): f1.write(line)
    return


def character_word_analysis(t_out_file, t_count_file, main_character):
    # count words in tv character's transcript file
    words = collections.Counter()    
    char_transcript = open(t_out_file)
    for line in char_transcript:
        words.update(line.split())
    # store character's word counts in a CSV file
    word_count_file = open(t_count_file, 'w')
    writer = csv.writer(word_count_file)
    for word, count in words.iteritems():
        # don't count starting word name: (e.g. "pam:", "jim:", etc.)
        if word != main_character + ':':
            # CSV row: tv character name, word, count
            writer.writerow([main_character, word, count])
    return


def sum_word_count(count_file, subject):
    cr = csv.reader(open(count_file,"rb"))
    total_count = sum(int(x[2]) for x in cr)
    #print '%s | %d' % (subject, total_count)
    return


def sum_curse_word_count(count_file, subject):
    bad_words = {'damn', 'bitch', 'ass', 'hell', 'shit', 'whore'}
    curse_count = 0
    cr2 = csv.reader(open(count_file,"rb"))
    for y in cr2:
        if str(y[1]) in bad_words:
            curse_count = curse_count + int(y[2])
    print '%s | %d' % (subject, curse_count)
    return


def make_cloud_tag(text):
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)
    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(background_color='white', width=600, height = 400, 
                          max_font_size=60, relative_scaling=.5).generate(text)
    # display image the pil way
    image = wordcloud.to_image()
    image.show()
    return

    
def main():
    
    # The Office's main characters
    main_characters = [
        'michael', 'pam', 'jim', 'andy', 'dwight', 'jan', 'ryan', 'oscar', 'stanley',
        'kelly', 'toby', 'darryl', 'gabe', 'angela', 'robert', 'erin', 'holly',
        'phyllis', 'meredith', 'pete', 'roy', 'creed', 'clark', 'charles',
        'documentary crew member'
    ]

    # get the URLs to scrape
    with open("urls-for-testing.txt") as f:
    #with open("urls.txt") as f:
        urls = f.readlines()
    transcript = [get_page_text(url) for url in urls]
    
    # clean transcript string of noise
    cleaned_transcript = remove_noise(transcript)
    
    # remove Stop Words from cleaned_transcipt with regex
    stop_words = get_stop_words('en')    
    pattern = re.compile(r'\b(' + r'|'.join(stop_words) + r')\b\s*')
    cleaned_transcript = pattern.sub('', cleaned_transcript)
    
    # make a Cloud Tag from characters transcript
    make_cloud_tag(cleaned_transcript)
    
    # print cleaned trancript string to text file
    print_to_text_file(cleaned_transcript, "the_office_transcripts.txt")
    
    # count each word in transcript; store counts in all_count.csv
    character_word_analysis('the_office_transcripts.txt', 'all_count.csv', 'all')
    
    # sum the number of words in all_count.csv
    sum_word_count('all_count.csv', 'all')
    
    # get each of the main characters lines in the transcript
    for main_character in main_characters:
        # one txt file for transcript; one CSV file for word count
        t_out_file = main_character + ".txt"
        t_count_file = main_character + "_count.csv"
        
        # tv character lines start with a :[name] (e.g. "michael:")
        characters_line = main_character + ":"
        
        # get lines for main TV characters and write them to their own txt file
        print_user_lines_to_file("the_office_transcripts.txt", t_out_file, characters_line)

        # count each word for each TV character's transcript from txt file
        character_word_analysis(t_out_file, t_count_file, main_character)
        
        # sum number of words each TV character said from CSV file
        sum_word_count(t_count_file, main_character)
        
        sum_curse_word_count(t_count_file, main_character)
        
    print 'Done!'
    

if __name__=="__main__":
    main()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



