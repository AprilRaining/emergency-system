"""
  print_table will print a structured table with headers, defined column widths, and automatic text wrapping in columns. 
    It will also determine the terminal width and reduce the column widths automatically so they all fit without wrapping outside of the table
  
  print_table requires 3 parameters
    headers: A list or tuple of headers (strings)
    rows:   A list of lists or tuples with table row information as strings
              each entry in inner list maps to a column. 
            For a 3 column table, provide a list of lists or tuples with a length of 3
    sizes:  A list or tuple of integers specifying maximum column width for each column. Must provide a value for each column.
            columns will automatically be shrunk to fit the size of the widest data in the column if smaller than max width.
"""
# This function is obtained from an open source library!!!
import os
DEFAULT_WIDTH = 80
from system_log import *

def print_table(headers, rows, sizes):
    def fit_to_term():
        # find terminal width, then reduce largest column size by 1 until everything fits 
        try:
            x, _ = os.get_terminal_size()
        except OSError:
            x = DEFAULT_WIDTH
        width = sum(short_sizes) + len(short_sizes) - 1
        sizes = [s for s in short_sizes]
        while width > x:
            widest = max(sizes)
            for n, size in enumerate(sizes):
                if size == widest:
                    sizes[n] -= 1
                    width = sum(sizes) + len(sizes) - 1
                    break
        return sizes

    output = []
    template = ""

    if type(rows[0]) is str:
        rows = [rows, ]
    short_sizes = []

    # automatically shrink columns to the minimum required for the longest data if not longer than
    #   specified size
    for n, s in enumerate(sizes):
        max_size = s
        h_len = len(headers[n])
        size = h_len if h_len < max_size else max_size
        for r in rows:
            s_len = len(str(r[n])) if len(str(r[n])) < max_size else max_size
            size = s_len if s_len > size else size
        short_sizes.append(size)

    short_sizes = fit_to_term()

    for size in short_sizes:
        template += "{:<"+str(size)+"} "

    def process_row(row):
        while any(row):
            line = []
            rest = []
            for n, s in enumerate(row):
                line.append(str(s)[:short_sizes[n]])
                rest.append(str(s)[short_sizes[n]:])
            output.append(template.format(*line))
            row = rest

    process_row(headers)
    dashes = ['-'*s for s in short_sizes]
    process_row(dashes)


    for row in rows:
        process_row(row)

    for o in output:
        print(o)
        
"""
#
# header = ['name','id','keywords']
# rows = [['aabcdefghijklmnopqrstuvwxyz','babcdefghijklmnopqrstuvwxyz','cabcdefghijklmnopqrstuvwxyz'],
#         ['dabcdefghijklmnopqrstuvwxyz', 'eabcdefghijklmnopqrstuvwxyz', 'fabcdefghijklmnopqrstuvwxyz'],
#         ['aabcdefghijklmnopqrstuvwxyz','babcdefghijklmnopqrstuvwxyz','cabcdefghijklmnopqrstuvwxyz'],
#         ['dabcdefghijklmnopqrstuvwxyz', 'eabcdefghijklmnopqrstuvwxyz', 'fabcdefghijklmnopqrstuvwxyz']]
# print_table(header, rows, (15, 10, 7))
name            id         keyword
                           s 
--------------- ---------- ------- 
aabcdefghijklmn babcdefghi cabcdef 
opqrstuvwxyz    jklmnopqrs ghijklm 
                tuvwxyz    nopqrst 
                           uvwxyz  
dabcdefghijklmn eabcdefghi fabcdef 
opqrstuvwxyz    jklmnopqrs ghijklm 
                tuvwxyz    nopqrst 
                           uvwxyz  
aabcdefghijklmn babcdefghi cabcdef 
opqrstuvwxyz    jklmnopqrs ghijklm 
                tuvwxyz    nopqrst 
                           uvwxyz  
dabcdefghijklmn eabcdefghi fabcdef 
opqrstuvwxyz    jklmnopqrs ghijklm 
                tuvwxyz    nopqrst 
                           uvwxyz  
"""