import pdb
import json

from selenium import webdriver
from bs4 import BeautifulSoup
from sys import argv
from time import sleep


activity_url = 'https://www.quora.com/topic/Tourism'

# open with chromedriver
browser = webdriver.Chrome()
browser.get(activity_url)


# process via beautifulsoup
skip = 0
results = []
try:
	while True:
		# Get html so far
		html = browser.page_source

		# scroll to bottom of page
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# process html, skipping already processed results
		soup = BeautifulSoup(html, 'html.parser')
		elems_so_far = soup.findAll("div", {"class": "feed_type_answer"})

		for idx in range(skip, len(elems_so_far)):
			elem = elems_so_far[idx]


			# link to question
			question_link = elem.find('a', attrs={'class': 'question_link'}).get('href', None)

			# answer text
			answer_elems = elem.find('div', attrs={'class': 'answer_body_preview'}).find('p', attrs={'class': 'qtext_para'})
			
			# questions without answer text
			if answer_elems is None:
				continue

			answer_elems = answer_elems.parent
			answer_text = ' '.join([a_elem.get_text() for a_elem in answer_elems])

			# question text
			question_element = elem.find('span', attrs={'class': 'rendered_qtext'})
			question_text = question_element.get_text()

			results.append({'question': question_text, 'answer': answer_text, 'url': f'https://www.quora.com{question_link}'})

		sleep(5)
		skip = len(elems_so_far)
except KeyboardInterrupt:
	print('buh bye')
except e:
	print(e)

with open('output.txt', 'w') as outfile:
	json.dump(results, outfile)
browser.quit()