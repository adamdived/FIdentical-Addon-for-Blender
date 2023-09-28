# SelectIdentical 4 Blender
For a project i'm working, i need to optimize for game engines an industrial CAD mesh with gazillion of bolts, washers etc. I needed to separate all these small objects into a new collection and doing it by hand could kill also the most patient person in the world. So this script allows you to select objects in Blender that are identical or similar to the ACTIVE object. It compares the number of vertices and dimensions of each mesh object in the scene with that of the active object, and selects ONLY the objects that match these criteria.

The script starts by defining a tolerance threshold, epsilon, which is used to determine the acceptable percentage difference for dimensions and volume comparisons.

It then iterates over all the objects in the scene and checks if they are of type "MESH". For each mesh object, it compares the number of vertices with the active object. If they have the same number of vertices, it proceeds to further comparisons.

First, it checks if the dimensions of the current object match exactly with the active object's dimensions. If they match, the object is selected.

Next, it calculates the volume of the bounding box for both the active object and the current object. If the percentage difference between their volumes is within the tolerance threshold, the object is selected.

Lastly, it compares each individual dimension of the current object with that of the active object. If the percentage difference for each dimension is within the threshold, the object is selected.
