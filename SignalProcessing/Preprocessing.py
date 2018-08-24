import numpy as np
import wave

''' functions for pre-processing audio signals '''

def convert_audio_file(audio_dir, file_in, file_out):
    ''' uses ffmpeg (brew install ffmpeg) to convert between audio formats
    file_in:        e.g. 'file1.m4a'
    file_out:       e.g. 'file1.wav'  '''
    from subprocess import call
    call (['ffmpeg', '-i', audio_dir + file_in, audio_dir + file_out])
    

def read_wavfile(filename):
    with wave.open( filename, 'r') as wavfile:
        #Extract Raw Audio from Wav File
        data = wavfile.readframes(-1)
        data = np.frombuffer(data, 'Int16')
        framerate = wavfile.getframerate()
    return data, framerate


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
