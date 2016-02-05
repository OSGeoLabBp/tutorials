BEGIN { FS="[ ]"; # field sparator is space
    # for units and decimals
    u[0] = 1000;
    u[1] = 1000 * 3.28;
    u[6] = 10000;
    u[7] = 10000 * 3.28;
    u[8] = 100000;
}

/^\*/ { # 16 bytes records
    # point id
    psz = substr($1, 9);
    sub(/^0+/, "", psz) # removing leading zeros
    for (i = 2; i < NF; i++) {  # for each fields
        if (match($i, /^8[123]/)) { # coordinate field
            j = substr($i, 2, 1);  # coordinate code
            s = substr($i, 7, 1) == "+" ? 1 : -1;  # sign
            d = u[substr($i, 6, 1)];  # number of decimals
            w = substr($i, 8, 23);  # coordinate value
            sub(/^0+/, "", w);  # remove leading zeros
            c[j] = w / d * s;
        }
    }
    # print coordinates to standard output
    printf "%s %.3f %.3f %.3f\n", psz, c[1], c[2], c[3]
}
