from AgentGenerator import make_experiment
from Domains import GridWorldMixed, PolicyMixer
# from Policies import MultiTerrainPolicy, MultiTerrainQPolicy, MAgentMultinomial
from rlpy.Policies import eGreedy
from rlpy.Agents import Q_Learning
from Agents import *
from utils import get_time_str, load_all_agents
import os
import inspect, shutil
import numpy as np
from rlpy.Representations import IncrementalTabular, Tabular
from rlpy.Experiments import Experiment
import logging

mapname = '11x11-Rooms3.txt'

def generate_meta_experiment(exp_id, agent_paths, path, unique=True):
	opt = {}
	if unique:
		opt["path"] = os.path.join(path, get_time_str())
	else:
		opt["path"] = path

	opt["exp_id"] = exp_id
	opt["max_steps"] = 8000
	opt["num_policy_checks"] = 20
	opt["checks_per_policy"] = 40
	# start_at = np.array([4, 6])


	agents = load_all_agents(agent_paths, pretrained=True, load_confidence=True)
	for a in agents:
		a.policy.epsilon = 0

	actual_domain = GridWorldMixed(mapname=mapname, terrain_augmentation=False, noise=0.1)
	domain = PolicyMixer(actual_domain, agents)
	representation = Tabular(domain)
	policy = eGreedy(representation) # , tau=.1)
	# opt['agent'] = Q_Learning(representation=representation, policy=policy, lambda_=0.1,
	# 							discount_factor=0.9)
	opt['agent'] = Q_Learning(policy, representation, discount_factor=0.9, initial_learn_rate=0.8, lambda_=0.5, learn_rate_decay_mode= 'boyan', boyan_N0= 2380)
	opt['domain'] = domain
	experiment = Experiment(**opt)
	
	path_join = lambda s: os.path.join(opt["path"], s)
	if not os.path.exists(opt["path"]):
		os.makedirs(opt["path"])

	shutil.copy(inspect.getsourcefile(inspect.currentframe()), path_join("experiment.py"))

	return experiment

def run_exp_trials(exp_generator, agent_paths, path, num=10, **kwargs):
	for i in range(1, num + 1):
		experiment = exp_generator(i, agent_paths, path, unique=False)
		experiment.run(**kwargs)
		experiment.save()
	return path

if __name__ == '__main__':

	# exp0 = make_experiment("params/gridworld/", yaml_file="agent0.yml", 
	# 						result_path="./Results/Mixed/agent0", save=True) #TODO
	# assert mapname in exp0.domain.mapname, "Not using correct map!"
	# exp0.run(visualize_performance=0)
	# representation = exp0.agent.representation
	# representation.dump_to_directory(exp0.full_path) # TODO


	# result_path1 = "./Results/Mixed/agent1"
	# exp1 = make_experiment("params/gridworld/", yaml_file="agent1.yml", result_path=result_path1, save=True)
	# assert mapname in exp1.domain.mapname, "Not using correct map!"
	# exp1.run(visualize_performance=0)
	# representation = exp1.agent.representation
	# representation.dump_to_directory(exp1.full_path)



	# agent_paths = [exp0.full_path, exp1.full_path]
	# print agent_paths

	agent_paths4 =  ['./Results/Mixed_Actions3/agent0/Aug02_05-53-219522', 
		'./Results/Mixed_Actions3/agent1/Aug02_05-53-805251', 
		'./Results/Mixed_Actions3/agent2/Aug02_05-53-439359', 
		'./Results/Mixed_Actions3/agent3/Aug02_05-53-025208']

	result_path = "./Results/Meta/3agentmaze/"
	# FOR MANY TRIALS
	path = run_exp_trials(generate_meta_experiment, agent_paths4, result_path + get_time_str())
	print path

	# exp = generate_meta_experiment(1, agent_paths4, result_path, unique=True)
	# exp.run(visualize_performance=0, debug_on_sigurg=True)
	# exp.save()
	# exp.plot()
	# import joblib
