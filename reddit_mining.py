import praw
import pprint
import operator
pp=pprint.PrettyPrinter(indent=4)

r = praw.Reddit(user_agent='new_application_crawler_reddit')

def get_authors_of_comments_on_submission_about_subreddit(subreddit):
	authors = dict()
	len_submissions = 50
	submissions = r.get_subreddit(subreddit).get_top(limit = len_submissions)
	i = 1
	for submission in submissions:
		submission.replace_more_comments(limit=None, threshold=0)
		print "\n\n",i,") Submission Title: ",vars(submission)['title']
		all_comments = submission.comments

		#storing all comments (with replies to them) using BFS
		for comment in all_comments:
			json_comment = vars(comment)
			replies_to_comments = json_comment['_replies']
			for reply in replies_to_comments:
				all_comments.append(reply)
		len_comments = len(all_comments)

		print "Total # of comments (including recursive replies):",len_comments

		for comment in all_comments:
			json_comment = vars(comment)
			json_author = vars(json_comment['author'])
			author = str(json_author['name'])
			if author in authors:
				authors[author] = authors[author] + 1
			else:
				authors[author] = 1
		i = i + 1
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
	user = r.get_redditor(user)
	comments = user.get_comments(limit=None)
	print "# comments by",user,"=",
	
	len_comments = 0
	for comment in comments:
		len_comments = len_comments + 1
	print len_comments


sorted_authors_of_subreddit = get_authors_of_comments_on_submission_about_subreddit('marvel')
pp.pprint(sorted_authors_of_subreddit)
get_submissions_by_a_user(sorted_authors_of_subreddit[0][0])
get_comments_by_a_user(sorted_authors_of_subreddit[0][0])