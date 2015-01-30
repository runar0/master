

def build_config_string(config):
	""" Build a sniper configuration string based on a config dicitionary """

	variables = []

	for cache in ['l2', 'l3']:
		variables.append('-g perf_model/%s_cache/cache_size=%d' % (cache, config[cache]['size']))
		variables.append('-g perf_model/%s_cache/tags_access_time=%d' % (cache, config[cache]['tags']))
		variables.append('-g perf_model/%s_cache/data_access_time=%d' % (cache, config[cache]['data']))

	variables.append('-g perf_model/l3_cache/replacement_policy=%s' % config['policy']['policy'])

	return ' '.join(variables)


def build_command(traces, config):
	""" Build a single sniper command given a configuration set and traces """

	cores = len(traces)
	confstr = build_config_string(config)

	dumpStatsCmd = [];
	for cpu in range(cores):
		dumpStatsCmd.append('$SNIPER_DUMP_STATS --partial roi-begin:benchmark-%d-done > stats-benchmark-%d.txt' % (cpu,cpu))
	dumpStatsCmd = ' && '.join(dumpStatsCmd)

	command = "{ $SNIPER_EXECUTABLE -c cachepartiton -n %d --traces=%s -d . -sappeventsstats --sim-end last-restart %s; %s; }" % (cores, ','.join(traces), confstr, dumpStatsCmd)

	return command

def wrap_command(run_name, config_name, cmd):
	folder = '%s.%s' % (run_name,config_name)
	return '{ rm -rf "%s" ; mkdir "%s" ; pushd "%s" ; %s ; popd ; }' % (folder, folder, folder, cmd)


def build_commands(runs, configs):
	""" Build a list of sniper commands given a set of runs and a set of configurations """
	cmds = []
	for config in configs:
		for run in runs:
			cmd = build_command(run['traces'], config)
			cmd = wrap_command(run['name'], config['name'], cmd)

			cmds.append(cmd)

	return cmds

def build_bash_script(output_dir, sniper_dir, runs, configs):
	script = []

	script.append('#!/usr/bin/env bash')

	# Start by building header
	script.append('export SNIPER_EXECUTABLE=%s/run-sniper' % sniper_dir)
	script.append('export SNIPER_DUMP_STATS=%s/tools/dumpstats.py' % sniper_dir)

	# Create and move to output directory
	script.append('if [ ! -d "%s" ]; then mkdir -p "%s"; fi' % (output_dir, output_dir))
	script.append('pushd "%s"' % output_dir)

	# Job scheduler variables
	script.append('MAX_JOBS=%d' % 16)
	script.append('BLOCK_DURATION=15') 

	# Generate all commands
	script.append('COMMANDS=(');
	import pipes
	for cmd in build_commands(runs, configs):
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