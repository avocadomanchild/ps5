# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:
# -*- coding: utf-8 -*-
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
#import datetim
import pytz

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================
punctuations = (string.punctuation)

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

def strip_phrase(phrase): 
    
    new_message = ""
    for letters in phrase: 
        if letters not in punctuations: 
            new_message = new_message + letters 
        else: 
            new_message = new_message + " "
    #print(new_message)
    newer_m = new_message.lower().split()
    return (newer_m)  




#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
class NewsStory(Trigger): 
    def __init__(self, guid, titles, description, link, pubdate):
        self.news_guid = guid
        self.news_title = titles 
        self.news_description = description 
        self.news_link = link 
        self.news_pubdate = pubdate 
    
    def get_guid(self): 
        return self.news_guid
    def get_title(self): 
        return self.news_title
    def get_description(self): 
        return self.news_description
    def get_link(self): 
        return self.news_link
    def get_pubdate(self):
        return self.news_pubdate 
    
class PhraseTrigger(Trigger): 
    def __init__(self, phrase):
        Trigger.__init__(self)
    
        try: 
            self.phrase = phrase
        except: 
            print("User input must be a string of words ex,'this is a string'")


    def get_phrase(self): 
        return self.phrase

    def is_phrase_in(self,input_phrase):

        phrases = self.get_phrase()
        correctedstring = " ".join(phrases.split())
        for punc in punctuations: # this checks if the object that was created has punctuation
            if punc in phrases: 
                return str("Punctuation cannot be in object phrase, please make a new object")
            else:
                pass
         
        if phrases == correctedstring: # this checks if your phrase has whitespace
            new_phrase = phrases.lower().split()  # this is the phrase object that you created 
            #print(new_phrase)
            try:
                user_phrase = strip_phrase(input_phrase)  # this is the phrase that you want to check if it has the same phrase 
                #print(user_phrase)
                y = 0                                     # counter 
                x2 = len(new_phrase)                      # allows you to check if your counter is equal to new_phrase
                for i in range(len(new_phrase)):          # for loop through the index of new phrase 
                        if y == x2:
                            break
                        else:
                            for j in range(len(user_phrase)):  # nested for loop through the user_phrase 
                                if new_phrase[i] == user_phrase[j]: 
                                    y += 1
                                    for k in range(1,len(new_phrase)): # again for looping throught the new phrase to check what is after the first success 
                                        try:
                                            if new_phrase[i+k] == user_phrase[j+k]:
                                                y += 1
                                                if y == x2:
                                                    return True
                                        except IndexError:
                                            return False 
                return False # one more False statment if you finish looping the values dont match up 

            except:
                return("Input must be a string")

        else:
            return str("Cannot have multiple whitespaces.")

# cuddly  = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
# print(cuddly.get_title())
# x = PhraseTrigger('Purple cow',"","The purple cow is soft and cuddly.","","","")
# print(x.get_phrase())
# print(x.is_phrase_in())
        


# test_message = PhraseTrigger("PURPLE COW")
# #print(test_message.get_phrase())
# print(test_message.is_phrase_in('The purple cow tree is soft and cuddly.'))

# # PHRASE TRIGGERS

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger): # cotains the attributes of Phrase 
    def evaluate(self, story):     # also contains the attributeds of  trigger which allows you to pass the test cause you want to return the TRUE OR FALSE INTO THE function 
        return self.is_phrase_in(story.get_title())

    # def __str__(self):
    #     return str(f'TitleTrigger("{self.phrase}")')


class DescriptionTrigger(PhraseTrigger): 

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
    
    def __str__(self):
        return str(f'DescriptionTrigger("{self.phrase}")')
       

# test_message = TitleTrigger("robinhood")
# print(test_message)
# # print(test_message.get_title())
# print(test_message.is_phrase_in('The purple cow is soft and cuddly.'))


class TimeTrigger(Trigger):

    def __init__(self, input_datetime):
        self.datetime = input_datetime
        try: # this error handeling to get the correct string input 
            datetime.strptime(self.datetime, '%d %b %Y %H:%M:%S')
            
            #print("true")
        except ValueError:
            print("Incorrect data format, should be '%d %b %Y %H:%M:%S")

    
    def get_datetime(self):
        format = "%d %b %Y %H:%M:%S"
        datetime_str = datetime.strptime(self.datetime, format) # this function converts to a datetime object

        return datetime_str
        
    def convert_datetime(self,object_datetime): 
        #input_datetime = self.get_datetime()
        format = "%d %b %Y %H:%M:%S"
        datetime_str = datetime.strptime(object_datetime, format) # this function converts to a datetime object

        return datetime_str
    
    def Check_Datetime_Before(self,input_datetime): 
        x = self.get_datetime()
        y = input_datetime
        dt = y.replace(tzinfo=None)
        if x > dt : 
            return True 
        else: 
            return False
    
    def Check_Datetime_After(self,input_datetime): 
        x = self.get_datetime()
        y = input_datetime
        dt = y.replace(tzinfo=None) # this takes the time zone away and compares the datetimes 
        if x > dt : 
            return False
        else: 
            return True

    
