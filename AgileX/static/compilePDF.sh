#!/bin/sh
cd Modules/

cp ../tex/headerPDF.txt currentTex.txt

for var in $@
do
    echo "$var"
    cat $var/$var.txt >> currentTex.txt
done

cat ../tex/footer.txt >> currentTex.txt

TEXINPUTS=".;../tex//;%LocalAppData%/Programs/MiKTeX/tex//;$TEXINPUTS" pdflatex currentTex.txt
files="$(ls -I.git -I?.txt -I*.html -I*.css -I*.pdf -I*.json -p | grep -v /)"
rm $files
cd ..