jQuery(function( $ ){
	/**
	 * Demo binding and preparation, no need to read this part
	 */
	//borrowed from jQuery easing plugin
	//http://gsgd.co.uk/sandbox/jquery.easing.php
	$.easing.elasout = function(x, t, b, c, d) {
		var s=1.70158;var p=0;var a=c;
		if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
		if (a < Math.abs(c)) { a=c; var s=p/4; }
		else var s = p/(2*Math.PI) * Math.asin (c/a);
		return a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b;
	};
	// back links
	$('a.back').click(function(){
		$(this).parents('div.pane').scrollTo( 0, 800, { queue:true } );
		$(this).parents('div.section').find('span.message').text( this.title );
		return false;
	});
	//just for the example, to stop the click on the links.
	$('ul.links').click(function(e){
		e.preventDefault();
		var link = e.target;
		link.blur();
		if( link.title )
			$(this).parent().find('span.message').text(link.title);
	});
	
	// This one is important, many browsers don't reset scroll on refreshes
	// Reset all scrollable panes to (0,0)
	$('div.pane').scrollTo( 0 );
	// Reset the screen to (0,0)
	$.scrollTo( 0 );
	
	// TOC, shows how to scroll the whole window
	$('#toc a').click(function(){//$.scrollTo works EXACTLY the same way, but scrolls the whole screen
		$.scrollTo( this.hash, 1500, { easing:'elasout' });
		$(this.hash).find('span.message').text( this.title );
		return false;
	});
	
	// Target examples bindings
	// THIS DEMO IS NOT INTENDED TO SHOW HOW TO CODE IT
	// JUST THE MULTIPLE OPTIONS. THIS CODE IS UGLY.
	var $paneTarget = $('#pane-target');
	
	$('#relative-selector').click(function(){
		$paneTarget.stop().scrollTo( 'li:eq(14)', 800 );
	});
	$('#jquery-object').click(function(){
		var $target = $paneTarget.find('li:eq(14)');
		$paneTarget.stop().scrollTo( $target , 800 );
	});
	$('#dom-element').click(function(){
		var target = $paneTarget.find('ul').get(0).childNodes[20];
		$paneTarget.stop().scrollTo( target, 800 );
	});
	$('#absolute-number').click(function(){
		$paneTarget.stop().scrollTo( 150, 800 );
	});
	$('#absolute-number-hash').click(function(){
		$paneTarget.stop().scrollTo( { top:800,left:700} , 800 );
	});
	$('#absolute-position').click(function(){
		$paneTarget.stop().scrollTo( '520px', 800 );
	});
	$('#absolute-position-hash').click(function(){
		$paneTarget.stop().scrollTo( {top:'110px',left:'290px'}, 800 );
	});
	$('#relative-position').click(function(){
		$paneTarget.stop().scrollTo( '+=100', 500 );
	});
	$('#relative-position-hash').click(function(){				
		$paneTarget.stop().scrollTo( {top:'-=100px',left:'+=100'}, 500 );
	});
	
	$('#percentage-position').click(function(){				
		$paneTarget.stop().scrollTo( '50%', 800 );
	});
	
	// Options examples bindings, they will all scroll to the same place, with different options
	function reset_o(){//before each animation, reset to (0,0), skip this.
		$paneOptions.stop(true).attr({scrollLeft:0, scrollTop:0});
	};
	var $paneOptions = $('#pane-options');
	
	$('#options-no').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000 );
	});
	$('#options-axis').click(function(){// only scroll horizontally
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { axis:'x' } );
	});
	$('#options-duration').click(function(){// it's the same as specifying it in the 2nd argument
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', { duration: 3000 } );
	});
	$('#options-easing').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 2500, { easing:'elasout' } );
	});
	$('#options-margin').click(function(){//scroll to the "outer" position of the element
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { margin:true } );
	});
	$('#options-offset').click(function(){//same as { top:-50, left:-50 }
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { offset:-50 } );
	});
	$('#options-offset-hash').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { offset:{ top:-5,left:-30 } });
	});
	$('#options-over').click(function(){//same as { top:-50, left:-50 }
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { over:0.5 });
	});
	$('#options-over-hash').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1000, { over:{ top:0.2, left:-0.5 } });
	});
	$('#options-queue').click(function(){//in this case, having 'axis' as 'xy' or 'yx' matters.
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 2000, { queue:true });
	});
	$('#options-onAfter').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 2000, { 
			onAfter:function(){
				$('#options-message').text('Got there!');
			}
		});
	});
	// onAfterFirst exists only when queuing
	$('#options-onAfterFirst').click(function(){
		reset_o(); $paneOptions.scrollTo( 'li:eq(15)', 1600, { 
			queue:true,
			onAfterFirst:function(){
				$('#options-message').text('Got there horizontally!');
			},
			onAfter:function(){
				$('#options-message').text('Got there vertically!');
			}
		});
	});
});