from unittest import TestCase

from utils.Dev      import Dev
from utils.Process  import Process


class Test_Process(TestCase):

    def test_run__ls(self):
        result = Process.run('ls')
        #assert result == {'runParams': ['ls'], 'stderr': '', 'stdout': 'Test_Process.py\naws\n'}
        Dev.pprint(result)
        result = Process.run('ls', ['-la', '..'])
        #assert '-rw-r--r--@  1 dinis  staff  6148 Oct 29 11:59 .DS_Store\n' in result['stdout']
        Dev.pprint(result)

