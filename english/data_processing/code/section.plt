#!/usr/bin/gnuplot
set xlabel "x"
set ylabel "z"
set grid xtics lt 1 lw 1 lc rgb "#bbbbbb"
set grid ytics lt 1 lw 1 lc rgb "#bbbbbb"
set autoscale
set terminal postscript portrait enhanced mono dashed lw 1 'Helvetica' 14
set style line 1 lt 1 lw 3 pt 3 linecolor rgb "red"
set output 'out.eps'
plot 'e1000.txt' using 1:2 w points title "section"
