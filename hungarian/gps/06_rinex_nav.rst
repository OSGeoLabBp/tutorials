RINEX navigációs fájlból adatok keresése
========================================

Felmerült a feladat, hogy egy 2.1 verziójú (amerikai) GPS-műholdak adatait tartalmazó RINEX navigációs állományból keressük ki egy adott műhold, adott időpontra vonatkozó navigációs adatait! Ebben a segédanyagban lépésről-lépésre bemutatjuk hogyan oldható meg a feladat octave programban. A segédletet teljesen kezdőknek is ajánljuk.

**1.** Először írjunk egy szkriptet, ami sorról sorra végiolvassa a rinex formátumú navigációs állományunkat, bár megjegyezzük, hogy ez az alap szkript bármilyen text fájl beolvasására alkalmazható::

	fid = fopen ("brdc1520.15n", "r");
	while (! feof (fid) )
		text_line = fgetl (fid);
	endwhile
	fclose (fid);

Az első sorban olvasásra nyitjuk meg a brdc1520.15n állományunkat, a fájlt az 5. sorban zárjuk le. Megnyitán után a while ciklusban amíg a fájl vége jelet el nem érjük, a fgetl parancs segítségével soronként beolvassuk az állomány tartalmát, az aktuális sor tartalmát a text_line változóba tesszük. Egyelőre a beolvasott adatokkal semmit nem kezdünk.

Ha szeretnéd kiíratni az egyes sorok tartalmát a lépernyőre, a text_line = fgetl (fid); sorok végéről töröld ki a ;-t! 

**2.** Ezután alakítsuk át úgy a szkriptünket, hogy a fejléc ("header") sorainak tartalmát ne írja ki, csak a tényleges navigációs adatokat! Ehhez először nézzük meg, hogy az aktuális sor tartalmazza-e az "END OF HEADER" szavakat, ha igen, akkor írja ki az adott sor tartalmát. Ehhez a strfind beépített függvényt használjuk::

	fid = fopen ("brdc1520.15n", "r");
	while (! feof (fid) )
		text_line = fgetl (fid);
		if strfind(text_line, "END OF HEADER") 
			disp(text_line);
		endif
	endwhile
	fclose (fid);
	


