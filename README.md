# World Heritage browser
It is intended to replace the aged KML format of the annual World Heritage spatial data release.
Off the shelf esri solution with arcgisonline subscription
- here is the [link] (http://goo.gl/xur7mL) to the application

# World Heritage applications on the web
## World Heritage datasheet
This is a prototype aimed at replacing the old fashioned way of maintaining the World Hertage datasheets through Microsoft Word. Instead, it would be done entirely online and simplify the way it is published and accessed in the future.
It uses the following software/libraries: Web2py, slugify (Django utility), Bootstrap (+scrollspy), jQuery, python-markdown, bs4, codemirror.

### Currently implemented
- mobile friendly view
- affix sidebar with scroll sense and hyperlinks
- file based read and write
- deployment (AWS EC2 micro instance)
- added GA for tracking traffic
- WYSIWYG editor for updating

### Remaining implmentations
- pan-doc to convert existing datasheet in Word to Markdown
- UI polish

### Working example
- here is the [link](http://52.16.74.158/wh_app/default/wh_html_bs2/191) to the datasheet 

## World Heritage Landcover change
A prototype to visualise Landcovers in 2000 and 2010, including quantitative change. A Sankey chart is also included to visualise conversion matrix, i.e., how much of a certain type of landcover has been converted to another.
It uses the following software/libraries:Web2py, Bootsrap, jQuery, D3js, D3js-Sankey plugin, leaflet. Data courtesy of National Geomatics Centre of China.

### working example
- here is the [link](http://52.16.74.158/wh_app/landcover/) to the landcover change product 
