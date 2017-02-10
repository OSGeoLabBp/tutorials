# get a slide from point cloud perpendicular to one of the axis
# of the co-ordinate system with a tolerance
# parameters
#   coo - fix coordinate for slide
#   col - column to test from input file
#   tol - tolerance
BEGIN { if (coo+0 == 0) { coo = 1000; }
        if (tol+0 == 0) { tol = 0.2; }
		if (col+0 == 0) { col = 3; }
		mi = coo - tol / 2;
		ma = coo + tol / 2;
}
{  if (NF >= col) {
		if ($col > mi && $col < ma) { print $0; }
   }
}
