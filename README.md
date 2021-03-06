# Fitts' Law calculation and RANSAC 

File study_data.csv contains part of the actual study result from Berkeley Fitts Law Dataset (http://automation.berkeley.edu/fitts-dataset/). The code shows how the Fitts' Law coefficients are calculated and visualize the results. 

The calculation is based on wikipedia. In particular the version of Prof. Scott MacKenzie:

![fitts](fitts_equation.png)

In such a case, the Index of Difficulty is log(D/2+1).


## Running the program 

sklearn is required. Then run: 
```bash
python3 simple_fitts_law.py
```

Note that in the dataset (study_data.csv), each line is a task. The first value is distance, the second value is width of target, and the last value is the completion time (MT).

The result before outlier removal will be visualized in the same folder:
![raw](raw_data.png)

The result after outlier removal is as follow. The black dots are the inliers and the red dots are the outliers.
![vis](fitts_law.png)

## RANSAC (Random sample consensus)

Ransac is one of the most most commonly used method to remove outliers; which is especially useful when the data is quite noisy. The program contains RANSAC. You just need to change the iteration number and threshold in line 82, 83.

```bash
## Set the N steps and the threshold
## YOU CAN TUNE THESE TWO VALUES TO EFFECTIVELY REMOVE OUTLIERS! ##
steps = 2000
thres = 1
```

The more steps give, it will find better line. The threshold determines how centered the points should be. Set the threshold high could include more points but potentially include more noisy points as well.