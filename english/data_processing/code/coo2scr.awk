BEGIN { FS="[ ]";  # field separator is space
}
{ # for each line of input file
    # point id text
    printf "TEXT %.3f,%.3f\n", $2+0.1, $3-0.25;  # position of text
    printf "0.25 0\n";  # size and angle of text
    printf "%s\n", $1;  # Cannotation text
    printf "POINT %.3f,%.3f,%.3f\n", $2, $3, $4;  # point symbol
}
