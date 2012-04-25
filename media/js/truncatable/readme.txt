/*-------------------  READ ME ---------------*/

You can now pass in 2 more parameters to the truncatable plugin like so:

	 $('.myClass').truncatable({
	 								limit:200,
	 								more: '.....',
	 								less: true,
	 								hideText: '[hide]'
	 							});
	 							
* less: choose to display a link to hide the truncated text on the page.

*hideText: set what you would like that text to display (only works when less is set to true)

* more: lets you choose what you would like the expanding link to be ie 'read more'

Hope this is helpful, if you spot any bugs please let me know so I can fix them! 

Philip Beel 
http://www.theodin.co.uk
contact@theodin.co.uk