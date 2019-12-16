import os, signal, glob, time, shutil
from .utils import Utils

class ZeekIndenter():
	def __init__(self, timeout=0, debug_flag=False, zeek_parser=None):
		self.TIMEOUT = timeout
		self.DEBUG_FLAG = debug_flag
		self.ZEEK_PARSER = zeek_parser

	def handler(self, signum, frame):
		raise Exception("TimeoutError")

	def cleanup(self, exc, fp, outdir):
		def moveTo(fp, path):
			if not os.path.exists(fp):
				open(fp, 'a').close()
			os.makedirs(os.path.dirname(path), exist_ok=True)
			shutil.move(fp, path + "/" + os.path.basename(fp))

		if self.DEBUG_FLAG:
			print (exc)

		if exc == "LarkParseError":
			moveTo(fp, outdir + "/error/lark/")
		elif exc == "TransformError":
			moveTo(fp, outdir + "/error/transform/")
		elif exc == "TimeoutError":
			moveTo(fp, outdir + "/error/timeout/")
		elif exc == "ZeekParseError":
			moveTo(fp, outdir + "/error/zeek/")
		elif exc == "Verified":
			moveTo(fp, outdir + "/verified/")
		else:
			print ("Something went wrong! File = " + fp)

	def indent_file(self, fp, idx, outdir, summary_flag):
		try:
			signal.signal(signal.SIGALRM, self.handler)
			signal.alarm(self.TIMEOUT)
			basename = os.path.basename(fp)
			ofile = os.path.join(outdir + "/" + basename)
			Utils.indent_file(self.ZEEK_PARSER, fp, idx, ofile, summary_flag, self.DEBUG_FLAG)
			raise Exception("Verified")
		except Exception as exc:
			self.cleanup(str(exc), ofile, outdir)

	def indent_directory(self, path, outdir):
	    files = []
	    for ext in ('*.zeek*', '*.bro*'):
	        files.extend(glob.glob(os.path.join(path, ext)))
	    
	    i, l = 0, len(files);
	    if l:
	        Utils.printProgress(0, l, prefix = 'Progress:', suffix = '', file = '', bar_length = 100)
	    start = time.time()

	    for f in files:
	        i += 1
	        self.indent_file(f, i, outdir, False)
	        Utils.printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', file = os.path.basename(f), bar_length = 100)
	               
	    end = time.time()
	    print ("\nAnalyzed %d Zeek files.\nTotal time: %s secs.\n"%(len(files), end-start))

	def parse_file(self, fp, summary_flag):
		signal.signal(signal.SIGALRM, self.handler)
		signal.alarm(self.TIMEOUT)

		tree = None
		start = time.time()

		try:
			tree = Utils.parse(self.ZEEK_PARSER, fp, self.DEBUG_FLAG)
		except Exception as exc:
			if self.DEBUG_FLAG:
				print (exc)

		end = time.time()

		if summary_flag:
			print("\nAnalyzed 1 Zeek file.\nParse time:\t%s secs.\n" % (end - start))

		return tree