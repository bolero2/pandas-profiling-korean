# pandas-profiling-korean
pandas profiling 패키지 사용 시, 그래프 View에서 한글이 나오지 않는 문제를 해결한 것입니다.

# Installation
1. Install **Nanum Font** : `apt install fonts-nanum*`
2. Install python package
```bash
pip install pandas==1.2.5
pip install ruamel-yaml
pip install markupsafe==2.0.1
pip install pandas_profiling==3.2.0
```
or
```bash
pip install -r requirements.txt
```

# Usage
`python make_profile.py --file mycsv.csv --html`
* file extension supported
  * **csv**
  * **xlsx**
* save type
  * **html**(option: `--html`)
  * **json**(option: `--json`)
  
# Thanks to...
1. Pandas-Profiling official Repository : https://github.com/ydataai/pandas-profiling
2. How-to-change Font? : https://www.youtube.com/watch?v=BhZvZpNF9jU

-----

# 한글 패치 방법

1. 언어를 담당하는 `site-packages/pandas_profiling/visualisation/context.py` 의 함수가 길지 않음.
2. 그러므로, 해당 함수를 string으로 긁어와서, 필요한 부분만 내가 바꾼 뒤에 파일을 바꿔치기 하는 형식으로 한글패치를 진행함.
3. prototype 코드
```python
NEW_FUNCTION_STRING = \
"""
import contextlib
import warnings
from typing import Any

import matplotlib
import matplotlib.cbook
import seaborn as sns
from pandas.plotting import (
    deregister_matplotlib_converters,
    register_matplotlib_converters,
)


@contextlib.contextmanager
def manage_matplotlib_context() -> Any:
    originalRcParams = matplotlib.rcParams.copy()

    # Credits for this style go to the ggplot and seaborn packages.
    #   We copied the style file to remove dependencies on the Seaborn package.
    #   Check it out, it's an awesome library for plotting
    customRcParams = {
        "patch.facecolor": "#348ABD",  # blue
        "patch.antialiased": True,
        "font.size": 10.0,
        "figure.edgecolor": "0.50",
        # Seaborn common parameters
        "figure.facecolor": "white",
        "text.color": ".15",
        "axes.labelcolor": ".15",
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": ".15",
        "ytick.color": ".15",
        "axes.axisbelow": True,
        "image.cmap": "Greys",
        # "font.family": ["sans-serif"],
        # "font.sans-serif": [
        #     "Arial",
        #     "Liberation Sans",
        #     "Bitstream Vera Sans",
        #     "sans-serif",
        # ],
        "grid.linestyle": "-",
        "lines.solid_capstyle": "round",
        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        "axes.grid": True,
        "axes.facecolor": "#EAEAF2",
        "axes.edgecolor": "white",
        "axes.linewidth": 0,
        "grid.color": "white",
        # Seaborn notebook context
        "figure.figsize": [8.0, 5.5],
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.linewidth": 1,
        "lines.linewidth": 1.75,
        "patch.linewidth": 0.3,
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        "font.family": ["NanumGothic"],
        "font.sans-serif": ["NanumGothic"]
    }

    try:
        register_matplotlib_converters()
        matplotlib.rcParams.update(customRcParams)
        # sns.set_style(style="white")
        yield
    finally:
        deregister_matplotlib_converters()  # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
            matplotlib.rcParams.update(originalRcParams)  # revert to original rcParams
"""

import pandas as pd
import warnings
import os


ret = os.popen("pip show pandas_profiling").read()
ret = ret.replace('\n', ' ').split(' ')
index = ret.index("Location:") + 1
package_path = ret[index]
context_script_path = os.path.join(package_path, "pandas_profiling", "visualisation", "context.py")

if not os.path.isfile(os.path.abspath(context_script_path)):
    print(f"Please Check context.py file! : {os.path.abspath(context_script_path)}")
    exit()

print("\n - Target context.py path :", context_script_path)

default_function = ''
need_update = False

with open(context_script_path, 'r') as context_script:
    default_function = context_script.read()

    if NEW_FUNCTION_STRING == default_function:
        print(" - Don't have to update context.py file!")
    else:
        print(" - !!! You should have to update context.py file !!!")
        need_update = True

if need_update:
    with open(context_script_path, 'w') as context_script:
        print(f"\n Write new function ............ \n\n'''{NEW_FUNCTION_STRING}'''\n\n")
        print(f"\n\n [NEW_FUNCTION_STRING] will be inserted here -> {os.path.abspath(context_script_path)}")
        context_script.write(NEW_FUNCTION_STRING)
        print(" Success.")

import pandas_profiling
from pandas_profiling import ProfileReport

print(f"\n\n - import pandas\n - [Pandas] Package Version : {pd.__version__}")
print(f"\n - import pandas_profiling\n - [Pandas Profiling] Package Version : {pandas_profiling.__version__}\n")

warnings.filterwarnings("ignore")

print("\n============ read csv/excel data using pandas package + DESCRIBE ============ ")
# data = pd.read_csv("BostonHousing_noNaN_forRegressor.csv")
data = pd.read_csv("bostonHousing_hangul.csv")
print(data.describe())

profile = ProfileReport(data, title="Dataset Profiling Report", explorative=True)

print("\n\n============ Save profiling report to html file ============ ")
pwd = os.getcwd()
filename = os.path.join(pwd, "report.html")
profile.to_file(filename)

html_obj = profile.to_html()
if html_obj is not None:
    print(f"\n\n - Saving [report.html] is Successful ! : {os.path.abspath(filename)}\n\n")
```
4. NEW_FUNCTION_STRING을 context.py에 붙여넣기 하는걸로.
5. 조건:
> 1. pandas_profiling 패키지는 **3.2.0** 만 가능함. (이후 버전 업데이트 시에, 경로나 함수명 등등이 변경될 수 있음.)
> 2. pandas 패키지는 **1.2.5** 쓰는걸로.
> 3. `apt install fonts-nanum*` 커맨드로 나눔 폰트를 설치해야 함.
> 4. (재언급) **markupsafe** 패키지는 **2.0.1** 만 가능. (이 외의 버전 설치 시 오류 발생, `pip install markupsafe==2.0.1`)
> 5. (재언급) **ruamel-yaml** 패키지 설치해야 함 : `pip install ruamel-yaml`
6. 실행 결과 - **한글 패치가 필요한 경우**
```plain
(neural) gpuadmin@gpusystem:~/dc/neural-framework/dc$ python pandas_profiling_test.py 

 - Target context.py path : /home/gpuadmin/.conda/envs/neural/lib/python3.8/site-packages/pandas_profiling/visualisation/context.py
 - !!! You should have to update context.py file !!!

 Write new function ............ 

'''
import contextlib
import warnings
from typing import Any

import matplotlib
import matplotlib.cbook
import seaborn as sns
from pandas.plotting import (
    deregister_matplotlib_converters,
    register_matplotlib_converters,
)


@contextlib.contextmanager
def manage_matplotlib_context() -> Any:
    originalRcParams = matplotlib.rcParams.copy()

    # Credits for this style go to the ggplot and seaborn packages.
    #   We copied the style file to remove dependencies on the Seaborn package.
    #   Check it out, it's an awesome library for plotting
    customRcParams = {
        "patch.facecolor": "#348ABD",  # blue
        "patch.antialiased": True,
        "font.size": 10.0,
        "figure.edgecolor": "0.50",
        # Seaborn common parameters
        "figure.facecolor": "white",
        "text.color": ".15",
        "axes.labelcolor": ".15",
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": ".15",
        "ytick.color": ".15",
        "axes.axisbelow": True,
        "image.cmap": "Greys",
        # "font.family": ["sans-serif"],
        # "font.sans-serif": [
        #     "Arial",
        #     "Liberation Sans",
        #     "Bitstream Vera Sans",
        #     "sans-serif",
        # ],
        "grid.linestyle": "-",
        "lines.solid_capstyle": "round",
        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        "axes.grid": True,
        "axes.facecolor": "#EAEAF2",
        "axes.edgecolor": "white",
        "axes.linewidth": 0,
        "grid.color": "white",
        # Seaborn notebook context
        "figure.figsize": [8.0, 5.5],
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.linewidth": 1,
        "lines.linewidth": 1.75,
        "patch.linewidth": 0.3,
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        "font.family": ["NanumGothic"],
        "font.sans-serif": ["NanumGothic"]
    }

    try:
        register_matplotlib_converters()
        matplotlib.rcParams.update(customRcParams)
        # sns.set_style(style="white")
        yield
    finally:
        deregister_matplotlib_converters()  # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
            matplotlib.rcParams.update(originalRcParams)  # revert to original rcParams
'''




 Insert here -> /home/gpuadmin/.conda/envs/neural/lib/python3.8/site-packages/pandas_profiling/visualisation/context.py
 Success.


 - import pandas
 - [Pandas] Package Version : 1.2.5

 - import pandas_profiling
 - [Pandas Profiling] Package Version : 3.2.0


============ read csv/excel data using pandas package + DESCRIBE ============ 
              범죄율      주거토지비율      상업토지비율       찰스강인근       일산화질소        방_개수     오래된주택비율      직업센터거리     고속도로접근성        재산세율      학생교사비율           B      하위계층비율        주택가격      주택가격등급
count  486.000000  486.000000  486.000000  486.000000  506.000000  506.000000  486.000000  506.000000  506.000000  506.000000  506.000000  506.000000  486.000000  506.000000  506.000000
mean     3.611874   11.211934   11.083992    0.069959    0.554695    6.284634   68.518519    3.795043    9.549407  408.237154   18.455534  356.674032   12.715432   22.532806    0.974308
std      8.720192   23.388876    6.835896    0.255340    0.115878    0.702617   27.999513    2.105710    8.707259  168.537116    2.164946   91.294864    7.155871    9.197104    0.598126
min      0.006320    0.000000    0.460000    0.000000    0.385000    3.561000    2.900000    1.129600    1.000000  187.000000   12.600000    0.320000    1.730000    5.000000    0.000000
25%      0.081900    0.000000    5.190000    0.000000    0.449000    5.885500   45.175000    2.100175    4.000000  279.000000   17.400000  375.377500    7.125000   17.025000    1.000000
50%      0.253715    0.000000    9.690000    0.000000    0.538000    6.208500   76.800000    3.207450    5.000000  330.000000   19.050000  391.440000   11.430000   21.200000    1.000000
75%      3.560263   12.500000   18.100000    0.000000    0.624000    6.623500   93.975000    5.188425   24.000000  666.000000   20.200000  396.225000   16.955000   25.000000    1.000000
max     88.976200  100.000000   27.740000    1.000000    0.871000    8.780000  100.000000   12.126500   24.000000  711.000000   22.000000  396.900000   37.970000   50.000000    2.000000


============ Save profiling report to html file ============ 
Summarize dataset: 100%|██████████████████████████████| 199/199 [00:20<00:00,  9.48it/s, Completed]
Generate report structure: 100%|██████████████████████████████| 1/1 [00:04<00:00,  4.42s/it]
Render HTML: 100%|██████████████████████████████| 1/1 [00:05<00:00,  5.60s/it]
Export report to file: 100%|██████████████████████████████| 1/1 [00:00<00:00, 27.35it/s]


 - Saving [report.html] is Successful ! : /home/gpuadmin/dc/neural-framework/dc/report.html

```
7. 실행 결과 - **한글 패치가 필요없는 경우**
```plain
(neural) gpuadmin@gpusystem:~/dc/neural-framework/dc$ python pandas_profiling_test.py 

 - Target context.py path : /home/gpuadmin/.conda/envs/neural/lib/python3.8/site-packages/pandas_profiling/visualisation/context.py
 - Don't have to update context.py file!


 - import pandas
 - [Pandas] Package Version : 1.2.5

 - import pandas_profiling
 - [Pandas Profiling] Package Version : 3.2.0


============ read csv/excel data using pandas package + DESCRIBE ============ 
              범죄율      주거토지비율      상업토지비율       찰스강인근       일산화질소        방_개수     오래된주택비율      직업센터거리     고속도로접근성        재산세율      학생교사비율           B      하위계층비율        주택가격      주택가격등급
count  486.000000  486.000000  486.000000  486.000000  506.000000  506.000000  486.000000  506.000000  506.000000  506.000000  506.000000  506.000000  486.000000  506.000000  506.000000
mean     3.611874   11.211934   11.083992    0.069959    0.554695    6.284634   68.518519    3.795043    9.549407  408.237154   18.455534  356.674032   12.715432   22.532806    0.974308
std      8.720192   23.388876    6.835896    0.255340    0.115878    0.702617   27.999513    2.105710    8.707259  168.537116    2.164946   91.294864    7.155871    9.197104    0.598126
min      0.006320    0.000000    0.460000    0.000000    0.385000    3.561000    2.900000    1.129600    1.000000  187.000000   12.600000    0.320000    1.730000    5.000000    0.000000
25%      0.081900    0.000000    5.190000    0.000000    0.449000    5.885500   45.175000    2.100175    4.000000  279.000000   17.400000  375.377500    7.125000   17.025000    1.000000
50%      0.253715    0.000000    9.690000    0.000000    0.538000    6.208500   76.800000    3.207450    5.000000  330.000000   19.050000  391.440000   11.430000   21.200000    1.000000
75%      3.560263   12.500000   18.100000    0.000000    0.624000    6.623500   93.975000    5.188425   24.000000  666.000000   20.200000  396.225000   16.955000   25.000000    1.000000
max     88.976200  100.000000   27.740000    1.000000    0.871000    8.780000  100.000000   12.126500   24.000000  711.000000   22.000000  396.900000   37.970000   50.000000    2.000000


============ Save profiling report to html file ============ 
Summarize dataset: 100%|██████████████████████████████| 199/199 [00:20<00:00,  9.76it/s, Completed]
Generate report structure: 100%|██████████████████████████████| 1/1 [00:04<00:00,  4.27s/it]
Render HTML: 100%|██████████████████████████████| 1/1 [00:05<00:00,  5.39s/it]
Export report to file: 100%|██████████████████████████████| 1/1 [00:00<00:00, 32.39it/s]


 - Saving [report.html] is Successful ! : /home/gpuadmin/dc/neural-framework/dc/report.html


```

8. 결과 이미지 - **한글 X**
<img width="1227" alt="image" src="https://user-images.githubusercontent.com/41134624/177969269-5a03d147-f26b-4bd7-8f10-fea33581f074.png">
<img width="1210" alt="image" src="https://user-images.githubusercontent.com/41134624/177974299-f6ec70f3-3f6c-45bb-8ff7-dfd95543d476.png">

9. 결과 이미지 - **한글 O**
<img width="1216" alt="image" src="https://user-images.githubusercontent.com/41134624/177969750-ec94355a-10c6-4095-b2f9-395f952eee6b.png">
<img width="1204" alt="image" src="https://user-images.githubusercontent.com/41134624/177970270-390fa56b-8946-4c8a-9d8d-d2e8ac4425fb.png">

