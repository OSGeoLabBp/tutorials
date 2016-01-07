RTKLIB programmal meghatározott pozíciók és a permanens állomás ismert pozíciójának eltérése
============================================================================================
*szerző: Takács Bence (takacs.bence@epito.bme.hu), BME Általános- és Felsőgeodézia Tanszék, utolsó módosítás: 2016. január 7.*

Az előzőekben permanens állomás nyers méréseit dolgoztuk fel RTKLIB szoftverrel, abszolút helymeghatározásként. Tekintettele arra, hogy a permanens állomások pontot pozíciója ismert, így kiszámolthatjuk az abszolút helymeghatározással meghatározott pozíciók valódi hibáit. Erre most egy awk szkriptet mutatunk be. Az awk linux operációs rendszer alatt elérhető. Windows operációs rendszer alá is telepíthető. Az egyik egyszerű megoldás osgeo4w programcsomag telepítése, majd az awk programot ennek parancssorából tudjuk meghívni.

Az RTKPOST programmal végzett feldolgozás eredményállománya fejlécből és adatokból áll. A fejléc sorok elején % jel található:: 

  % program   : RTKPOST ver.2.4.2
  % inp file  : E:\kutat\rtklib\bute0060.16o
  % inp file  : E:\kutat\rtklib\brdc0060.16n
  % obs start : 2016/01/06 00:00:00.0 GPST (week1878 259200.0s)
  % obs end   : 2016/01/06 23:59:30.0 GPST (week1878 345570.0s)
  % pos mode  : single
  % elev mask : 15.0 deg
  % ionos opt : broadcast
  % tropo opt : saastamoinen
  % ephemeris : broadcast
  %
  % (lat/lon/height=WGS84/ellipsoidal,Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp,ns=# of satellites)
  %  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio
  2016/01/06 00:00:00.000   47.480948244   19.056512467   177.0515   5   5   4.9465   2.9464   8.0844   2.3532   3.9166   4.0832   0.00    0.0
  2016/01/06 00:00:30.000   47.480947993   19.056507472   176.6958   5   5   4.9220   2.9519   8.0474   2.3445   3.9147   4.0482   0.00    0.0
  2016/01/06 00:01:00.000   47.480948162   19.056508639   176.8775   5   5   4.8975   2.9571   8.0103   2.3355   3.9125   4.0132   0.00    0.0
  2016/01/06 00:01:30.000   47.480947143   19.056513251   177.2445   5   5   4.8729   2.9622   7.9733   2.3262   3.9099   3.9781   0.00    0.0
  2016/01/06 00:02:00.000   47.480948018   19.056518484   177.8703   5   5   4.8482   2.9671   7.9363   2.3166   3.9070   3.9430   0.00    0.0

Az adatrész könnyen olvasható, minden sorban egy mérési epochához tartozó eredmények, azaz dátum, idő, meghatározott koordináták, magasság, meghatározás módja, műholdak száma, középhibák található.
