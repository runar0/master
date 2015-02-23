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
	],
	'workload-bw': [
		['milc', 'libquantum', 'lbm', 'leslie3d'],
		['lbm', 'milc', 'bwaves', 'xalancbmk'],
		['libquantum', 'cactusADM', 'wrf', 'xalancbmk'],
		['wrf', 'libquantum', 'bwaves', 'xalancbmk'],
		['cactusADM', 'libquantum', 'milc', 'leslie3d'],
		['cactusADM', 'milc', 'wrf', 'lbm'],
		['wrf', 'libquantum', 'xalancbmk', 'milc'],
		['xalancbmk', 'cactusADM', 'libquantum', 'milc'],
		['milc', 'xalancbmk', 'cactusADM', 'wrf'],
		['bwaves', 'leslie3d', 'xalancbmk', 'wrf'],
	],
	'workload-cache-bw': [
	    ['bzip2', 'sphinx3', 'gcc', 'omnetpp'],
		['zeusmp', 'gcc', 'soplex', 'sphinx3'],
		['sphinx3', 'gcc', 'mcf', 'zeusmp'],
		['zeusmp', 'bzip2', 'omnetpp', 'soplex'],
		['omnetpp', 'sphinx3', 'soplex', 'zeusmp'],
		['zeusmp', 'bzip2', 'sphinx3', 'soplex'],
		['mcf', 'soplex', 'gcc', 'bzip2'],
		['mcf', 'bzip2', 'gcc', 'zeusmp'],
		['mcf', 'sphinx3', 'gcc', 'bzip2'],
		['gcc', 'mcf', 'omnetpp', 'sphinx3'],
	],
	'workload-compute': [
		['povray', 'namd', 'calculix', 'gamess'],
		['gamess', 'povray', 'dealII', 'GemsFDTD'],
		['GemsFDTD', 'povray', 'sjeng', 'namd'],
		['sjeng', 'calculix', 'GemsFDTD', 'povray'],
		['GemsFDTD', 'gamess', 'calculix', 'namd'],
		['GemsFDTD', 'calculix', 'sjeng', 'dealII'],
		['namd', 'calculix', 'povray', 'GemsFDTD'],
		['calculix', 'dealII', 'namd', 'gamess'],
		['namd', 'povray', 'dealII', 'gamess'],
		['dealII', 'calculix', 'GemsFDTD', 'namd'],
	],
	'workload-random': [
		['zeusmp', 'GemsFDTD', 'sphinx3', 'povray'],
		['cactusADM', 'omnetpp', 'bzip2', 'gobmk'],
		['gobmk', 'tonto', 'wrf', 'dealII'],
		['zeusmp', 'hmmer', 'h264ref', 'perlbench'],
		['milc', 'omnetpp', 'sphinx3', 'mcf'],
		['hmmer', 'calculix', 'omnetpp', 'perlbench'],
		['omnetpp', 'gobmk', 'mcf', 'xalancbmk'],
		['milc', 'wrf', 'GemsFDTD', 'astar'],
		['astar', 'gcc', 'namd', 'wrf'],
		['omnetpp', 'leslie3d', 'sjeng', 'gamess'],
		['soplex', 'cactusADM', 'gromacs', 'namd'],
		['astar', 'gcc', 'xalancbmk', 'omnetpp'],
		['sphinx3', 'gobmk', 'sjeng', 'povray'],
		['sjeng', 'sphinx3', 'gcc', 'perlbench'],
		['gcc', 'namd', 'sjeng', 'bzip2'],
		['cactusADM', 'hmmer', 'sjeng', 'h264ref'],
		['lbm', 'omnetpp', 'wrf', 'calculix'],
		['povray', 'perlbench', 'astar', 'gcc'],
		['leslie3d', 'perlbench', 'mcf', 'povray'],
		['sjeng', 'gobmk', 'hmmer', 'tonto'],
	],
}
