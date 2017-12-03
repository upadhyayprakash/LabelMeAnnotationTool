LabelMe annotation tool source code
===========

LabelMe is a Web Application written in JavaScript which can be used for Image annotation. The source-code can be downloaded an run on the server capable of hosting perl runtime along with specific requirements for python. An ubuntu 16.04 based installation should have these by default.

# DOWNLOAD:

You can clone/download the project here:https://github.com/upadhyayprakash/LabelMe2.git

# STEPS:
1.	Git clone code.
		Git Repo link: https://github.com/upadhyayprakash/LabelMe2.git
      
      Create a docker image of git repo by following the configuration in "Dockerfile" file.
      
2.	Start a LabelMe containerized service by volume sharing "Data" folder in host which has 2 main folders "Images" and "Annotation" inside. That should show as /Data folder inside the container.

   	a. Create a Container Service. Execute,
      		
         	sudo nvidia-docker run -it --name <container_name> -p 8282:80 -v /face_data/LabelMeAnnotationTool/Data/:/var/www/html/Data <docker_image_id>
   
      	E.g.
         	sudo nvidia-docker run -it --name i319452_labelme -p 8282:80 -v /face_data/LabelMeAnnotationTool/Data/:/var/www/html/Data cf2e34b6a1fd
      
         You shall note down the Container ID of the newly created sevice.
      
   	b. After this execute the "docker start" command to start the newly created container service. Execute,
         
         	"docker start <container_id>"
      
   	c. Post which, enter inside the container environment. Execute,
         
         	"docker exec -it <container_id> bash"
      
      	You can come-out of container using CTRL+P+Q key combination or CMD+P+Q in case of MAC.
		
3.	Now in the host machine, put 2 image in the Data/Images folder in the host. One image has 1 person and another image has more than 1 persons.
		Path to Store Images:
			"/Data/Images/" in aws host machine.
			
4. 	Run the populate_dirlist.sh script from project folder
		
		sudo ./populate_dirlist.sh
		
	you can see the changes in the "/Data/DirLists/labelme.txt" file
	
4.	Go to LabelMe service and annotate
	
	Access the LabelMe web service at: http://ec2-54-255-172-202.ap-southeast-1.compute.amazonaws.com:8181/tool.html
	You will be shown an image. Use the Bounding Box control from the left menu and Annotate individual Person from the image.
	
5.	Check that Annotation XML files are created in the "Data/Annotations/" folder for every image you annotated.

6.	Run code to take a list of images (in this case 2) in "/Data/Images/" folder and generate multiple images depending on number of people in the images. Execute from project folder,
		
		sudo ./transform.py
	
	The outcome of the run can be seen in the "/Data/SelectedImages" folder. Also you can see the Pascal VOC format of the annotation XML files in the "/Data/Annotations/PVOC/" folder. These are used later for training and configuration purpose.
	
7.	Run "config_gen.sh" script from project folder to generate "example.json" file based on the images copies created in last step.
	
		sudo ./config_gen.sh
		
	Give argument as path to newly copied image folder, ie. "Data/SelectedImages/"
	
	This will generate the example.json file in the "/Data/SelectedImages/Config/" folder.

8.	Make sure you're able to access the JS Annotator Tool at link:
		
		https://s3.ap-south-1.amazonaws.com/js-image-annotator/js-segment-annotator-master/index.html
		
	Alternatively, you can clone the git repo <link> to host the repo in AWS S3 under a bucket.
	
9.	Push the image copies and the example.json file from AWS host to S3 bucket.
	For this, an appropriate settings have to be done in AWS host which will sync images and example.json to "/data/images/" folder of JS Annotator tool hosted on S3.
	
	Currently, the settings are enabled. So, to actually sync the data, execute these two command,
	For Images,
	
		sudo aws s3 sync /face_data/LabelMeAnnotationTool/Data/SelectedImages/ s3://js-image-annotator/js-segment-annotator-master/data/images/
		
	For example.json Config file
	
		sudo aws s3 sync /face_data/LabelMeAnnotationTool/Data/SelectedImages/Config/ s3://js-image-annotator/js-segment-annotator-master/data/
		
	with this step, you should be able to start with image segmentation in JS Annotation tool.

10.	Start Image Segmentation Service here: https://s3.ap-south-1.amazonaws.com/js-image-annotator/js-segment-annotator-master/index.html

