import sys
import os.path
import mpasparse
import mpascheck
import sys
from errors import subscribe_errors


filename = sys.argv[1]
outfile = os.path.splitext(filename)[0] + ".s"

f = open(filename)
data = f.read()
f.close()
parser = mpasparse.make_parser()
with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
  top = parser.parse(data)
  mpascheck.check_program(top)

  if top:
    import mpasgen
    outf = open(outfile,"w")
    mpasgen.generate(outf,top)
    mpasgen.emit_program(outf,top)
    outf.close()
    if sys.argv[-1] == '-t':
      mpasparse.dump_tree(top)
  