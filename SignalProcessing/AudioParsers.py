import numpy as np
from scipy.signal import butter, lfilter, freqz, argrelextrema
import pdb

class LowpassFilterAudioParser(object):
    ''' finds indices of peaks in an audio file after applying lowpass filter
        includes functionality for removing double peaks that are close together'''

    def __init__(self, cutoff, fs, order, absval=True):
        self.cutoff = cutoff # high frequency cutoff
        self.fs = fs # sample frequency of signal
        self.order = order # order of butterworth filter
        self.absval = absval # if True, run filter on abs(signal)

    def butter_lowpass_params(self):
        ''' get b, a params for digital butter filter'''
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, b, a):
        y = lfilter(b, a, self.signal)
        return y

    def filter(self, signal):
        self.signal = signal
        b, a = self.butter_lowpass_params()
        if self.absval:
            self.signal = np.abs(self.signal)
        self.y = self.butter_lowpass_filter(b, a)
        return self.y

    def find_peaks(self):
        self.extrema_idx = argrelextrema(self.y, np.greater, order=2)[0]
        return self.extrema_idx

    def remove_double_peaks(self, thresh=0.33):
        self.find_peaks()
        deltas = np.diff(self.extrema_idx)
        dblpeak = deltas < np.mean(deltas)*thresh # boolean array
        # test if any double peaks
        if np.sum(dblpeak) == 0:
            return self.extrema_idx
        else:
            i_dbl = np.where(dblpeak)[0][0] + 1 # index of dblpeak , +1 b/c of diff fn
            self.extrema_idx = np.delete(self.extrema_idx, i_dbl)
            return self.extrema_idx

    def remove_peaks_below_threshold(self, thresh=3000):
        ''' remove peaks below an amplitude threshold '''
        extrema = self.y[self.extrema_idx]
        keep_if_true = extrema >= thresh
        ii = self.extrema_idx[keep_if_true]
        return ii


class IterativeThresholdAudioParser(object):
    def __init__(self, window, peak_scale_factor, trough_scale_factor):
        self.window = window
        self.peakscale = peak_scale_factor
        self.troughscale = trough_scale_factor

    def scale_by_min_max(self):
        max = np.max(self.signal)
        min = np.min(self.signal)
        meanmax = np.mean([max, np.abs(min)])
        self.t_peak = meanmax * self.peakscale
        self.t_trough = meanmax * self.troughscale

    def find_trough_index_max_n(self, xx):
        for i in range(len(xx)):
            max_n = np.max(xx[i: i + self.window])
            min_n = np.min(xx[i: i + self.window])
            #pdb.set_trace()
            if max_n < self.t_trough and min_n > self.t_trough * -1:
                return i
                break

    def find_peaks_troughs(self):
        idxs = []
        dd = self.signal.copy()
        count = 0
        i = 0
        while count <= len(self.signal):
            # break search if no more peaks above p_threshold
            if np.sum(dd > self.t_peak) == 0:
                break
            else:
                # find next peak
                peak = np.argmax(dd > self.t_peak)
                idxs.append(peak)
                dd = dd[peak:]
                count += peak
                i += 1

            # break search if no more troughs below t_threshold
            if np.sum(np.abs(dd) < self.t_trough) == 0:
                trough = 0
            else:
                # find next trough
                trough = self.find_trough_index_max_n(dd)
            idxs.append(trough)
            dd = dd[trough:]
                #pdb.set_trace()
            count += trough
            i += 1

        return idxs


    def fit(self, signal):
        self.signal = signal
        self.scale_by_min_max()
        idxs = self.find_peaks_troughs()
        # cumsum indices and parse peaks vs troughs
        idxs = np.cumsum(idxs)
        return idxs