11.	Select an image to go in edit mode. Then, select label from right panel, and annotate the specific person on the image which has a bounding box around it. You should be able to select the region on the image and color the different parts based on labels.

12.	Once you're done with labeling the images objects, click on "Export" button. This will save the Image Masks in S3 bucket. You can refresh the page or go to "index" link to see the saved image masks. You can edit the already annotated images as well.

13. You're Done!



### CONTENTS Description:
* tool.html - Main web page for LabelMe annotation tool.
* annotator.sh - Shell script used to create the example.json config file for JS Annotator usage.
* populate_dirlist.sh - Shell script used to create the list of image names and their corresponding path as a 1st Step in the LabelMe tool. The list generated is used to render the images on the Web App for manual annotation.
* transform.py - Python script to convert the generated XML Annotations file to Pascal VOC (PVOC) format. The outcome of the script run are stored in the Data/Annotations/PVOC. Additionally the script also makes copies of original images of Data/Images/ folder into the Data/SelectedImages based on the identified objects(Bounding Boxes) in an individual images.
* Data/Images - This is where your images are stored under multiple hierarchy.
* Data/Annotations - This is where the generated XML annotations are collected in similar hierarchy as Images.
* Data/SelectedImages - This is where the final Images are stored by copying the original images multiple times based on count of the objects defined under the annotated XML files of individual images.
* Data/SelectedImages/Config/example.json - JSON config file which is generated using the annotator.sh script based on the number of images under the Data/SelectedImages folder
* Data/SelectedImages/Config/labels.txt - This is where the labels of the Annotation are stored to be used by the annotator.sh script while generating the example.json file
* Scribbles - This is where the scribbles are collected (scribble mode).
* annotationTools - Directory with source code.
* annotationCache - Location of temporary files.
* Icons - Icons used on web page.


### QUICK INSTALLATION INSTRUCTIONS:

1. Put LabelMe annotation tool code on web server (see web server
   configuration requirements below).

2. On the command line run:

   ``` sh
   $ make
   ```

   This will set a global variable that the perl scripts
   need.  ***Note*** If you move the location of the code, then you
   need to re-run "make" to refresh the global variable.

3. Create a subfolder inside the "Images" folder and place your images
   there.  For example: "Images/example_folder/img1.jpg".  Make sure
   all of your images have a ".jpg" extension and the
   folders/filenames have alphanumeric characters (i.e. no spaces or
   funny characters).

4. Point your web browser to the following URL: 

   http://www.yourserver.edu/path/to/LabelMe/tool.html?collection=LabelMe&mode=f&folder=example_folder&image=img1.jpg

5. Label your image.  Press "show me another image" to go to the next
   image in the folder.

6. Voila!  Your annotations will appear inside of the "Annotations" folder.


### WEB SERVER REQUIREMENTS:

You will need the following to set up the LabelMe tool on your web
server:

* Run an Apache server (see special configuration instructions for
  [Ubuntu](UBUNTU.md) or [Windows](WINDOWS.md)).
* Enable authconfig in Apache so that server side includes (SSI) will
  work. This will allow SVG drawing capabilities. This is the most
  common source of errors, so make sure this step is working.
* Allow perl/CGI scripts to run.  This is the second most common
  source of errors.
* Make sure the php5 and libapache2-mod-php5 libraries are
  installed. You can install them on Linux by running the following:

   ``` sh
   $ sudo apt-get install php5 libapache2-mod-php5
   ```

* (Optional) See special configuration instructions if you are
  installing on [Ubuntu](UBUNTU.md) or [Windows](WINDOWS.md).

If you are not able to draw polygons, check to see if the page is
loaded as an "application/xhtml+xml" page (you can see this in
Firefox by navigating to Tools->Page Info). If it is not, be sure
that SSI are enabled (see above for enabling authconfig in Apache).

Make sure that your images have read permissions on your web server
and folders in the "Annotations" folder have write permissions. Also,
"annotationCache/TmpAnnotations" needs to have write permissions.


### FEATURES OF THE ANNOTATION TOOL:

