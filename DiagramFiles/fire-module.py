import sys
sys.path.append('../../../../../../lib/PlotMakers/')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    to_Conv( name='c1', s_filer=1, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=2, height=20, depth=20  ),
    to_Conv( name='c2', s_filer=1, n_filer=256, offset="(1,0,0)", to="(c1-east)", width=8, height=20, depth=20  ),
    to_connection("c1","c2"),
    to_Conv( name='c3', s_filer=3, n_filer=256, offset="(1,5,0)", to="(c1-east)", width=8, height=20, depth=20  ),
    to_connection("c1","c3"),
    to_Sum( name="out", offset="(2,0,0)", to=("(c2-east)")),
    to_connection("c3","out"),
    to_connection("c2","out"),
    to_Conv(name="pool1", offset="(1,0,0)", to="(out-east)",  s_filer="", n_filer=512, width=16, height=20, depth=20, caption = "Output will have 512 layers after concatenation"),
    to_connection("out","pool1"),
    
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
