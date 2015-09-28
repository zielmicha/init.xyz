# This is the main configuration file for init.xyz, see http://init.xyz/doc for documentation
from initxyz.common.ensure import *

execfile_if_exists('machines/%s.py' % hostname())
