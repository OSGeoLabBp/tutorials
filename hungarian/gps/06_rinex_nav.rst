Felmerült a feladat, hogy egy 2.1 verziójú rinex navigációs állományból keressük ki egy adott műhold, adott időpontra vonatkozó navigációs adatait! Ebben a segédanyagban lépésről-lépésre bemutatjuk hogyan oldható meg a feladat octave szkripttel. A segédletet tlejesen kezdőknek is ajánljuk.

1. Először írjunk egy szkriptet, ami sorról sorra végiolvassa a rinex formátumú navigációs állományunkat, bár megjegyezzük, hogy ez az alap szkript bármilyen text fájl beolvasására alkalmazható. 

fid = fopen ("brdc1520.15n", "r");
while (! feof (fid) )
  text_line = fgetl (fid);
endwhile
fclose (fid);


