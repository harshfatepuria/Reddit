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
	unique_subreddits = dict()
	user = r.get_redditor(user)
	comments = user.get_comments(limit=None)
	
	len_comments = 0
	for comment in comments:
		len_comments = len_comments + 1
		json_comment = vars(comment)
		subreddit_commented_on = json_comment['subreddit']
		json_subreddit = vars(subreddit_commented_on)
		subreddit_name = str(json_subreddit['display_name'])
		if subreddit_name in unique_subreddits:
			unique_subreddits[subreddit_name] = unique_subreddits[subreddit_name] + 1
		else:
			unique_subreddits[subreddit_name] = 1
	sorted_unique_subreddits = sorted(unique_subreddits.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_unique_subreddits

def get_subreddits_commented_on_by_a_set_of_users(subreddit , list_of_users_tuple):
	generic_subreddit_commented_on_by_all_users = dict()
	i = 1
	number_of_users = len(list_of_users_tuple)
	for user_tuple in list_of_users_tuple:
		username = user_tuple[0]
		list_of_subreddits_tuple = get_comments_by_a_user(username)
		print i,"of",number_of_users,") has commented on",len(list_of_subreddits_tuple),"unique subreddits"
		for subreddit_tuple in list_of_subreddits_tuple:
			subreddit_name = subreddit_tuple[0]
			if subreddit_name in generic_subreddit_commented_on_by_all_users:
				generic_subreddit_commented_on_by_all_users[subreddit_name] = generic_subreddit_commented_on_by_all_users[subreddit_name] + subreddit_tuple[1]
			else:
				generic_subreddit_commented_on_by_all_users[subreddit_name] = subreddit_tuple[1]
		i = i + 1
		if i % 31 == 0:
			output_file=open('subreddits_related_to_' + subreddit + '_' + str(i) + '.txt','w')
			output_file.write(str(generic_subreddit_commented_on_by_all_users))
			output_file.close()
	output_file=open('subreddits_related_to_' + subreddit + '_all.txt','w')
	output_file.write(str(generic_subreddit_commented_on_by_all_users))
	output_file.close()
	


subreddit='marvel'
sorted_authors_of_subreddit = get_authors_of_comments_on_submission_about_subreddit(subreddit)

output_file=open('all_commenters_of_' + subreddit + '.txt','w')
output_file.write(str(sorted_authors_of_subreddit))
output_file.close()

input_file=open('all_commenters_of_' + subreddit + '.txt','r')
sorted_authors_of_subreddit_new=eval(input_file.read())
input_file.close()

get_subreddits_commented_on_by_a_set_of_users(subreddit , sorted_authors_of_subreddit_new)
