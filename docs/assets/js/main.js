/*
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	skel.breakpoints({
		wide: '(min-width: 961px) and (max-width: 1880px)',
		normal: '(min-width: 961px) and (max-width: 1620px)',
		narrow: '(min-width: 961px) and (max-width: 1320px)',
		narrower: '(max-width: 960px)',
		mobile: '(max-width: 736px)'
	});
	
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
		
	$(function() {
		
		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				$body.removeClass('is-loading');
			});

		// CSS polyfills (IE<9).
			if (skel.vars.IEVersion < 9)
				$(':last-child').addClass('last-child');

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on mobile.
			skel.on('+mobile -mobile', function() {
				$.prioritize(
					'.important\\28 mobile\\29',
					skel.breakpoint('mobile').active
				);
			});

		// Scrolly links.
			$('.scrolly').scrolly();

		// Nav.
			var $nav_a = $('#nav a.scrolly');

			// Scrolly-fy links.
				$nav_a
					.scrolly()
					.on('click', function(e) {

						var t = $(this),
							href = t.attr('href');

						if (href[0] != '#')
							return;

						e.preventDefault();

						// Clear active and lock scrollzer until scrolling has stopped
							$nav_a
								.removeClass('active')
								.addClass('scrollzer-locked');

						// Set this link to active
							t.addClass('active');

					});

			// Initialize scrollzer.
				var ids = [];

				$nav_a.each(function() {

					var href = $(this).attr('href');

					if (href[0] != '#')
						return;

					ids.push(href.substring(1));

				});

				$.scrollzer(ids, { pad: 200, lastHack: true });

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

			// Fix: Remove transitions on WP<10 (poor/buggy performance).
				if (skel.vars.os == 'wp' && skel.vars.osVersion < 10)
					$('#headerToggle, #header, #main')
						.css('transition', 'none');

	});

})(jQuery);