* The following are URL variables you can pass to the annotation tool:

   * mode=im - Only show the image and drawing canvas (do not show anything outside of the image.
   * mode=mt - Mechanical Turk mode.
   * mode=f - Pressing "next image" button goes to next image in the folder.
   * mode=i - Pressing "next image" button goes to random image in the default LabelMe collection.
   * mode=c - Go to next image in the collection (set via the dirlist).
   * username=johndoe - Sets username for labeling session.
   * collection=LabelMe - Uses the default LabelMe collection list. See below for setting up a new collection list.
   * folder=MyLabelMeFolder - LabelMe folder where the image lives.
   * image=image.jpg - LabelMe image to annotate.
   * objects=car,person,building - When popup bubble appears asking the user for the object name, the user selects one of these objects appearing as a drop-down list.
   * scribble=false - Turns off scribble mode.
   * objlist=visible - This controls whether the object list on the right side is visible or not. Use "objlist=hidden" to make it hidden.
   * actions=n - Control what actions the user is allowed to do. To set the desired actions, use any combination of the letters below. For example, to allow renaming, modify control points, and delete actions, then set "actions=rmd". By default, "actions=n". The following are possible actions:
      * n - create and edit new polygons
      * r - rename existing objects
      * m - modify control points on existing objects
      * d - delete existing objects
      * a - allow all actions
      * v - view polygons only (do not allow any editing)
   * viewobj=e - Control which objects the user sees. Use one of the following possible options below. By default, "viewobj=e". Note that for deleted objects, these will be shown in gray and the object name in the object list will be italicized.
      * e - view new and previously labeled objects
      * n - view new objects only
      * d - view new and deleted objects
      * a - view all objects (new, existing, deleted)

   The following are for Mechanical Turk mode:

   * mt_sandbox=true - Use Mechanical Turk sandbox mode. This mode is used for debugging on Mechanical Turk. You may want to start with this variable set to make sure everything works.
   * N=5 - The worker is required to label at least 5 polygons. Use N=inf to allow the worker to label as many as they want.
   * mt_intro=http://yourpage.com - You may customize the instructions that the worker sees. By default, the following [instructions](http://labelme2.csail.mit.edu/Release3.0/annotationTools/html/mt_instructions.html) are given to the workers.
   * mt_instructions=Place your instructions here - You may customize the one-line instructions that the worker sees at the top of the labeling task. By default, the instructions are: Please label as many objects as you want in this image.

* You can create a collection of images to label by running the
  following on the command line:

   ``` sh
   $ cd ./annotationTools/sh/
   $ ./populate_dirlist.sh
   ```

  This will create a list of all images inside the "./Images" folder,
  and will appear inside the file "./annotationCache/DirLists/labelme.txt".

  You can then label images inside the collection using the following URL:

   http://www.yourserver.edu/path/to/LabelMe/tool.html?collection=labelme&mode=i

  You can create a collection consisting of a particular folder by
  running the following from the command line:

   ``` sh
   $ cd ./annotationTools/sh/
   $ ./populate_dirlist.sh my_collection.txt example_folder
   ```

  The list will appear inside
  "./annotationCache/DirLists/my_collection.txt".  You can then
  label images inside the collection using the following URL:

   http://www.yourserver.edu/path/to/LabelMe/tool.html?collection=my_collection&mode=i

* You can change the layout of the annotation files for your
  collection by modifying the XML file template inside of
  "./annotationCache/XMLTemplates/your_collection.xml".  The default
  template is "./annotationCache/XMLTemplates/labelme.xml".

* A log file of the annotation tool actions are recorded in
  "./annotationCache/Logs/logfile.txt".  Make sure that this file has
  write permissions.


### CODE API

The following is a brief overview of the source code.  Please see the
[Javascript code API](http://<hostname>:<port>/annotationTools/js/api/index.html) for more details.
   

* tool.html - This is the entry point for the annotation tool.  The main
functionality is to insert all of the javascript code and lay down the
drawing canvases.

* annotationTools/js/ - This folder contains all of the javascript
code for the annotation tool functionalities.
We provide the [code API](http://<hostname>:<port>/annotationTools/js/api/index.html)
for the Javascript source code, which has been automatically extracted
from the source code comments.

* annotationTools/perl/ - This folder contains all of the Perl
scripts used for communication with the server back-end.

* annotationTools/css/ - This folder contains all of the CSS style
definitions.

* annotationTools/html/ - This folder contains auxillary HTML files
(e.g. for Mechanical Turk instructions, etc.).
