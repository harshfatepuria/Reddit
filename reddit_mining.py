# -*- coding: utf-8 -*-

__author__ = "Harsh Fatepuria"
__credits__ = "Harsh Fatepuria"
__maintainer__ = "Harsh Fatepuria"
__email__ = "fatepuri@usc.edu"
__status__ = "Developement"

'''
note: needs praw and pprint modules in python installed to work
'''

import praw
import pprint
import operator
pp=pprint.PrettyPrinter(indent=4)

r = praw.Reddit(user_agent='ETC_reddit_mining')

def get_authors_of_comments_on_submission_about_subreddit(subreddit):
	authors = dict()
	submissions = r.get_subreddit(subreddit).get_top_from_year(limit = None)
	i = 0
	for submission in submissions:
		i = i + 1
		try:
			submission.replace_more_comments(limit = None, threshold = 0)
			print "\n\n", i, ") Submission Title: ", vars(submission)['title']
			all_comments = submission.comments

			#storing all comments (with replies to them) using BFS
			for comment in all_comments:
				try:
					json_comment = vars(comment)
					replies_to_comments = json_comment['_replies']
					for reply in replies_to_comments:
						all_comments.append(reply)
				except:
					continue
			len_comments = len(all_comments)

			print "Total # of comments (including recursive replies):", len_comments

			for comment in all_comments:
				try:
					json_comment = vars(comment)

					if json_comment['author']:
						json_author = vars(json_comment['author'])
						author = str(json_author['name'])
						if author in authors:
							authors[author] = authors[author] + 1
						else:
							authors[author] = 1
				except:
					continue
		except:
			continue
		
	sorted_authors = sorted(authors.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_authors

def get_submissions_by_a_user(user):
	user = r.get_redditor(user)
	submissions = user.get_submitted(limit=None)
	print "# submissions by",user,"=",

	len_submissions = 0
	for submission in submissions:
		len_submissions = len_submissions + 1
	print len_submissions

def get_comments_by_a_user(user):
	subreddits = list()
	user = r.get_redditor(user)
	comments = user.get_comments(limit = None)
	
	for comment in comments:
		try:
			json_comment = vars(comment)
			subreddit_commented_on = json_comment['subreddit']
			json_subreddit = vars(subreddit_commented_on)
			subreddit_name = str(json_subreddit['display_name'])
			subreddits.append(subreddit_name)
		except:
			continue
	unique_subreddits = list(set(subreddits))
	return unique_subreddits

def get_subreddits_commented_on_by_a_set_of_users(org_subreddit , list_of_users_tuple):
	generic_subreddit_commented_on_by_all_users = dict()
	i = 1
	number_of_users = len(list_of_users_tuple)
	for user_tuple in list_of_users_tuple:
		username = user_tuple[0]
		list_of_subreddits = get_comments_by_a_user(username)
		print '\n', i, "of", number_of_users, ") has commented on", len(list_of_subreddits), "unique subreddits",
		for subreddit_name in list_of_subreddits:
			if subreddit_name in generic_subreddit_commented_on_by_all_users:
				generic_subreddit_commented_on_by_all_users[subreddit_name] = generic_subreddit_commented_on_by_all_users[subreddit_name] + 1
			else:
				generic_subreddit_commented_on_by_all_users[subreddit_name] = 1
		if i % 20 == 0:
			output_file=open('subreddits_related_to_' + org_subreddit + '_' + str(i) + '.txt','w')
			output_file.write(str(sorted(generic_subreddit_commented_on_by_all_users.items(), key = operator.itemgetter(1), reverse = True)))
			output_file.close()
		i = i + 1
	output_file=open('subreddits_related_to_' + org_subreddit + '_all.txt','w')
	output_file.write(str(sorted(generic_subreddit_commented_on_by_all_users.items(), key = operator.itemgetter(1), reverse = True)))
	output_file.close()
	
input_file=open('subreddits.txt' , 'r')
subreddits=input_file.read().split("\n")

for subreddit in subreddits:
	if subreddit != '':
		try:
			print '\n\n', subreddit
			print '=================='
			sorted_authors_of_subreddit = get_authors_of_comments_on_submission_about_subreddit(subreddit)
			if len(sorted_authors_of_subreddit) > 100:
				sorted_authors_of_subreddit = sorted_authors_of_subreddit[:100]
			output_file=open('top_commenters_of_' + subreddit + '.txt','w')
			output_file.write(str(sorted_authors_of_subreddit))
			output_file.close()

			# input_file=open('top_commenters_of_' + subreddit + '.txt','r')
			# sorted_authors_of_subreddit=eval(input_file.read())
			# input_file.close()

			get_subreddits_commented_on_by_a_set_of_users(subreddit , sorted_authors_of_subreddit)
		except:
			continue
			