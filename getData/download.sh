


for i in 2010 2011;
    do
    rm -f $i.html && wget http://www.gazzetta.it/speciali/risultati_classifiche/$i/calcio/seriea/calendario.shtml -O web/$i.html &
    rm -f b_$i.html && wget http://www.gazzetta.it/speciali/risultati_classifiche/$i/calcio/serieb/calendario.shtml -O web/b_$i.html &
done    


#rm -f 2010.html
#wget http://www.gazzetta.it/speciali/risultati_classifiche/2010/calcio/seriea/calendario.shtml -O web/2010.html
