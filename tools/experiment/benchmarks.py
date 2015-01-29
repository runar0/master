# http://www.m5sim.org/SPEC_CPU2006_benchmarks

import sys
from os import path

def convert_to_traces(tracedir, benchmarks):
	parsed = []
	for run in benchmarks:
		item = []
		for benchmark in run:
			name = path.realpath('%s/%s' % (tracedir, benchmark))
			if not path.exists(name + '.sift'):
				sys.exit('Missing trace for %s (%s.sift)' % (benchmark, name))

			item.append(name)

		run = {
			'name': '-'.join(run),
			'traces': item
		}
		parsed.append(run)
	return parsed

def get_benchmarks(tracedir, benchmarks):
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


	return convert_to_traces(tracedir, parsed)



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
		['bzip2', 'h264ref', 'hmmer', 'sphinx3'],
		['bzip2', 'h264ref', 'hmmer', 'gcc'],
		['bzip2', 'h264ref', 'gcc', 'sphinx3'],
		['bzip2', 'gcc', 'hmmer', 'sphinx3'],
		['gcc', 'h264ref', 'hmmer', 'sphinx3']
	],
	'workload-cache-bw': [
		['omnetpp', 'perlbench', 'soplex', 'tonto'],
		['omnetpp', 'perlbench', 'soplex', 'gobmk'],
		['omnetpp', 'perlbench', 'gobmk', 'tonto'],
		['omnetpp', 'gobmk', 'soplex', 'tonto'],
		['gobmk', 'perlbench', 'soplex', 'tonto']
	],
	'workload-bw': [
		['astar', 'cactusADM', 'lbm', 'wrf'],
		['wrf', 'bwaves', 'GemsFDTD', 'astar'],
		['wrf', 'cactusADM', 'milc', 'GemsFDTD'],
		['wrf', 'zeusmp', 'leslie3d', 'GemsFDTD'],
		['leslie3d', 'lbm', 'astar', 'cactusADM'],
		['bwaves', 'astar', 'xalancbmk', 'lbm'],
		['lbm', 'wrf', 'milc', 'xalancbmk'],
		['astar', 'bwaves', 'lbm', 'cactusADM'],
		['xalancbmk', 'cactusADM', 'zeusmp', 'GemsFDTD'],
		['xalancbmk', 'leslie3d', 'cactusADM', 'GemsFDTD'],
	],
	'workload-compute': [
		['calculix', 'mcf', 'gamess', 'sjeng'],
		['libquantum', 'mcf', 'namd', 'calculix'],
		['gamess', 'mcf', 'calculix', 'libquantum'],
		['libquantum', 'mcf', 'gamess', 'namd'],
		['libquantum', 'povray', 'namd', 'mcf'],
		['libquantum', 'mcf', 'povray', 'gamess'],
		['povray', 'gamess', 'namd', 'libquantum'],
		['namd', 'sjeng', 'gamess', 'povray'],
		['gamess', 'sjeng', 'libquantum', 'povray'],
		['sjeng', 'libquantum', 'mcf', 'gamess'],
	],
	'workload-random': [
		['leslie3d', 'bwaves', 'zeusmp', 'bzip2'],
		['milc', 'mcf', 'leslie3d', 'namd'],
		['gamess', 'omnetpp', 'calculix', 'hmmer'],
		['milc', 'sphinx3', 'gamess', 'h264ref'],
		['bzip2', 'xalancbmk', 'soplex', 'GemsFDTD'],
		['wrf', 'gamess', 'mcf', 'libquantum'],
		['zeusmp', 'wrf', 'povray', 'tonto'],
		['perlbench', 'gobmk', 'bwaves', 'gamess'],
		['libquantum', 'mcf', 'gobmk', 'wrf'],
		['calculix', 'lbm', 'bzip2', 'namd'],
		['namd', 'GemsFDTD', 'hmmer', 'cactusADM'],
		['hmmer', 'lbm', 'bzip2', 'GemsFDTD'],
		['tonto', 'povray', 'cactusADM', 'libquantum'],
		['h264ref', 'soplex', 'namd', 'xalancbmk'],
		['namd', 'wrf', 'tonto', 'gobmk'],
		['cactusADM', 'astar', 'hmmer', 'perlbench'],
		['gcc', 'perlbench', 'wrf', 'GemsFDTD'],
		['omnetpp', 'xalancbmk', 'bzip2', 'mcf'],
		['GemsFDTD', 'libquantum', 'povray', 'milc'],
		['sjeng', 'calculix', 'wrf', 'milc'],
	],


	'workloads': [
		['bzip2', 'h264ref', 'hmmer', 'sphinx3'],
		['bzip2', 'h264ref', 'hmmer', 'gcc'],
		['bzip2', 'h264ref', 'gcc', 'sphinx3'],
		['bzip2', 'gcc', 'hmmer', 'sphinx3'],
		['gcc', 'h264ref', 'hmmer', 'sphinx3'],
		['omnetpp', 'perlbench', 'soplex', 'tonto'],
		['omnetpp', 'perlbench', 'soplex', 'gobmk'],
		['omnetpp', 'perlbench', 'gobmk', 'tonto'],
		['omnetpp', 'gobmk', 'soplex', 'tonto'],
		['gobmk', 'perlbench', 'soplex', 'tonto'],
		['astar', 'cactusADM', 'lbm', 'wrf'],
		['wrf', 'bwaves', 'GemsFDTD', 'astar'],
		['wrf', 'cactusADM', 'milc', 'GemsFDTD'],
		['wrf', 'zeusmp', 'leslie3d', 'GemsFDTD'],
		['leslie3d', 'lbm', 'astar', 'cactusADM'],
		['bwaves', 'astar', 'xalancbmk', 'lbm'],
		['lbm', 'wrf', 'milc', 'xalancbmk'],
		['astar', 'bwaves', 'lbm', 'cactusADM'],
		['xalancbmk', 'cactusADM', 'zeusmp', 'GemsFDTD'],
		['xalancbmk', 'leslie3d', 'cactusADM', 'GemsFDTD'],
		['calculix', 'mcf', 'gamess', 'sjeng'],
		['libquantum', 'mcf', 'namd', 'calculix'],
		['gamess', 'mcf', 'calculix', 'libquantum'],
		['libquantum', 'mcf', 'gamess', 'namd'],
		['libquantum', 'povray', 'namd', 'mcf'],
		['libquantum', 'mcf', 'povray', 'gamess'],
		['povray', 'gamess', 'namd', 'libquantum'],
		['namd', 'sjeng', 'gamess', 'povray'],
		['gamess', 'sjeng', 'libquantum', 'povray'],
		['sjeng', 'libquantum', 'mcf', 'gamess'],
		['leslie3d', 'bwaves', 'zeusmp', 'bzip2'],
		['milc', 'mcf', 'leslie3d', 'namd'],
		['gamess', 'omnetpp', 'calculix', 'hmmer'],
		['milc', 'sphinx3', 'gamess', 'h264ref'],
		['bzip2', 'xalancbmk', 'soplex', 'GemsFDTD'],
		['wrf', 'gamess', 'mcf', 'libquantum'],
		['zeusmp', 'wrf', 'povray', 'tonto'],
		['perlbench', 'gobmk', 'bwaves', 'gamess'],
		['libquantum', 'mcf', 'gobmk', 'wrf'],
		['calculix', 'lbm', 'bzip2', 'namd'],
		['namd', 'GemsFDTD', 'hmmer', 'cactusADM'],
		['hmmer', 'lbm', 'bzip2', 'GemsFDTD'],
		['tonto', 'povray', 'cactusADM', 'libquantum'],
		['h264ref', 'soplex', 'namd', 'xalancbmk'],
		['namd', 'wrf', 'tonto', 'gobmk'],
		['cactusADM', 'astar', 'hmmer', 'perlbench'],
		['gcc', 'perlbench', 'wrf', 'GemsFDTD'],
		['omnetpp', 'xalancbmk', 'bzip2', 'mcf'],
		['GemsFDTD', 'libquantum', 'povray', 'milc'],
		['sjeng', 'calculix', 'wrf', 'milc'],
	]
}
