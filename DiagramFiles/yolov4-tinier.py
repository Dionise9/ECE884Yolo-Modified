import sys
sys.path.append('../../../../../../lib/PlotMakers/')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    #block-001
    to_Conv( name='c1', s_filer="", n_filer=32, offset="(0,0,0)", to="(0,0,0)", width=2, height=50, depth=50  ),
    to_Conv( name='c2', s_filer="", n_filer=64, offset="(0,0,0)", to="(c1-east)", width=4, height=40, depth=40  ),
    #to_connection("c1","c2"),
    to_Conv( name='c3', s_filer="", n_filer=64, offset="(0,0,0)", to="(c2-east)", width=4, height=30, depth=30  ),
    #to_connection("c2","c3"),
    to_Conv( name='c4', s_filer="", n_filer=32, offset="(0,0,0)", to="(c3-east)", width=2, height=30, depth=30  ),
    #to_connection("c3","c4"),
    to_Conv( name='c5', s_filer="", n_filer=32, offset="(0,0,0)", to="(c4-east)", width=2, height=30, depth=30  ),
    #to_connection("c4","c5"),
    to_Conv( name='c6', s_filer=1, n_filer=64, offset="(0,0,0)", to="(c5-east)", width=4, height=30, depth=30  ),
    #to_connection("c5","c6"),
    to_skip( "c4", "c6"),
    to_Pool(name="pool1", offset="(0,0,0)", to="(c6-east)", width=1, height=20, depth=20, opacity=0.5),
    to_skip("c3","pool1"),
    
    
    #Block 2
    to_Conv( name='c7', s_filer="", n_filer=128, offset="(2,0,0)", to="(pool1-east)", width=8, height=20, depth=20  ),
    to_Pool(name="pool2", offset="(0,0,0)", to="(c7-east)", width=1, height=10, depth=10, opacity=0.5),
    to_connection("pool1","c7"),
    
    to_Conv( name='c8', s_filer="", n_filer="", offset="(2,0,0)", to="(pool2-east)", width=16, height=10, depth=10, caption = "Fire Modules"  ),
    to_connection("c7","c8"),
    to_Conv( name='c9', s_filer="", n_filer="", offset="(1,0,0)", to="(c8-east)", width=16, height=10, depth=10  ),
    to_connection("c8","c9"),
    to_skip("pool2","c9"),
    to_Conv( name='c10', s_filer="", n_filer="", offset="(1,0,0)", to="(c9-east)", width=16, height=10, depth=10, caption = "Densely Connected" ),
    to_connection("c9","c10"),
    to_skip("pool2","c10"),
    to_skip("c8","c10"),
    to_Conv( name='c11', s_filer="", n_filer="", offset="(1,0,0)", to="(c10-east)", width=16, height=10, depth=10  ),
    to_connection("c10","c11"),
    to_skip("pool2","c11"),
    to_skip("c8","c11"),
    to_skip("c9","c11"),

    to_Pool(name="pool3", offset="(0,0,0)", to="(c11-east)", width=1, height=5, depth=5, opacity=0.5),
    to_skip("pool2","pool3"),
    to_skip("c8","pool3"),
    to_skip("c9","pool3"),
    to_skip("c10","pool3"),
    
    to_Conv( name='c17', s_filer="", n_filer="", offset="(2,0,0)", to="(pool3-east)", width=16, height=5, depth=5, caption = "Fire Module 5"  ),
    to_connection("pool3","c17"),
    to_Conv( name='c18', s_filer="", n_filer=30, offset="(0,0,0)", to="(c17-east)", width=2, height=5, depth=5),
    
    
    to_ConvRes( name='c19', s_filer="", n_filer="", offset="(1,0,0)", to="(c18-east)", width=2, height=5, depth=5, caption="YOLO Layer 1"  ),
    to_connection("c17","c19"),
    
    to_Conv( name='c20', s_filer=1, n_filer=128, offset="(1,0,0)", to="(c19-east)", width=8, height=5, depth=5  ),
    to_skip('c18','c20'),
    to_UnPool(name='up1', offset="(0,0,0)", to="(c20-east)", width=1, height=10, depth=10, opacity=0.5, caption=""),
    to_Conv( name='c21', s_filer="", n_filer="", offset="(2,0,0)", to="(up1-east)", width=16, height=10, depth=10, caption = "Fire Module 6"  ),
    to_skip("c11","c21"),
    to_connection("up1","c21"),
    to_Conv( name='c22', s_filer=1, n_filer=30, offset="(0,0,0)", to="(c21-east)", width=2, height=10, depth=10),
    to_ConvRes( name='c23', s_filer="", n_filer="", offset="(1,0,0)", to="(c22-east)", width=2, height=10, depth=10, caption="YOLO Layer 2"  ),
    to_connection("c22","c23"),
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
