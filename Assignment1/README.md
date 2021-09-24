# Assignment 1

This assignment focuses on finding the intersection of the lines segments using an optimal algorithm. In this assignment, I have implemented the Graham Scan algorithm.

This implementation consists of 4 files:
1. util.py - that contains the classes that I use in the implementation and other util methods that help me read and write to the files. It also has some of the common methods that are needed in both the other files.
2. convexHullGrahamScan.py is the file that contains the implementation of the Graham Scan algorithm
3. convexHullBruteForce.py is the file that has the brute force implementation to find the convex hull of n points.
4. testcaseGenerator.py creates the test cases and puts it in the test folder

Test folder has all the test cases.

In order to run one of the files, use the following command template:

``` python3 convexHullGrahamScan.py test/1000_completelyRandom.txt ```

You can replace the convexHullGrahamScan with convexHullBruteForce and put one of the other test files from the test folder.

### Dependencies:
The program also additionally uses the matplotlib in order to plot the values on a graph