
# What is `xarray`?

From [xarray.pydata.org](http://xarray.pydata.org/):

![xarray](http://xarray.pydata.org/en/stable/_images/dataset-diagram-logo.png)

N-D labeled arrays and datasets in Python
=========================================

**xarray** (formerly **xray**) is an open source project and Python package
that aims to bring the labeled data power of `pandas` to the physical sciences,
by providing N-dimensional variants of the core pandas data structures.

Our goal is to provide a pandas-like and pandas-compatible toolkit for
analytics on multi-dimensional arrays, rather than the tabular data for which
pandas excels. Our approach adopts the `Common Data Model` for self-
describing scientific data in widespread use in the Earth sciences:
``xarray.Dataset`` is an in-memory representation of a netCDF file.

# Why is `xarray` cool?

- `pandas`, but for multiple dimensions!
    - Formerly `pd.Panel`, `pd.Panel4D`, etc
- Automatic broadcasting and alignment
- Simple vectorization
    - Takes advantage of balanced data
- Built-in support for `dask`, `netCDF`, etc

# How do I use `xarray`?

## Installation
1. Creating a new `conda env`
```
source /ihme/code/central_comp/miniconda/bin/activate gbd_env
conda create --name xarray-demo --clone gbd_env
source activate xarray-demo
```
2. Installing `xarray`
```
conda install xarray
```
3. Optional add-ons
```
conda install dask
conda install netcdf4
```


# Who should use `xarray`, and when?

`xarray` excels when:
- You've got lots of dimensions
- ...which are balanced
- You need to do lots of combining of data
- You're slicing across different dimensions

`xarray` is not the answer to your problems if:
- Your data is not balanced
    - E.g. raw data, where you have different numbers of data points for different demographic combos
- You need to use things which expect `pandas`, like `statsmodels`
    - _However_, there's always `xr.Dataset.to_pandas()`!

# Where can I learn more about `xarray`?

The [`xarray` documentation](http://xarray.pydata.org/en/stable/index.html) is really great!

# Notes

__Author__: Kyle Foreman (kfor@uw.edu)

__Originally presented:__ 13 October 2017

