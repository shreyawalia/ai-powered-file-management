import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'text':"Trent's 2018 Sustainability Plan sets a long-term goal for Trent to move to a low/no carbon campus. The basis of the plan, as it relates to energy, is to strategically work toward eventual campus electrification while balancing costs and emissions in the short term. This means more efficient, and ideally no new, use of natural gas in the short to mid term and a mindful approach that assesses the true cost of projects as Trent moves forward. Project planning will consider the environmental impacts, costs and the replacement cycle of equipment with the intent that all projects will help meet the intent of efficient, environmentally sensitive campus operations. This plan is scheduled for an update in 2019."})

print(r.json())