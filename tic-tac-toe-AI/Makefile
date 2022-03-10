all:
	ipetoipe -pdf tic-tac-toe-form.ipe
	ipetoipe -pdf tic-tac-toe-opp.ipe
	pdftk tic-tac-toe-form.pdf cat 1-end 1-end output tic-tac-toe-form-2.pdf
	pdftk A=tic-tac-toe-form.pdf B=tic-tac-toe-opp-nup.pdf cat A1 B1west output tic-tac-toe-form-2.pdf
	pdfjam --landscape --nup 2x1 tic-tac-toe-form-2.pdf --outfile tic-tac-toe-worksheet.pdf

