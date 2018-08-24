import numpy as np

def convert_audio_file(audio_dir, file_in, file_out):
    ''' uses ffmpeg (brew install ffmpeg) to convert between audio formats
    file_in:        e.g. 'file1.m4a'
    file_out:       e.g. 'file1.wav'  '''
    from subprocess import call
    call (['ffmpeg', '-i', audio_dir + file_in, audio_dir + file_out])


def read_wavfile(filename):
    import wave
    with wave.open( filename, 'r') as wavfile:
        #Extract Raw Audio from Wav File
        data = wavfile.readframes(-1)
        data = np.frombuffer(data, 'Int16')
        framerate = wavfile.getframerate()
    return data, framerate
