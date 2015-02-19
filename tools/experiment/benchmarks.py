# http://www.m5sim.org/SPEC_CPU2006_benchmarks

import sys
from os import path

def convert_to_traces(tracedir, benchmarks, length):
	parsed = []

	if length == '100M':
		length = 100000000
	elif length == '250M':
		length = 250000000
	else:
		length = 500000000

	for run in benchmarks:
		item = []
		for benchmark in run:
			name = path.realpath('%s/%s.%d' % (tracedir, benchmark, length))
			if not path.exists(name + '.sift'):
				sys.exit('Missing trace for %s (%s.sift)' % (benchmark, name))

			item.append(name)

		run = {
			'name': '-'.join(run),
			'traces': item
		}
		parsed.append(run)
	return parsed

def get_benchmarks(tracedir, benchmarks, length):
	"""  """

	if not type(benchmarks) is list:
		benchmarks = [benchmarks]

	parsed = []
	for benchmark in benchmarks:
		if benchmark in benchmark_sets:
			for item in benchmark_sets[benchmark]:
				parsed.append(item)
		else:
			parsed.append(benchmark.split('-'))


	return convert_to_traces(tracedir, parsed, length)



benchmark_sets = {
	'benchmarks': [
        ['perlbench'],
        ['bzip2'],
        ['gcc'],
        ['bwaves'],
        ['gamess'],
        ['mcf'],
        ['milc'],
        ['zeusmp'],
        ['gromacs'],
        ['cactusADM'],
        ['leslie3d'],
        ['namd'],
        ['gobmk'],
        ['dealII'],
        ['sjeng'],
        ['soplex'],
        ['povray'],
        ['calculix'],
        ['hmmer'],
        ['GemsFDTD'],
        ['libquantum'],
        ['h264ref'],
        ['tonto'],
        ['lbm'],
        ['omnetpp'],
        ['astar'],
        ['wrf'],
        ['sphinx3'],
        ['xalancbmk'],
	],	
	'workload-cache': [
		['tonto', 'astar', 'perlbench', 'hmmer'],
		['perlbench', 'gromacs', 'h264ref', 'tonto'],
		['gromacs', 'gobmk', 'astar', 'perlbench'],
		['h264ref', 'hmmer', 'tonto', 'perlbench'],
		['hmmer', 'perlbench', 'gromacs', 'h264ref'],
		['gromacs', 'h264ref', 'perlbench', 'gobmk'],
		['h264ref', 'gobmk', 'perlbench', 'hmmer'],
		['h264ref', 'tonto', 'perlbench', 'astar'],
		['h264ref', 'astar', 'gromacs', 'hmmer'],
		['hmmer', 'perlbench', 'tonto', 'gobmk'],
	]
}
