/^G[0-9][0-9]/ {
	numGPS++;
}
/^R[0-9][0-9]/ {
	numGLO++;
}
/^E[0-9][0-9]/ {
	numGAL++;
}
/^C[0-9][0-9]/ {
	numBDS++;
}
END {
	print FILENAME, numGPS, numGLO, numGAL, numBDS;
}