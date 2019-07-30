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
				arr1.innerHTML = "<h3 style='color:white'>&#9660;</h3>"	
				arr2.innerHTML = "<h3 style='color:white'>&#9650;</h3>"
			} else if (bs2 < bs1) {
				arr2.innerHTML = "<h3 style='color:white'>&#9660;</h3>"	
				arr1.innerHTML = "<h3 style='color:white'>&#9650;</h3>"	
			} else {
				arr1.innerHTML = "<h3 style='color:white'>&#9650;</h3>"	
				arr2.innerHTML = "<h3 style='color:white'>&#9650;</h3>"	
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

})(jQuery);