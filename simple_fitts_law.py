import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 
import math

csv_file = open('study_data.csv', "r")
distance = []
width = []
index_difficulty = [] # index of difficulty
c_time = []           # completion time (or movement time)
data =[]

## Read csv file
for line in csv_file:
    this_line = line.replace("\n","").split(",")
    this_line = [float(i) for i in this_line]
    distance.append(this_line[0])
    width.append(this_line[1])
    width.append(this_line[1])
    # Calculate Index of Difficulty
    i_d = math.log(this_line[0] / this_line[1] +1 ,2)
    index_difficulty.append(i_d)
    c_time.append(this_line[2])

data = np.array([index_difficulty, c_time])
x, y = data[0], data[1]
plt.scatter(x, y, color='black')
plt.title('Raw data distribution')
plt.xlabel('Index of difficulty')
plt.ylabel('MT')
plt.savefig('raw_data.png')
plt.close()

## Robust line fitting

## The Ransac Function ##
## DON'T TOUCH THIS!   ##
def ransac(steps, threshold):
    x_line = np.array([0,0])
    y_line = np.array([0,0])
    inliers_count = 0
    for step_count in range (steps):
        # Get random 2 points
        idx1 = np.random.randint(0,len(data[0]))
        idx2 = np.random.randint(0,len(data[0]))
        while (idx1 == idx2):
            idx2 = np.random.randint(0,len(data[0]))
        # Get the line (ax+by=d) based on the 2 points
        xs = np.array([data[0][idx1],data[0][idx2]])
        ys = np.array([data[1][idx1],data[1][idx2]])
        tmp_a = (ys[1]-ys[0])/(xs[1]-xs[0])
        tmp_b = -1
        magnitude = np.sqrt(tmp_a**2+tmp_b**2)
        tmp_a = tmp_a / magnitude
        tmp_b = tmp_b / magnitude
        tmp_d = tmp_a*xs[0] + tmp_b*ys[0]
        
        inliers_x = []
        inliers_y = []
        outliers_x = []
        outliers_y = []
        # determine the number of inliers and also outliers
        for i in range(len(data[0])):
            # get distance from a point to the line
            tmp_dot = [data[0][i],data[1][i]]
            dissqr = (data[0][i]*tmp_a + data[1][i]*tmp_b- tmp_d)**2
            # categorizing inliers and outliers
            if (dissqr < threshold**2):
                inliers_x.append(tmp_dot[0])
                inliers_y.append(tmp_dot[1])
            else:
                outliers_x.append(tmp_dot[0])
                outliers_y.append(tmp_dot[1])
        if (len(inliers_x) > inliers_count):
            x_line = xs
            y_line = ys
            inliers_count = len(inliers_x)
    return (x_line, y_line, inliers_count)
## The Ransac Function Ends Here ##

## Set the N steps and the threshold
## YOU CAN TUNE THESE TWO VALUES TO EFFECTIVELY REMOVE OUTLIERS! ##
steps = 2000
thres = 1

## Calculating ransac which returns the final 2 points and the count of inliers
x_model, y_model, inliers_n = ransac(steps,thres)

## Based on the 2 points calculating the inliers again 
# Get the line (ax+by=d) based on the final 2 points
tmpp_a = (y_model[1]-y_model[0])/(x_model[1]-x_model[0])
tmpp_b = -1
magnitude = np.sqrt(tmpp_a**2+tmpp_b**2)
tmpp_a = tmpp_a / magnitude
tmpp_b = tmpp_b / magnitude
tmpp_d = tmpp_a*x_model[0] + tmpp_b*y_model[0]
inliers_x = []
inliers_y = []
outliers_x = []
outliers_y = []
# determine the number of final inliers and outliers
for i in range(len(data[0])):
    # get distance from a point to the line
    tmp_dot = [data[0][i],data[1][i]]
    dissqr = (data[0][i]*tmpp_a + data[1][i]*tmpp_b- tmpp_d)**2
    # categorizing inliers and outliers
    if (dissqr < thres**2):
        inliers_x.append(tmp_dot[0])
        inliers_y.append(tmp_dot[1])
    else:
        outliers_x.append(tmp_dot[0])
        outliers_y.append(tmp_dot[1])
inliers_final = np.array([inliers_x, inliers_y])
outliers_final = np.array([outliers_x, outliers_y])

inliers_x = np.array(inliers_x).reshape((-1,1))
inliers_y = np.array(inliers_y)


###### THE ONLY ACTUALLY FITTS' LAW FITTING PART
###### Refit the inliers based on total least square method 
model = LinearRegression()
model.fit(inliers_x, inliers_y)
fl_a = model.intercept_
fl_b = model.coef_[0]
r_sq = model.score(inliers_x, inliers_y)
print ('coefficient to determination: ', r_sq)
print ('a in fitts law (intercept): ', fl_a)
print ('b in fitts law (slope): ', fl_b)

###### Plotting the final outcome
print ("")
print ("Red dots are the", inliers_n, "inliers contributes the final fitting, and the blue ones are the",len(data[0])-inliers_n, "outliers.")
#plt.plot(data[0], data[0]*slope_final + intercept, 'r')
plt.plot(inliers_x, model.predict(inliers_x), color='black')
plt.scatter(inliers_final[0], inliers_final[1], color = 'black')
plt.scatter(outliers_final[0], outliers_final[1], color = 'red')
plt.title('Final distribution')
plt.xlabel('Index of difficulty')
plt.ylabel('MT')
plt.savefig('fitts_law.png')