# time = TimeTrigger("3 Oct 2016 17:00:10")
# print(time.get_datetime())
    
class BeforeTrigger(TimeTrigger): 
    def evaluate(self,story): 
        return self.Check_Datetime_Before(story.news_pubdate)

class AfterTrigger(TimeTrigger):
    def evaluate(self,story): 
        return self.Check_Datetime_After(story.news_pubdate)



# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, not_trigger):
        self.not_trigger = not_trigger 
        Trigger.__init__(self)
    def evaluate(self, story):
        return not self.not_trigger.evaluate(story)


class AndTrigger(Trigger): 
    def __init__(self, and_trigger1, and_trigger2): 
        self.and_trigger1 = and_trigger1
        self.and_trigger2 = and_trigger2
        Trigger.__init__(self)
    def evaluate(self, story):
        return self.and_trigger1.evaluate(story) and self.and_trigger2.evaluate(story)

class OrTrigger(Trigger): 
    def __init__(self, and_trigger1, and_trigger2): 
        self.and_trigger1 = and_trigger1
        self.and_trigger2 = and_trigger2
        Trigger.__init__(self)
    def evaluate(self, story):
        return self.and_trigger1.evaluate(story) or self.and_trigger2.evaluate(story)


t1 = TitleTrigger("robinhood")
t2 = DescriptionTrigger("stocks")
x = AndTrigger(t1,t2)
print(x)
    




# Problem 8
# TODO: AndTrigger

# Problem 9
# TODO: OrTrigger


#======================
# Filtering
#======================

# Problem 10

# s1 = TitleTrigger('PURPLE COW')
# cuddly = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
# print(s1.evaluate(cuddly))


def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    
    stories1 = [] 
    for triggers in triggerlist: 
        for news in stories:
            #print(triggers.evaluate(news)) 
            if triggers.evaluate(news) == True:
                stories1.append(news)
            else: 
                pass 
    #print(news)

    
    
   
   
    return stories1



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    #print(lines) 

    # TODO: Problem 11
    # to build triggers
    lists= ['t1,TITLE,robinhood','t2,DESCRIPTION,STOCKS','t3,DESCRIPTION,investors','t4,AND,t2,t3',"ADD,t1,t4"]
    dictnews = {"TITLE" : TitleTrigger, "DESCRIPTION" : DescriptionTrigger, "AFTER" : AfterTrigger, "BEFORE": BeforeTrigger, "NOT": NotTrigger, "Or" : OrTrigger, "AND" : AndTrigger}
    dict2 = {} 
    for i in lists: 
        x = list(i.split(","))
        for j in range(len(x)): 
            if x[j] in dictnews:
                for chars,y in dictnews.items():
                    #print(chars)
                    try: 
                        if x[j] == chars:
                                dict2[x[0]] =y(x[2])
                                #print("here")
                        else: 
                            pass
                    except TypeError:
                        if x[j] == chars:
                                dict2[x[0]] =y(x[2],x[3])
                        else: 
                            pass
                        # dict3 = {}
                        # #print(dict2)
                        # for j in range(len(x)):
                        #     for chars,y in dict2.items():
                        #         #
                        #         if chars == x[j]:
                        #             dict3[chars] = y 
                        #         else :
                        #             pass
                        #     print("this is dict3")
                        #     print( dict3)
                        
                        # dict2[x[0]] =y(list(dict3.keys()[0]),list(dict3.keys()[1]))
                        #         #x1.clear()
                                
    #print(dict3)
    print(dict2)
    newlist = []
    for i in lists:
        x = list(i.split(","))
        for j in range(len(x)): 
            if x[j] == "ADD" or "OR":
                return (x[j+1:])
    
                


        
   




print(read_trigger_config('triggers.txt'))

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the titles to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("robinhood")
        t2 = DescriptionTrigger("stocks")
        t3 = DescriptionTrigger("investors")
        t4 = AndTrigger(t2, t3)
        #print(type(t1))
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        #triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

