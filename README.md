# Image_Overlaying_Using_Perspective_Transform
Using the concept of Perspective Transform to overlay one image onto another with OpenCV-Python  

In this project, we use opencv to warp an image and merge it with another image. For more details
you can refer to my article on Medium [here].

<img src ='base_img.jpg' width = 300 height=250> <img src ='subject.jpg' width = 300>  

## Output:
<img src ='images/Final_Output.png' width = 300 height=250>

## Usage:

To run without debug enabled :-  
`python main.py --base_img base_img.jpg --subject_img subject.jpg`

To run with debug enabled :-  
`python main.py --base_img base_img.jpg --subject_img subject.jpg --debug True`

Enabling debug would allow you to visualize the intermediate masks and processed images so that 
you can better analyze where you're going wrong and remedy the problem accordingly.


Do let me know if you face any issues. I'll do my best to help :)  
Happy Learning People ! Keep chasing your dreams ! ⭐️
