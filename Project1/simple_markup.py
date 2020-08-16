import sys, re
from util import *

print('<html><head><title>...</title><body>')

fin = open('test_input.txt', 'r')
old = sys.stdin
sys.stdin = fin

fout = open('test_output.html', 'w')
old_out = sys.stdout
sys.stdout = fout
title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if title:
        print('<h1>')
        print(block)
        print('</h1>')
        title = False
    else:
        print('<p>')
        print(block)
        print('</p>')

print('</body></html>')
