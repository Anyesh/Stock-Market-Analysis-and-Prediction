import pandas as pd
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

plt.style.use('ggplot')
def plot(name, *, cols=[], plot_kind=None, start_date=None, end_date=None):
    """ Plots selected financial data of selected company which ranges over specified
    date range[start_date:end_date]. The plot is as specified by the plot_kind parameter.
    :param
          name: company's ticker
          cols: list of columns specifying data fields to plot.
          kind: type of plot. One of 'line', 'box', 'hexbin','scatter_matrix'.
          start_date: The data is indexed by the Date column. starting date specifies
                      the first date index row to be plotted.
          end_date: end_date specifies the last date index row to be plotted.
    """
    header = ['Date','Total Transactions','Traded Shares','TotalTraded Amount',
              'Maximum Price','Minimum Price','Closing Price']

    plottypes = ['line', 'box', 'hexbin','scatter_matrix']

    if cols is None or not cols:
        cols = header[1:]
    if plot_kind is None:
        plot_kind = 'line'

    if not set(cols) <= set(header):
        raise ValueError('{} is not a valid column list in the data present.'.format(cols))

    if not plot_kind in plottypes:
        raise ValueError('{} is not a valid plot type. Please enter one of these {}.'.format(plot_kind, plottypes))

    filename = name
    try:
        data = pd.read_csv(filename,index_col=0, parse_dates=True)
    except(FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return None

    if plot_kind == 'scatter_matrix':
        scatter_matrix(data.ix[:,cols][start_date:end_date], alpha=0.2, diagonal='kde')
    elif plot_kind == 'hexbin':
        if len(cols) < 2:
            print('invalid no of columns for a hexbin plot. Two data columns are required.')
            return None
        data.ix[:,cols][start_date:end_date].plot(kind=plot_kind, x=cols[0], y=cols[1], gridsize=25)
    else:
         data.ix[:,cols][start_date:end_date].plot(kind=plot_kind,subplots=True,
                             title='{} Plot of {}.'.format(plot_kind.title(),name))
    plt.show()

def comparision_plot(name,*, cols=None, plot_kind=None, start_date=None, end_date=None):
    """ Plots selected financial data of selected companies which ranges over specified
    date range[start_date:end_date]. The plot is as specified by the plot_kind parameter.
    :param
          name: list of companies ticker.
          cols: list of columns specifying data fields to plot.
          kind: type of plot. One of 'line', 'box'.
          start_date: The data is indexed by the Date column. starting date specifies
                      the first date index row to be plotted.
          end_date: end_date specifies the last date index row to be plotted.
    """
    header = ['Date','Total Transactions','Traded Shares','TotalTraded Amount',
              'Maximum Price','Minimum Price','Closing Price']

    plottypes = ['line', 'box']

    if cols is None or not cols:
        cols = header[1:]
    if plot_kind is None:
        plot_kind = 'line'

    if not set(cols) <= set(header):
        raise ValueError('{} is not a valid column list in the data present.'.format(cols))
    if not plot_kind in plottypes:
        raise ValueError('{} is not a valid plot type. Please enter one of these {}.'.format(plot_kind, plottypes))

    filenames = name
    try:
        data = pd.concat([pd.read_csv(company, index_col=0, parse_dates=True) for company in filenames], axis=1, keys=name)
    except(FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return None

    ax = data.ix[:, data.columns.get_level_values(1).isin(set(cols))][start_date:end_date].plot()
    ax.set_title('{} Plot of {} of {}.'.format(plot_kind.title(),','.join(cols), ','.join([s.strip('.csv') for s in name])))
    plt.legend(title='Companies', fancybox=True, shadow=True, loc='best')
    plt.show()
