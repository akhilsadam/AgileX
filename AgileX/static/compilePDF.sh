#!/bin/sh
cd Modules/

cp ../tex/headerPDF.txt currentTex.txt

cat ../tex/spacer.txt ../tex/begin.txt ../tex/spacer.txt authors.txt ../tex/spacer.txt  ../tex/title.txt ../tex/spacer.txt >> currentTex.txt

for var in $@
do
    echo "$var"
    cat $var/$var.txt ../tex/spacer.txt >> currentTex.txt
done

cat ../tex/footer.txt ../tex/spacer.txt >> currentTex.txt

TEXINPUTS=".;../tex//;%LocalAppData%/Programs/MiKTeX/tex//;$TEXINPUTS" pdflatex currentTex.txt
files="$(ls -I.git -I*.txt -I*.html -I*.css -I*.pdf -I*.json -I*.gif -I*.jpg -I*.png -p | grep -v /)"
rm $files
cd ..