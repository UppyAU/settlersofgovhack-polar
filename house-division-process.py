#!/usr/bin/env python

from datetime import date
import json
from itertools import combinations
import networkx as nx

# Split the graphs into years
for y in range(2006, 2016):
  divisions = []
  for m in range(1, 13):
    f = 'house-' + str(m) + '-' + str(y) + '.json'
    print "FILE: " + f
    try:
      divlist = json.loads(open(f).read())
      divisions.extend(divlist)
    except:
      pass

  # We now have a list of divisions
  # Load each division into another object
  div_detail = {}
  reps = set()
  colours = {}
  roll_calls = []
  for d in divisions:
    print "Processing division " + str(d['id'])
    div = json.loads(open('divisions/house-div-' + str(d['id']) + '.json').read())
    div_detail[d['id']] = div
    # Compile the list of reps for this year too
    r = []
    roll_call = {}
    for v in div['votes']:
      # Get the name of the senator
      name = v['member']['first_name'] + ' ' + v['member']['last_name'] + ' (' + v['member']['party'] + ')'
      r.append(name)
      # Update the party of the rep (what colour it will appear on the graph
      if v['member']['party'] == 'Australian Labor Party':
        colours[name] = "red"
      elif v['member']['party'] == 'Liberal Party':
        colours[name] = "blue"
      elif v['member']['party'] == 'National Party':
        colours[name] = "yellow"
      elif v['member']['party'] == 'Australian Greens':
        colours[name] = 'green'
      else:
        colours[name] = "black"
      
      if v['vote'] not in roll_call:
        roll_call[v['vote']] = []
      roll_call[v['vote']].append(name)
    reps.update(r)
    roll_calls.append(roll_call)
  
  # Create the graph
  graph = nx.Graph()
  all_rep_pairs = combinations(reps, 2)
  common_votes = {}
  
  # Create the edges
  for pair in all_rep_pairs:
    common_votes[pair] = 0
  
  for vote in roll_calls:
    if 'aye' in vote:
      aye_pairs = combinations(vote['aye'], 2)
      for pair in aye_pairs:
        try:
          common_votes[pair] += 1
        except KeyError:
          # flip the combination so we can find a common pair in the common_votes
          common_votes[(pair[1], pair[0])] += 1
    
    if 'no' in vote:
      no_pairs = combinations(vote['no'], 2)
      for pair in no_pairs:
        try:
          common_votes[pair] += 1
        except KeyError:
          # flip to find a common pair in common_votes
          common_votes[(pair[1], pair[0])] += 1
  
  js = {}
  js['nodes'] = []
  js['links'] = []
  
  # we need an array of reps not a set
  rep_list = []
  # Create the nodes and give them a colour
  for rep in reps:
    graph.add_node(rep, color=colours[rep])
    n = { 'name': rep, 'colour': colours[rep] }
    js['nodes'].append(n)
    rep_list.append(rep)
    
  
  # Add the edges
  for pair in common_votes:
    if common_votes[pair] == 0:
      continue
    graph.add_edge(pair[0], pair[1], weight=common_votes[pair], difference=1.0/common_votes[pair])
    l = { 'source': rep_list.index(pair[0]), 'target': rep_list.index(pair[1]), 'value': common_votes[pair] }
    js['links'].append(l)
  
  # Save the graph
  nx.write_gexf(graph, 'house-graph-' + str(y) + '.gexf')
  with open('../../static/house-'+str(y)+'.json', 'w') as of:
    json.dump(js, of)

