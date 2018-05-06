% image template matching
pkg load image
img = rgb2gray(imread("monalisa.jpg"));
temp = rgb2gray(imread("mona_temp4.png"));
%temp = img(5:6,10:12);
[n, m] = size(img);
[nt, mt] = size(temp);
min_dif = nt * mt * 255;
pos = [0, 0, min_dif];
for i = 1:n - nt
  for j = 1: m - mt
    dif = sum(sum(abs(img(i:i+nt-1, j:j+mt-1) - temp)));
    if dif < min_dif
      pos = [i, j, dif];
      min_dif = dif;
    end
  end
end
pos
