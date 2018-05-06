for i in 1 2 3 4 5 6 7 8 9
do
	x=$(((RANDOM % 10) + 1))
	y=$(((RANDOM % 10) + 1))
	gdal_translate -of PNG -srcwin $x $y 160 260 monalisa.jpg monalisa$i.png
done
