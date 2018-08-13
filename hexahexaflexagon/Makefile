all: worksheet.pdf worksheet-with-sol.pdf

worksheet.pdf: worksheet.tex
	latexmk -pdf $^

worksheet-with-sol.pdf: worksheet.tex 
	latexmk -pdf worksheet-with-sol
