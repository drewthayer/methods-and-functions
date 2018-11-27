import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def time_series_plot(series, lags, figsize=(8, 6), style='bmh'):
    ''' plots time series, autocorrelation, and partial autocorrelation

    requires imports:
        from statsmodels.graphics.tsaplots import plot_acf, plot_pacf '''
    with plt.style.context(style):
        layout = (3,1)
        ts_ax = plt.subplot2grid(layout, (0,0))
        acf_ax = plt.subplot2grid(layout, (1,0))
        pacf_ax = plt.subplot2grid(layout, (2,0))

        ts_ax.plot(data)
        ts_ax.set_title('Time Series')
        plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5)
        plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5)

        plt.tight_layout()
        plt.show()
    return


def decomposition_plot(data, result):
    ''' data        timeseries
        result      statsmodels seasonal_decompose result object '''
    fig, ax = plt.subplots(4,1)
    ax[0].plot(data, '-k', label='observed')
    ax[0].set_ylabel('observed')
    ax[0].get_xaxis().set_ticklabels([])
    ax[1].plot(result.trend, '-b', label='trend')
    ax[1].set_ylabel('trend')
    ax[1].get_xaxis().set_ticklabels([])
    ax[2].plot(result.seasonal, '-g', label='seasonal')
    ax[2].set_ylabel('seasonal')
    ax[2].get_xaxis().set_ticklabels([])
    ax[3].plot(result.resid, '-k', label='residual')
    ax[3].set_ylabel('residual')
    plt.suptitle('time series decomposition')
    plt.subplots_adjust(top=0.9)
    plt.show()
    

def decompose_and_plot(data):
    ''' data        timeseries '''
    from statsmodels.tsa.seasonal import seasonal_decompose
    result = seasonal_decompose(data, model='additive', freq=15) # An object with seasonal, trend, and resid attributes

    decomposition_plot(data, result)

    return result
