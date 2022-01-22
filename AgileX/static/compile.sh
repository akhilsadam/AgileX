#!/bin/sh
cd Modules/$1/
cat ../../tex/header.txt ../../tex/headerPDF.txt $1.txt ../../tex/footer.txt > currentTex.tex
#setx TEXINPUTS .:$PWD/../../tex/:
#TEXINPUTS=.;../../tex/;
TEXINPUTS=".;../../tex//;%LocalAppData%/Programs/MiKTeX/tex//;$TEXINPUTS" htlatex currentTex.tex
cat ../../tex/def.css >> currentTex.css
files="$(ls -I.git -I?.txt -I*.html -I*.css -I*.json)"
rm $files
cd ..