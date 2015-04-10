

def build_config_string(config, cores):
	""" Build a sniper configuration string based on a config dicitionary """

	variables = []

	for cache in ['l2', 'l3']:
		variables.append('-g perf_model/%s_cache/cache_size=%d' % (cache, config[cache]['size']))
		variables.append('-g perf_model/%s_cache/tags_access_time=%d' % (cache, config[cache]['tags']))
		variables.append('-g perf_model/%s_cache/data_access_time=%d' % (cache, config[cache]['data']))
		if 'ways' in config[cache]:
			variables.append('-g perf_model/%s_cache/associativity=%d' % (cache, config[cache]['ways']))


	variables.append('-g perf_model/l3_cache/shared_cores=%d' % (cores))

	if config['policy']['policy'] == "pipp": 		
		variables.append('-g perf_model/l3_cache/replacement_policy=pipp')
		variables.append('-g perf_model/l3_cache/umon/enable_stream_detection=true')
	elif config['policy']['policy'] == "pipp-min8": 		
		variables.append('-g perf_model/l3_cache/replacement_policy=pipp')
		variables.append('-g perf_model/l3_cache/umon/enable_stream_detection=true')
		variables.append('-g perf_model/l3_cache/pipp_min_insert=8')
	elif config['policy']['policy'] == "drrip-3": 		
		variables.append('-g perf_model/l3_cache/replacement_policy=drrip')
		variables.append('-g perf_model/l3_cache/drrip/bits=3')
	else:
		variables.append('-g perf_model/l3_cache/replacement_policy=%s' % (config['policy']['policy']))

	# Core model
	variables.append('-g perf_model/core/interval_timer/window_size=%d' % config['core']['rob'])
	variables.append('-g perf_model/core/rob_timer/outstanding_loads=%d' % config['core']['ol'])
	variables.append('-g perf_model/core/rob_timer/outstanding_stores=%d' % config['core']['os'])
	variables.append('-g perf_model/core/rob_timer/rs_entries=%d' % config['core']['rs'])
	variables.append('-g perf_model/l1_icache/outstanding_misses=%d' % config['core']['mshr'])
	variables.append('-g perf_model/l1_dcache/outstanding_misses=%d' % config['core']['mshr'])
	variables.append('-g perf_model/l2_cache/outstanding_misses=%d' % (config['core']['mshr2']))

	# Membus
	variables.append('-g perf_model/dram/per_controller_bandwidth=%f' % (config['membus']['bw']))
	variables.append('-g perf_model/dram/latency=%f' % (config['membus']['latency']))

	# Clock skew minimization barrier
	variables.append('-g clock_skew_minimization/barrier/quantum=%d' % (config['csmb']['barrier']))


	return ' '.join(variables)


def build_command(traces, config, periodic_stats):
	""" Build a single sniper command given a configuration set and traces """

	cores = len(traces)
	confstr = build_config_string(config, cores)

	dumpStatsCmd = [];
	for cpu in range(cores):
		dumpStatsCmd.append('$SNIPER_DUMP_STATS --partial roi-begin:benchmark-%d-done > stats-benchmark-%d.txt' % (cpu,cpu))
	dumpStatsCmd = ' && '.join(dumpStatsCmd)

	output_pipe = '2> sim.stderr.log 1> sim.stdout.log'
	command = "{ $SNIPER_EXECUTABLE -c cachepartiton -n %d --traces=%s -d . -sappeventsstats%s --sim-end last-restart %s %s; %s; }" % (cores, ','.join(traces), ":periodic" if periodic_stats else "", confstr, output_pipe, dumpStatsCmd)

	return command

def wrap_command(run_name, config_name, cmd):
	folder = '%s.%s' % (run_name,config_name)
	start = 'echo "Starting %s"' % folder
	return '{ if [ ! -f "%s/.sift_done" ]; then { rm -rf "%s"; mkdir "%s" ; pushd "%s" > /dev/null ; %s; %s; popd > /dev/null ; } fi }' % (folder, folder, folder, folder, start, cmd)


def build_commands(runs, configs, periodic_stats):
	""" Build a list of sniper commands given a set of runs and a set of configurations """
	cmds = []
	for config in configs:
		for run in runs:
			cmd = build_command(run['traces'], config, periodic_stats)
			cmd = wrap_command(run['name'], config['name'], cmd)

			cmds.append(cmd)

	return cmds

def build_bash_script(args, runs, configs):
	script = []

	output_dir = args.output_dir
	sniper_dir = args.sniper_dir
	max_sim_cores = args.max_sim_cores

	script.append('#!/usr/bin/env bash')

	# Start by building header
	script.append('export SNIPER_EXECUTABLE=%s/run-sniper' % sniper_dir)
	script.append('export SNIPER_DUMP_STATS=%s/tools/dumpstats.py' % sniper_dir)

	# Create and move to output directory
	script.append('if [ ! -d "%s" ]; then mkdir -p "%s"; fi' % (output_dir, output_dir))
	script.append('pushd "%s"' % output_dir)

	# Job scheduler variables
	max_job_width = max([len(run['traces']) for run in runs])
	max_jobs = max_sim_cores / max_job_width
	if max_jobs == 0: max_jobs = 1

	script.append('MAX_JOBS=%d' % max_jobs)
	script.append('BLOCK_DURATION=15') 

	# Generate all commands
	script.append('COMMANDS=(');
	import pipes
	for cmd in build_commands(runs, configs, args.periodic_stats):
		script.append('    %s' % pipes.quote(cmd))
	script.append(')')

	# Job scheduler
	script.append("""
# Count number of jobs currently in state Running
function job_count {
	jobs=`jobs -l | grep Running | wc -l`
	echo $jobs
}

# Issue jobs untill all commands are executed, but only run $MAX_JOBS in parallel
function schedule {
	for ((i = 0; i < ${#COMMANDS[@]}; i++))
	do
		echo -e "\e[1;32m[Starting]: \e[0;34m[$((i+1))/${#COMMANDS[@]}] \e[0;30m${COMMANDS[$i]}"
		{ bash -c "${COMMANDS[$i]}" ; echo -e "\e[1;32m[Done]: \e[0;34m$((i+1))\e[0;30m" ; } &
		while [ `job_count` -ge $MAX_JOBS ]
		do
			sleep $BLOCK_DURATION
		done
	done

	wait
	echo -e "\e[1;32mAll jobs completed\e[0;30m"
}

schedule
	  """)

	# End
	script.append('popd')

	return '\n'.join(script)

def build_qbs_script(output_dir, sniper_dir, runs, configs):
	# TODO: Use the bash generator but decorate with correct queue system headers
	pass