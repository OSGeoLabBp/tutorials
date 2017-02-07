/^[1-9][0-9]{2} / { i = int($1 / 100);	# array index
					sum_x[i] += $2; sum_y[i] += $3; n[i]++; }
END { for (i in n) {
		printf("%d00-%d99: %.3f, %.3f\n", i, i, sum_x[i] / n[i], sum_y[i] / n[i]);
	}
}
