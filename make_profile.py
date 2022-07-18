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
        "font.sans-serif": ["NanumGothic"],
        "axes.unicode_minus": False
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


if __name__ == "__main__":
    import pandas as pd
    import warnings
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Pandas Profiling - Making Korean profile')

    parser.add_argument("--file", type=str, help='Input dataset(csv, xlsx)')

    parser.add_argument("--html", action='store_true', help='returned html file')
    parser.add_argument("--json", action='store_true', help='returned json file')
#    parser.add_argument("--iframe", action='store_true', help='returned iframe file')

    args = parser.parse_args()

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
    data = None

    if args.file.endswith("csv"):
        print("Dataset extention : [csv]\n")
        data = pd.read_csv(args.file)
    elif args.file.endswith("xlsx"):
        print("Dataset extention : [xlsx]\n")
        data = pd.read_excel(args.file, engine="openpyxl")
    else:
        raise NotImplementedError

    print(data.describe())

    profile = ProfileReport(data, title="Dataset Profiling Report", explorative=True)

    pwd = os.getcwd()
    if args.html:
        print("\n\n============ Save profiling report to html file ============ ")
        filename = os.path.join(pwd, "report.html")
        profile.to_file(filename)

        html_obj = profile.to_html()
        if html_obj is not None:
            print(f"\n\n - Saving [report.html] is Successful ! : {os.path.abspath(filename)}\n\n")
    elif args.json:
        import json

        filename = os.path.join(pwd, "report.json")
        json_data = profile.to_json()

        with open(filename, "w") as f:
            json.dump(json_data, f)

#    elif args.iframe:
#        iframe = profile.to_notebook_iframe()
#        print(iframe)

    else:
        raise NotImplementedError
