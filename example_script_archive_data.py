import json
from collections import defaultdict
import networkx as nx
data_path = '/mnt/md1/data/reddit/reddit_data/2009/RC_2009-06'

with open(data_path) as f:
    fdata = f.readlines()

data = [json.loads(elem) for elem in fdata]

user_comment =defaultdict(list)
user_attributes = defaultdict(list)
user_parent_id =defaultdict(list)
comment_parent_id =defaultdict(list)
comment_user =defaultdict(list)
comment_comment = defaultdict(list)
target_comment_comment = defaultdict(list)
iter_i = 0
target_subreddit = 'AskReddit'
for elem in data:
    if iter_i % 1000 == 0:
        print iter_i
    iter_i +=1
    author = elem['author']
    id = elem['id']
    parent_id = elem['parent_id'].split('_')[-1]
    if elem['subreddit'] == target_subreddit:
        target_comment_comment[id].append(parent_id)
    comment_comment[id].append(parent_id)
    user_comment[author].append(id)
    user_attributes[author].append(elem['subreddit'])
    user_parent_id[author].append(parent_id)
    comment_user[id].append(author)
    comment_parent_id[id].append(parent_id)


# user attributed should be derived from data[541231]['subreddit']
user_dict = defaultdict(list)
for user in user_comment.keys():
    connected_users = []
    for comment in user_parent_id[user]:
        connected_users.append(comment_user[comment])
    a = [elem[0] for elem in connected_users if len(elem) == 1]
    a = [elem for elem in a if elem !='[deleted]']
    user_dict[user] = a
user_dict.pop('[deleted]')

graph = nx.from_dict_of_lists(user_dict)
nx.write_gexf(graph,'aux_graph.gexf')

graph = nx.from_dict_of_lists(target_comment_comment)
nx.write_gexf(graph,'aux_graph_cc.gexf')

#
# def evaluate(attributes,node,target_value=['politics']):
#     for elem in target_value:
#         if elem in attributes[node]:
#             return 1.0
#     return 0.0
#
# def neighbors(graph,node):
#     return graph[node].keys()
#
# def ego(graph,node):
#     return nx.ego_graph(graph, node)
#
# evaluate(user_attributes,user_attributes.keys()[20])
#
# cost_eval = 1.0
# cost_neighbor = 0.4
# cost_ego = 1.5
# value_finding = 10.0
#
# def strategy(known_graph,known_attributes,nodes_evaluated,nodes_visible,edges_visible):
#     return
#
# POSITIVE_PART = sum([value_finding * evaluate(attributes,node) for node in nodes_evaluted])
# NEGATIVE_PART = cost_eval * len(nodes_evaluated) + cost_neighbor * len(nodes_neighbor) + cost_ego * len(nodes_ego)
#
# strategy_value = POSITIVE_PART - NEGATIVE_PART
