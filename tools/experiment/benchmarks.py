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
		['perlbench', 'h264ref', 'gobmk', 'hmmer'],
		['perlbench', 'gobmk', 'astar', 'h264ref'],
		['perlbench', 'hmmer', 'h264ref', 'astar'],
		['perlbench', 'astar', 'gobmk', 'hmmer'],
		['h264ref', 'gobmk', 'hmmer', 'astar'],
	],	
	'workload-bw': [
		['wrf', 'gcc', 'milc', 'libquantum'],
		['libquantum', 'milc', 'gcc', 'xalancbmk'],
		['libquantum', 'cactusADM', 'milc', 'zeusmp'],
		['xalancbmk', 'libquantum', 'lbm', 'milc'],
		['bwaves', 'gcc', 'lbm', 'xalancbmk'],
		['xalancbmk', 'wrf', 'cactusADM', 'libquantum'],
		['libquantum', 'gcc', 'xalancbmk', 'bwaves'],
		['cactusADM', 'milc', 'zeusmp', 'gcc'],
		['wrf', 'gcc', 'bwaves', 'cactusADM'],
		['libquantum', 'gcc', 'milc', 'lbm'],
	],	
	'workload-cache-bw': [
		['omnetpp', 'sphinx3', 'soplex', 'bzip2'],
		['sphinx3', 'mcf', 'soplex', 'omnetpp'],
		['sphinx3', 'mcf', 'soplex', 'bzip2'],
		['bzip2', 'sphinx3', 'omnetpp', 'mcf'],
		['soplex', 'bzip2', 'omnetpp', 'mcf'],
	],	
	'workload-compute': [
		['sjeng', 'calculix', 'namd', 'dealII'],
		['namd', 'GemsFDTD', 'sjeng', 'tonto'],
		['povray', 'gamess', 'calculix', 'namd'],
		['calculix', 'tonto', 'gromacs', 'povray'],
		['gromacs', 'namd', 'leslie3d', 'calculix'],
		['namd', 'dealII', 'sjeng', 'tonto'],
		['sjeng', 'povray', 'gromacs', 'dealII'],
		['leslie3d', 'gromacs', 'povray', 'dealII'],
		['GemsFDTD', 'dealII', 'calculix', 'povray'],
		['dealII', 'namd', 'calculix', 'gromacs'],
	],	
	'workload-random': [
		['libquantum', 'namd', 'perlbench', 'gcc'],
		['calculix', 'gobmk', 'GemsFDTD', 'cactusADM'],
		['astar', 'mcf', 'omnetpp', 'gcc'],
		['lbm', 'povray', 'sphinx3', 'gamess'],
		['calculix', 'dealII', 'lbm', 'perlbench'],
		['libquantum', 'h264ref', 'GemsFDTD', 'gamess'],
		['astar', 'sphinx3', 'lbm', 'libquantum'],
		['sphinx3', 'soplex', 'povray', 'perlbench'],
		['sphinx3', 'bwaves', 'gobmk', 'bzip2'],
		['milc', 'calculix', 'astar', 'povray'],
		['lbm', 'hmmer', 'calculix', 'gamess'],
		['bwaves', 'soplex', 'GemsFDTD', 'milc'],
		['mcf', 'hmmer', 'cactusADM', 'wrf'],
		['sphinx3', 'leslie3d', 'namd', 'tonto'],
		['sphinx3', 'libquantum', 'calculix', 'povray'],
		['cactusADM', 'perlbench', 'povray', 'gromacs'],
		['astar', 'libquantum', 'calculix', 'soplex'],
		['tonto', 'povray', 'libquantum', 'cactusADM'],
		['xalancbmk', 'mcf', 'cactusADM', 'sjeng'],
		['h264ref', 'soplex', 'astar', 'libquantum'],
	],	
	'workload-8': [
		['tonto', 'bzip2', 'gobmk', 'h264ref', 'soplex', 'astar', 'hmmer', 'mcf'],
		['sjeng', 'omnetpp', 'GemsFDTD', 'calculix', 'perlbench', 'xalancbmk', 'gcc', 'mcf'],
		['h264ref', 'sjeng', 'gromacs', 'milc', 'tonto', 'libquantum', 'povray', 'astar'],
		['calculix', 'omnetpp', 'gromacs', 'mcf', 'gobmk', 'leslie3d', 'xalancbmk', 'soplex'],
		['dealII', 'leslie3d', 'povray', 'gamess', 'wrf', 'sphinx3', 'cactusADM', 'perlbench'],
		['lbm', 'xalancbmk', 'libquantum', 'sjeng', 'cactusADM', 'zeusmp', 'hmmer', 'povray'],
		['h264ref', 'lbm', 'mcf', 'wrf', 'omnetpp', 'hmmer', 'perlbench', 'gamess'],
		['libquantum', 'leslie3d', 'h264ref', 'namd', 'cactusADM', 'astar', 'perlbench', 'dealII'],
		['astar', 'sjeng', 'povray', 'h264ref', 'calculix', 'gcc', 'gamess', 'wrf'],
		['gcc', 'gamess', 'milc', 'gromacs', 'tonto', 'hmmer', 'wrf', 'sphinx3'],
	],
	'workload-16': [
		['bzip2', 'calculix', 'astar', 'omnetpp', 'wrf', 'gamess', 'gobmk', 'povray', 'leslie3d', 'xalancbmk', 'namd', 'milc', 'hmmer', 'GemsFDTD', 'lbm', 'gcc'],
		['wrf', 'gobmk', 'zeusmp', 'leslie3d', 'perlbench', 'hmmer', 'milc', 'cactusADM', 'calculix', 'tonto', 'bwaves', 'povray', 'omnetpp', 'h264ref', 'gromacs', 'bzip2'],
		['wrf', 'GemsFDTD', 'libquantum', 'tonto', 'omnetpp', 'dealII', 'perlbench', 'soplex', 'lbm', 'leslie3d', 'bwaves', 'calculix', 'xalancbmk', 'milc', 'gamess', 'namd'],
		['soplex', 'povray', 'h264ref', 'leslie3d', 'namd', 'gobmk', 'hmmer', 'sjeng', 'astar', 'omnetpp', 'gcc', 'lbm', 'gamess', 'wrf', 'sphinx3', 'GemsFDTD'],
		['astar', 'bwaves', 'cactusADM', 'zeusmp', 'h264ref', 'omnetpp', 'namd', 'gromacs', 'GemsFDTD', 'libquantum', 'sphinx3', 'hmmer', 'xalancbmk', 'leslie3d', 'gcc', 'gamess'],
		['sphinx3', 'GemsFDTD', 'soplex', 'milc', 'libquantum', 'astar', 'zeusmp', 'omnetpp', 'namd', 'bwaves', 'bzip2', 'lbm', 'povray', 'cactusADM', 'h264ref', 'dealII'],
		['bwaves', 'hmmer', 'sjeng', 'leslie3d', 'astar', 'mcf', 'GemsFDTD', 'gromacs', 'libquantum', 'sphinx3', 'bzip2', 'omnetpp', 'gcc', 'milc', 'cactusADM', 'zeusmp'],
		['omnetpp', 'calculix', 'tonto', 'hmmer', 'h264ref', 'astar', 'wrf', 'sjeng', 'soplex', 'namd', 'zeusmp', 'povray', 'leslie3d', 'gromacs', 'gamess', 'perlbench'],
		['lbm', 'h264ref', 'soplex', 'gobmk', 'cactusADM', 'tonto', 'zeusmp', 'GemsFDTD', 'calculix', 'gromacs', 'bzip2', 'gcc', 'sphinx3', 'mcf', 'sjeng', 'namd'],
		['lbm', 'sjeng', 'sphinx3', 'tonto', 'milc', 'mcf', 'wrf', 'omnetpp', 'bzip2', 'leslie3d', 'gcc', 'perlbench', 'gamess', 'calculix', 'namd', 'xalancbmk'],
	]
}
