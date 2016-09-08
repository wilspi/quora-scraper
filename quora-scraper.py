#!/usr/bin/python

from selenium import webdriver
from bs4 import BeautifulSoup
from sys import argv


print "\n\n\033[1m\033[4mQUORA : UPVOTED QUESTION-ANSWER\033[0m"
print "###############################\n"

# if username passed as argument
try:
	quora_id = argv[1]
	print "\033[1mScraping\033[0m https://www.quora.com/profile/\033[4m"+quora_id+"\033[0m/activity/"
except IndexError:
	quora_id = raw_input("Enter your \033[1mQuora\033[0m username\n(Example: https://www.quora.com/profile/\033[4m<username>\033[0m/activity): ")

activity_url = 'https://www.quora.com/profile/'+quora_id+'/activity'
print "###############################\n"

# open with chromedriver
browser = webdriver.Chrome()
browser.get(activity_url)
html = browser.page_source
browser.quit()

# process via beautifulsoup
soup = BeautifulSoup(html, 'html.parser')
for foo in soup.findAll("div", {"class": "feed_type_answer"}):
	
	# upvoted answer link
	link_element = foo.find('span', attrs={'class': 'timestamp'})
	upvoted_answer_link = link_element.find('a').get('href', None)
	
	# question text
	question_element = foo.find('span', attrs={'class': 'rendered_qtext'})
	question_text = question_element.get_text()

	print "\033[1mQuestion:\033[0m \033[1m" + question_text + "\033[0m"
	print "\033[1mLink:\033[0m https://www.quora.com" + upvoted_answer_link
	print "-------------------------------\n"
