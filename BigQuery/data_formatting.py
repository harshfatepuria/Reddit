import pprint
import glob, os
import json
pp=pprint.PrettyPrinter(indent=4)
os.chdir("/Users/harshfatepuria/Desktop/ETC_Internship/BIG_QUERY_RESULTS")
unique_subreddit=list()
graph_data=dict()
graph_data["maxVal"]=999
graph_data["links"]=list()
graph_data["nodes"]=list()

for file in glob.glob("*.json"):
	input_file=open(file,'r')

	inp=input_file.read()
	input_file.close()

	inp=inp.split("\n")
	for entry in inp:
		unique_subreddit.append(str(eval(entry)['related_subreddit']))
unique_subreddit=sorted(list(set(unique_subreddit)))


i=0
for subreddit in unique_subreddit:
	node_dict=dict()
	node_dict["id"]=i
	node_dict["count"]=50
	node_dict["name"]=subreddit
	graph_data["nodes"].append(node_dict)
	i=i+1


for file in glob.glob("*.json"):
	input_file=open(file,'r')
	inp=input_file.read()
	input_file.close()

	inp=inp.split("\n")
	inp=inp[1:]
	sourceIndex=[i for i,x in enumerate(unique_subreddit) if x == str(eval(inp[0])['query_subreddit'])][0]
	j=0
	for nodes in graph_data["nodes"]:
		if nodes["id"]==sourceIndex:
			graph_data["nodes"][j]["count"]=400
			break
		j=j+1
	for entry in inp:
		link_dict=dict()
		json_data=eval(entry)
		dest=[i for i,x in enumerate(unique_subreddit) if x == str(json_data['related_subreddit'])][0]
		link_dict["source"]=dest
		link_dict["target"]=sourceIndex

		# temp_link_dict=dict()
		# temp_link_dict["source"]=sourceIndex
		# temp_link_dict["target"]=dest
		# if temp_link_dict not in graph_data["links"]:
		graph_data["links"].append(link_dict)
		
with open('/Users/harshfatepuria/Desktop/ETC_Internship/BIG_QUERY_RESULTS/Visualization/js/subreddit_data.json', 'w') as outfile:
    json.dump(graph_data, outfile)

# pp.pprint(graph_data)