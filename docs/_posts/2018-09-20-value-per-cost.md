---
layout: page
title: Value Per Cost Analysis
permalink: /value-per-cost/
---

<head>
	<script>		
		$(document).ready(function(){				
			$("#vpc_dropdown").change(function(){
				var newSrc = $(this).val();
				document.getElementById("vpc_plot").src = newSrc + ".html";		
			});
		});
	</script>
</head>
<body>
	<table stlye="width: 100%">
		<tr>
			<td align="left">
				<select id="vpc_dropdown" style="align: left; margin-left: 30px;">
					<option value="{{ site.baseurl }}/assets/bokeh/value_per_cost">All</option>
					<option value="{{ site.baseurl }}/assets/bokeh/value_per_cost_gkp">Goalkeepers</option>
					<option value="{{ site.baseurl }}/assets/bokeh/value_per_cost_def">Defenders</option>
					<option value="{{ site.baseurl }}/assets/bokeh/value_per_cost_mid">Midfielders</option>
					<option value="{{ site.baseurl }}/assets/bokeh/value_per_cost_fwd">Forwards</option>
				</select>
			</td>
		</tr>
		<tr>
			<td align="middle">
				<iframe id="vpc_plot" src="{{ site.baseurl }}/assets/bokeh/value_per_cost.html"
					width="100%"
					height="610px"
					scrolling="no"
					seamless="seamless"
					frameborder="0">
				</iframe>
			</td>
		</tr>
	</table>
</body>