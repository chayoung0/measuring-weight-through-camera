# measuring-weight-through-camera
### Determining the individual weights of objects seen through the camera with the help of Arduino and weight sensors

The main purpose is to determine the weight of the food in the refrigerator and thus enhance food tracking in smart refrigerators.

![1](https://user-images.githubusercontent.com/79144571/147954259-fa9a06fa-dab5-4cf0-bfd2-3c03a3023a72.png)

It is possible to calculate the position of an object, placed on a rectangular platform. When we consider the object as the center of gravity, the force applied by the object to each corner will change according to its position. 

![image](https://user-images.githubusercontent.com/79144571/147955027-34a7d7a7-d672-4d5b-bb45-9fdd5822458c.png)



Calculating the position of an object on a rectangular platform is achievable by considering the object as the center of gravity. As the object's position changes, the forces applied to each corner of the platform also vary accordingly. Whenever an object is added or removed from the platform, it is possible to calculate the position of the change by measuring the force differences at the four corners.

Utilizing a camera, it is also feasible to calculate the positions of objects. In this case, a known-sized platform is used as a reference. By recognizing the objects within the camera view, their positions can be determined by proportionally mapping their positions to the platform's dimensions. Subsequently, the weight-position pairs obtained from the weight sensors are matched with the camera-derived positions.

![image](https://user-images.githubusercontent.com/79144571/147956094-5b9c1954-a259-441c-98d7-0c7e7017ad93.png)

#### Discussion for Future Work
The project employs straightforward techniques to accomplish these tasks.
- Object recognition relies on color contrast, specifically utilizing the Otsu threshold method.
- To match the positions, the shortest quadratic distance method is utilized, although an alternative approach involving an imaginary grid could be explored.
- One challenge to address is the simultaneous addition of two objects, which may lead to incorrect results. I have a solution for this that requires an 8x8 matrix, but I can barely explain it :D 
