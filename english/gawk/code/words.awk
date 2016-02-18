{
    for (i = 1; i <= NF; i++) {
        words[$i]++;
	}
}

END {
    for (w in words) {
        print words[w], w;
	}
}
