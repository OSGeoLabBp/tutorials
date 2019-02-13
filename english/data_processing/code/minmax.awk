#! /usr/bin/gawk -f
# find minimal and maximal values in a column
# column number can be set from command line: -v col=2
BEGIN { mi = 1e10; ma = -1e10;
  if (col+0 == 0) { col = 1; }	# is col defined?
}
{ if (NF >= col) {
    if ($col < mi) { mi = $col; }
    if ($col > ma) { ma = $col; }
  }
} 
END { printf("%.3f %.3f\n", mi, ma); }
