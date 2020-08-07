# A toy version of Fitts' Law

File study_data.csv contains part of the actual study result from Berkeley Fitts Law Dataset (http://automation.berkeley.edu/fitts-dataset/). The code shows how the Fitts' Law coefficients are calculated and visualize the results. 

## Running the program 

sklearn is required. Then run: 
```bash
python3 simple_fitts_law.py
``

The result before outlier removal will be visualized in the same folder:
![raw]('raw_data.png')

The result after outlier removal is:
![vis]('fitts_law.png')