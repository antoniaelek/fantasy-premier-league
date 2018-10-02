/*
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$nav = $('#nav');
		
		//compare
	function compare(id){
			var if1 = document.getElementById('plstats1');
			var doc1 = (if1.contentDocument) ? if1.contentDocument : if1.contentWindow.document;
			var if2 = document.getElementById('plstats2');
			var doc2 = (if2.contentDocument) ? if2.contentDocument : if2.contentWindow.document;
			
			var bs1 = parseFloat(doc1.getElementById(id).innerHTML);
			var bs2 = parseFloat(doc2.getElementById(id).innerHTML);

			var p1 = doc1.getElementById(id).parentElement;
			var arr1 = p1.childNodes[2];

			var p2 = doc2.getElementById(id).parentElement;
			var arr2 = p2.childNodes[2];
			
			if (bs1 < bs2) {
				arr1.innerHTML = "<h3 style='color:red'>&#9660;</h3>"	
				arr2.innerHTML = "<h3 style='color:green'>&#9650;</h3>"
			} else if (bs2 < bs1) {
				arr2.innerHTML = "<h3 style='color:red'>&#9660;</h3>"	
				arr1.innerHTML = "<h3 style='color:green'>&#9650;</h3>"	
			} else {
				arr1.innerHTML = "<h3 style='color:gray'>&#9650;</h3>"	
				arr2.innerHTML = "<h3 style='color:gray'>&#9650;</h3>"	
			}
		};
		
		window.onload = function () { 
			compare('basic_stats');
			compare('quality');
			compare('in_game_stats');
			compare('popularity');
		}
		
		function continueExecution(){
			compare('basic_stats');
			compare('quality');
			compare('in_game_stats');
			compare('popularity');
		}
		$(document).ready(function(){				
			$("#vpc_dropdown").change(function(){
				var newSrc = $(this).val();
				document.getElementById("vpc_plot").src = newSrc + ".html";		
			});
			
			$("#pldropdown1").change(function(){
				var newSrc = $(this).val();
				var startIdx = newSrc.lastIndexOf("_");
				var endIdx = newSrc.length;
				var photoId = newSrc.substring(startIdx+1, endIdx);
				
				var imgurl = "https://platform-static-files.s3.amazonaws.com/premierleague/photos/players/110x140/p"+ photoId +".png";
				document.getElementById("plstats1").src = newSrc + "_text.html";
				document.getElementById("plimg1").src = imgurl;
				document.getElementById("plplots1").src = newSrc + ".html";
				
				setTimeout(continueExecution, 2000)				
			});
			  
			$("#pldropdown2").change(function(){
				var newSrc = $(this).val();
				var startIdx = newSrc.lastIndexOf("_");
				var endIdx = newSrc.length;
				var photoId = newSrc.substring(startIdx+1, endIdx);
				
				var imgurl = "https://platform-static-files.s3.amazonaws.com/premierleague/photos/players/110x140/p"+ photoId +".png";
				document.getElementById("plstats2").src = newSrc + "_text.html";
				document.getElementById("plimg2").src = imgurl;
				document.getElementById("plplots2").src = newSrc + ".html";
								
				setTimeout(continueExecution, 2000)	
			});
		});

	// Breakpoints.
		breakpoints({
			wide:      [ '961px',  '1880px' ],
			normal:    [ '961px',  '1620px' ],
			narrow:    [ '961px',  '1320px' ],
			narrower:  [ '737px',  '960px'  ],
			mobile:    [ null,     '736px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Nav.
		var $nav_a = $nav.find('a');

		$nav_a
			.addClass('scrolly')
			.on('click', function(e) {

				var $this = $(this);

				// External link? Bail.
					if ($this.attr('href').charAt(0) != '#')
						return;

				// Prevent default.
					e.preventDefault();

				// Deactivate all links.
					$nav_a.removeClass('active');

				// Activate link *and* lock it (so Scrollex doesn't try to activate other links as we're scrolling to this one's section).
					$this
						.addClass('active')
						.addClass('active-locked');

			})
			.each(function() {

				var	$this = $(this),
					id = $this.attr('href'),
					$section = $(id);

				// No section for this link? Bail.
					if ($section.length < 1)
						return;

				// Scrollex.
					$section.scrollex({
						mode: 'middle',
						top: '-10vh',
						bottom: '-10vh',
						initialize: function() {

							// Deactivate section.
								$section.addClass('inactive');

						},
						enter: function() {

							// Activate section.
								$section.removeClass('inactive');

							// No locked links? Deactivate all links and activate this section's one.
								if ($nav_a.filter('.active-locked').length == 0) {

									$nav_a.removeClass('active');
									$this.addClass('active');

								}

							// Otherwise, if this section's link is the one that's locked, unlock it.
								else if ($this.hasClass('active-locked'))
									$this.removeClass('active-locked');

						}
					});

			});

	// Scrolly.
		$('.scrolly').scrolly();

	// Header (narrower + mobile).

		// Toggle.
			$(
				'<div id="headerToggle">' +
					'<a href="#header" class="toggle"></a>' +
				'</div>'
			)
				.appendTo($body);

		// Header.
			$('#header')
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'header-visible'
				});

})(jQuery);