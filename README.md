# World Heritage applications on the web
## World Heritage browser
It is intended to replace the aged KML format of the annual World Heritage spatial data release.
Off the shelf esri solution with arcgisonline subscription
- here is the [link] (http://goo.gl/xur7mL) to the application

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

### Background
Land cover is the baseline biogeophysical characteristics underpinning habitats which biodiversity depends on. The monitoring of its change throughout time offers a unique window into how world’s habitats are increasingly being modified by anthropogenic activities. Natural World Heritage sites, often revered as crown jewels of the world’s most outstanding natural places, are no exception to such changes despite their stringent protection, in the face of conflicting interests from mankind. To date, a plethora of case studies have been undertaken to investigate land cover change within these sites, usually by means of remote sensing and done in an ad-hoc fashion. However, comprehensive studies that consider the entire natural World Heritage network has not been possible due to the lack of technical capacity to analyse exhaustively for every site. 
Globeland30, a new product released by NGCC, presents new opportunities at an unprecedented resolution spatially and temporally for natural World Heritage sites for land cover change detection.

### Data and methodology

The size and complexity of the data presented a significant challenge to the existing hardware and methods for analysis. The data is sorted by tiles according to their geographic extent and can be referenced by an index shapefile and each tile is projected to its corresponding UTM zone. There are two time epochs in the data, namely land cover 2000 and land cover 2010, each at 30 meter resolution, however, there appears to be some duplicate scenes, i.e., identical data are present whereas they should be different. There is also a missing tile in the 2000 data (tile ID: N39_60). Another potential issue is that areas between tiles overlap with each other. This does not cause any issue in the visualization however poses a real problem that needs to be taken into account otherwise double counting would occur and invalidate the result.

In light of the many drawbacks of commercial software and the growing capabilities of open source technology from the geospatial community, a choice was made to migrate many esri powered procedures and workflows to using open source libraries in order to reduce the heavy dependency on ArcGIS and increased flexibility. More specifically, low level GDAL/ORG libraries (Geospatial Data Abstraction Library and Open GIS Simple Feature Reference Implementation) were used in favour of PostGIS/Postgres, a popular alternative to ArcGIS, because the direct use of these libraries does not limit memory usage and the number of CPU cores used in the calculations, essential for efficiency and future repeatability and scalability. The Python language was chosen as the scripting language and numpy library for large matrix calculations.

The algorithm was largely inspired by the zonal statistics module - rasterstats, developed by perrygeo (https://github.com/perrygeo/python-raster-stats) to 1) calculate the amount of each land cover class and 2) calculate the conversion of each land cover class in 2000 to that in 2010. The central idea is to identify what a pixel of land cover class has changed from 2000 to 2010, and then scale it up to cover the entire set of World Heritage sites and aggregate statistics. The key step was to properly georeference and transform the vector data (polygon boundary) to the raster data (land cover data) and obtain a numpy matrix or two dimensional array of pixels, representing the overlap. Subsequent calculations were carried out using masked array operations to determine the amount of each land cover class. The conversion function was first implemented using a computationally expensive vectorised function but it was superseded by a native numpy string array function for increased performance (see code for detail).

### Thoughts and discussions
The analysis presents an advance in the methods to estimate change over time in the land cover within World Heritage thanks to the latest development in the land cover product by the remote sensing community. The Chinese product has a spatial resolution of the 30 meters, the only product at this fine resolution covering the entire world and consisting of two time epochs that allegedly allow comparison directly, enabling the quantification of land cover composition and change for each World Heritage site.

The question, however, remains the confidence in the result as the input data does not contain any quality assurance information, nor uncertainty estimates. This is testified in a few well known areas where the data has been proven to be inaccurate or wrong (Neil Burgess, personal communication). Other equally valid points of concern in some areas include apparently identical tiles between 2000 and 2010, sharp and noticeable edges between tiles. However, there is report of high level of accuracy in some other areas, such as Ireland (Eugunie). With this said, much more testing should be undertaken to understand better the quality of the underlying data before any conclusion is made. Nevertheless, the findings could be justified, if disclaimers are included where appropriate, attributing the source to NGCC who is ultimately responsible for the data. 

### Frontend development
Easy access and its popularity determines the web remains the best media for communicating findings of such analysis. The tech choice was heavily influenced by the ease of development and in the end, a python web framework Web2py was chosen to be the backend, which is lightweight, easy to deploy and meets all functional requirements. On the client side, many popular javascript libraries were used, including jquery, d3js, leaflet, amongst others to power functions of Sankey chart, and WMS basemaps by the Chinese institute.

