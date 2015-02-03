#!/usr/bin/env python

import argparse
from sys import exit
from os import path


# TODO: Move configuration to a separate file
profiles = {
	'l2' : {
		'128k':  {'size':  128, 'tags': 1, 'data': 2},
		'256k':  {'size':  256, 'tags': 1, 'data': 3},
		'512k':  {'size':  512, 'tags': 1, 'data': 3},
		'1024k': {'size': 1024, 'tags': 1, 'data': 3},
	},
	'l3' : {
		'4M':  {'size':  4*1024, 'tags': 2, 'data': 6},
		'8M':  {'size':  8*1024, 'tags': 3, 'data': 7},
		'16M': {'size': 16*1024, 'tags': 3, 'data': 9},
		'32M': {'size': 32*1024, 'tags': 3, 'data': 10},
	},
	'replacement': {
		'lru': {'policy': 'lru'},
		'tadip': {'policy': 'tadip'},
		'ucp': {'policy': 'ucp'},
		'pipp': {'policy': 'pipp'},
		'drrip': {'policy': 'drrip'},
	},

	'core': {
		'default' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 8},

		'rob-1' : {'rob': 96, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 8},
		'rob-2' : {'rob': 160, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 8},
		'rob-3' : {'rob': 192, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 8},
		'rob-4' : {'rob': 224, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 8},

		'rs-1' : {'rob': 128, 'rs': 28, 'ol': 48, 'os': 32, 'mshr': 8},
		'rs-2' : {'rob': 128, 'rs': 36, 'ol': 48, 'os': 32, 'mshr': 8},
		'rs-3' : {'rob': 128, 'rs': 40, 'ol': 48, 'os': 32, 'mshr': 8},
		'rs-4' : {'rob': 128, 'rs': 48, 'ol': 48, 'os': 32, 'mshr': 8},

		'ol-1' : {'rob': 128, 'rs': 32, 'ol': 40, 'os': 32, 'mshr': 8},
		'ol-2' : {'rob': 128, 'rs': 32, 'ol': 52, 'os': 32, 'mshr': 8},
		'ol-3' : {'rob': 128, 'rs': 32, 'ol': 56, 'os': 32, 'mshr': 8},

		'os-1' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 26, 'mshr': 8},
		'os-2' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 36, 'mshr': 8},
		'os-3' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 40, 'mshr': 8},

		'mshr-1' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 6},
		'mshr-2' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 10},
		'mshr-3' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 12},
		'mshr-4' : {'rob': 128, 'rs': 32, 'ol': 48, 'os': 32, 'mshr': 14},
	}
}

if __name__ == '__main__':	

	parser = argparse.ArgumentParser(description="Build a experiment script")

	# Add profile choices
	parser.add_argument('--l2-profile', choices=profiles['l2'].keys(), default=['256k'], nargs='*')
	parser.add_argument('--l3-profile', choices=profiles['l3'].keys(), default=['4M'], nargs='*')
	parser.add_argument('--replacement-profile', choices=profiles['replacement'].keys(), default=['lru'], nargs='*')
	parser.add_argument('--core-profile', choices=profiles['core'].keys(), default=['default'], nargs='*')

	# Path options
	basedir = path.dirname(path.realpath(__file__))
	parser.add_argument('--traces', default=path.realpath('%s/../../experiments/sniper-traces/' % basedir), help='Location of sniper trace files')
	parser.add_argument('--output-dir', default=path.realpath('%s/../../experiments/run/' % basedir), help='Simulation outut target')
	parser.add_argument('--sniper-dir', default=path.realpath('%s/../../simulator/sniper/' % basedir), help='Sniper location')
	parser.add_argument('--force-output', default=False, action='store_true')

	# Various other options
	parser.add_argument('--max-sim-cores', type=int, default=16, help='Max number of simulated cores active at the time (16 for a 4-core simulation gives 4 simulations in parallel)')
	parser.add_argument('--qbs', action='store_true', default=False)
	parser.add_argument('--submit', action='store_true', default=False)

	# Collect all benchmarks
	parser.add_argument('benchmarks', nargs="+");

	args = parser.parse_args()


	# Argument validation
	if args.qbs or args.submit:
		exit("--qbs and --submit is not yet supported")

	if not path.exists(args.traces):
		exit('sniper trace directory %s does not exist' % args.traces)
	args.traces = path.realpath(args.traces);

	if path.exists(args.output_dir) and not args.force_output:
		exit('output directory %s already exists, use --force-output to overwrite' % args.output_dir)
	args.output_dir = path.realpath(args.output_dir);

	if not path.exists(args.sniper_dir) or not path.exists('%s/run-sniper' % args.sniper_dir):
		exit('sniper directory %s does not exists, or run-sniper script was not found within it' % args.sniper_dir)

	if args.max_sim_cores < 1 or args.max_sim_cores > 64:
		exit('invalid maximum sim cores %d, must be between 1 and 64' % args.max_sim_cores)


	# Create a cross product of selected configuration profiles
	# TODO: We want to extend this with a membus profile
	configurations = []
	for replacement in args.replacement_profile:
		for l2 in args.l2_profile:
			for l3 in args.l3_profile:
				for core in args.core_profile:
					core = profiles['core'][core]
					name = '%s.l2-%s.l3-%s.rob-%s.rs-%d.ol-%d.os-%d.mshr-%s' % (replacement, l2.rjust(5, '0'), l3.rjust(3, '0'), str(core['rob']).rjust(3, '0'), core['rs'], core['ol'], core['os'], str(core['mshr']).rjust(2, '0'))
					configurations.append({
						'l2': profiles['l2'][l2], 
						'l3': profiles['l3'][l3], 
						'policy': profiles['replacement'][replacement], 
						'core': core,
						'name': name
					})
		

	import benchmarks
	runs = benchmarks.get_benchmarks(args.traces, args.benchmarks) 

	import sniper
	print sniper.build_bash_script(args.output_dir, args.sniper_dir, runs, configurations)


	# TODO: Expand benchmark list using benchmark aliases

	# TODO: Generate output, copy code from project