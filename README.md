# smart-refrigerator
### Determining the individual weights of objects seen through the camera with the help of Arduino and weight sensors

The main purpose is to determine the weight of the food in the refrigerator and thus to better track the food inside. 

![1](https://user-images.githubusercontent.com/79144571/147954259-fa9a06fa-dab5-4cf0-bfd2-3c03a3023a72.png)

It is possible to calculate the position of an object, placed on a rectangular platform. When we consider the object as the center of gravity, the force applied by the object to each corner will change according to its position. 

![image](https://user-images.githubusercontent.com/79144571/147955027-34a7d7a7-d672-4d5b-bb45-9fdd5822458c.png)



When an object is added (or removed) to the platform, the position where the change occurred can be calculated by measuring the change in forces at the 4 corners. 

It is also possible to calculate the position of objects via the camera. In my case, I have  a platform which I know the sizes. After recognizing the objects, I calculate their positions by proportioning their positions on the camera to the dimensions of the platform.
Next, I match the weight-position pairs from the weight sensors with the positions I get from the camera. 

![image](https://user-images.githubusercontent.com/79144571/147956094-5b9c1954-a259-441c-98d7-0c7e7017ad93.png)

I used the most straightforward ways in this project.
- It uses color contrasts to recognize objects (otsu threshold) 
- It also finds the shortest quadratic distance to match the positions. Instead, it could use an imaginary grid.
- Also, adding two objects at the same time will give wrong results. I have a solution for this that requires an 8x8 matrix, but I can barely explain it. 
