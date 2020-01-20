




# if __name__ == '__main__':
#     luigi.build([MyTask1(x=10), MyTask2(x=15, z=3)] , local_scheduler=True)
#
#     python -m luigi --module my_module MyTask --x 100 --local-scheduler

# if __name__ == '__main__':

import os
from pathlib import Path

print("cwd=" + os.getcwd() + "\n")

home = str(Path.home())

# define current directory
current_dir = home + '/Downloads/'

# update 'pathFile' to full path- absolute
current_dir = os.path.abspath(current_dir)

# update the current work directory
os.chdir(current_dir)

print("cwd=" + os.getcwd() + "\n")


# remove the output folder
import shutil
shutil.rmtree('outputs', ignore_errors=True)

# run the luigi script from the workflow run
import luigi.interface
# import hermes
# luigi.build([hermes.finalnode_xx_0()], local_scheduler=True)

from hermes import finalnode_xx_0
luigi.build([finalnode_xx_0()], local_scheduler=True)


    # python3 -m luigi --module heermes finalnode_xx_0 --local-scheduler