import numpy as np

''' functions for pre-processing digital signals '''

def clip_signal_start(signal, index):
    return signal[index:]


def clip_signal_both_ends(signal, clip_pcnt=0.05):
    clip_length = int(len(signal)*clip_pcnt)
    return signal[clip_length: -1*clip_length]


def cutoff_threshold_from_signal_max(signal, n_bins=10, cutoff_pcnt=0.33):
    ''' defines a cutoff amplitude for a signal based on the percent of the
        average max value within n number of bins '''
    n = len(signal)
    bins = [int(x) for x in np.linspace(1,n,n_bins+1)]
    bin_maxs = []
    for i in range(1,n_bins+1):
        xx = signal[bins[i-1]:bins[i]]
        bin_maxs.append(np.max(xx))

    mean_binmax = np.mean(bin_maxs)
    return mean_binmax * cutoff_pcnt


def clip_signal_start_by_threshold(signal, threshold):
    ''' clips the start of a signal:
        removes all values until threshold is reached, starting at first value '''
    i = np.argmax(signal > threshold)
    return signal[i:]


def clip_signal_end_by_threshold(signal, threshold):
    ''' clips the start of a signal:
        removes all values until threshold is reached, starting at first value '''
    arr_flip = np.fliplr([signal])[0]
    i = np.argmax(arr_flip > threshold)
    return signal[:-i]
