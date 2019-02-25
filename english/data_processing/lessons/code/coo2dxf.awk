#!/usr/bin/gawk -f
#
# create dxf file from space separated coordinate list
# Zoltan Siki siki.zoltan@epito.bme.hu
# usage:
#        gawk -f coo2dxf.awk coodinate_list > dxf_file

BEGIN { FS="[ ]";
    # minimal DXF header
    print "  0";
    print "SECTION";
    print "  2";
    print "ENTITIES"
}
{ # for each input line
    print "  0\nTEXT\n  8\nPTEXT\n 10"; # point id text & layer
    print $2 + 0.1;   # text position
    print " 20";
    print $3 - 0.25;
    print " 30\n0.00\n 40\n0.5\n  1";
    print $1
    print " 50\n0.00"
    print "  0\nPOINT\n  8\nPOINT";  # point entity & layer
    print " 10";  # position
    print $2;
    print " 20";
    print $3;
    print " 30";
    print $4
}
END {
    # footer for DXF
    print "  0\nENDSEC\n  0\nEOF"
}
