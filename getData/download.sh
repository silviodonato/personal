#/bin/bash
s="A"
for i in $(seq 1929 2017);
    do
    for s in A B;
    do
        j=$(($i+1))
        file_="web/"$i"_"$s".html"
        site="it.wikipedia.org/wiki/Serie_"$s"_"$i"-"$j
        echo $file_
        echo $site
        rm -f $file_ && wget $site -O $file_ &
    done
done    


#rm -f 2010.html
#wget http://www.gazzetta.it/speciali/risultati_classifiche/2010/calcio/seriea/calendario.shtml -O web/2010.html
