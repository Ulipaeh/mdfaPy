# PyMFDFA

A graphical interface to fractal/multifractal analysis in time series. 

## Install 🔧

1. Install python 3.7 (download link https://www.python.org/downloads/release/python-370/ ), mark "Add to path" option, add click next.

2. Open CMD or Terminal and install packages: numpy, pandas, numba, sklearn, pyqtgraph and pyqt5, with pip install comand:
```
pip install numpy         # enter
pip install pandas        # enter
pip install pyqtgraph   # enter
pip install numba        # enter
pip install sklearn        # enter
```

## Run program ⚙️
1. Locate (with cd comand) interface folder and run python main.py in CMD:
<img width="433" alt="1" src="https://user-images.githubusercontent.com/53945790/113024738-53859880-9144-11eb-8c7b-dc0c24336575.PNG">




## Use PyMFDFA ⌨️
### Automatic Segmentation 
The Program has a tool for the segmentation of series either manual or automatic.

1. Load signal(s) in format 1 column .txt or .csv:
2. Start segmentation button to manual segmentation (Manual segmentation shows 2 lines to select the segment of the series to be analized.): 
<img width="503" alt="2" src="https://user-images.githubusercontent.com/53945790/113024943-95164380-9144-11eb-9385-778751afd41e.PNG">
3. At the end of the process, the files are automatically saved in the folder of the loaded signal

Note: For automatic segmentation, characteristics such as baseline, width, peak size are chosen and it may have errors.


### Detrended Fluctuation Analysis (DFA)
This section can perform DFA:

1. Load signal(s) and select polynomial fit = 1.
<img width="494" alt="dfa1" src="https://user-images.githubusercontent.com/53945790/113025077-bd9e3d80-9144-11eb-9170-4af2da55534f.PNG">
2. Start button.
<img width="610" alt="dfa2" src="https://user-images.githubusercontent.com/53945790/113025137-d3abfe00-9144-11eb-82dd-e59dac3baa42.PNG">
3. The clasification image is saved automatically in the source folder of the time series loaded in a folder called DFA.


###  Multifractal Detrended Fluctuation Analysis (MFDFA)
This section can perform MFDFA with parameters to this experiment:

1. Load signal(s) and select the parameters.
<img width="526" alt="3" src="https://user-images.githubusercontent.com/53945790/113025183-e1fa1a00-9144-11eb-8bb7-ccbc2c522e49.PNG">
2. Start button.
<img width="527" alt="4" src="https://user-images.githubusercontent.com/53945790/113025261-fb02cb00-9144-11eb-8cc8-409979c6b625.PNG">
3. The clasification image is saved in a Excel file.
<img width="842" alt="5" src="https://user-images.githubusercontent.com/53945790/113025377-1ff73e00-9145-11eb-8722-10780de112bc.PNG">

Note: The parameters depends on the characteristics of the times series (size, stationarity, non-stationarity), for this experiment the parameters are those shown in the figure.
