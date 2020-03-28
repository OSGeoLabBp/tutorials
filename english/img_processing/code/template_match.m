#! /bin/octave
% image template matching minimizing absolute difference
pkg load image
args = argv();        % command line params into a cell array
if nargin > 1
  tnam = args{1};     % first parameter the template image
  inam = args{2};     % second parameter the image
else
  tnam = "mona_temp4.png";
  inam = "monalisa.jpg";
end
img = rgb2gray(imread(inam));   % read and convert to grayscale
temp = rgb2gray(imread(tnam));  % read and convert to grayscale
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
printf("%d %d %d\n", pos(1), pos(2), pos(3));
