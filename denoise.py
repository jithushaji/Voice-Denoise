import warnings
import os

import soundfile as sf
from tensorflow.keras.models import model_from_json
from utils import scaled_in, inv_scaled_ou
from utils import audio_files_to_numpy, numpy_audio_to_matrix_spectrogram, matrix_spectrogram_to_numpy_audio
import argparse
warnings.filterwarnings('ignore')

def noise():
    
    if os.path.exists('predictions')==False:
        os.mkdir('predictions')
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_dir_prediction', default='sound/', type=str)
    parser.add_argument('--dir_save_prediction', default='predictions/', type=str)
    parser.add_argument('--audio_input_prediction', default=['noise2.wav'], type=list)
    parser.add_argument('--audio_output_prediction', default='denoise.wav', type=str)
    parser.add_argument('--sample_rate', default=8000, type=int)
    parser.add_argument('--min_duration', default=1.0, type=float)
    parser.add_argument('--frame_length', default=8064, type=int)
    parser.add_argument('--hop_length_frame', default=8064, type=int)
    parser.add_argument('--hop_length_frame_noise', default=5000, type=int)
    parser.add_argument('--n_fft', default=255, type=int)
    parser.add_argument('--hop_length_fft', default=63, type=int)
    args = vars(parser.parse_args())



    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights('model.h5')
    print("Loaded model from disk")

    dir_list = os.listdir(args['audio_dir_prediction'])
     

    for noise in dir_list:
    # prints all files
        print(noise)
        voice =noise.split(" ") 
        print(voice)
        # Extracting noise and voice from folder and convert to numpy
        audio = audio_files_to_numpy(args['audio_dir_prediction'], voice, args['sample_rate'],
                                     args['frame_length'], args['hop_length_frame'], args['min_duration'])

        #Dimensions of squared spectrogram
        dim_square_spec = int(args['n_fft'] / 2) + 1
        print(dim_square_spec)

        # Create Amplitude and phase of the sounds
        m_amp_db_audio,  m_pha_audio = numpy_audio_to_matrix_spectrogram(
            audio, dim_square_spec, args['n_fft'], args['hop_length_fft'])

        #global scaling to have distribution -1/1
        X_in = scaled_in(m_amp_db_audio)
        #Reshape for prediction
        X_in = X_in.reshape(X_in.shape[0],X_in.shape[1],X_in.shape[2],1)
        #Prediction using loaded network
        X_pred = loaded_model.predict(X_in)
        #Rescale back the noise model
        inv_sca_X_pred = inv_scaled_ou(X_pred)
        #Remove noise model from noisy speech
        X_denoise = m_amp_db_audio - inv_sca_X_pred[:,:,:,0]
        #Reconstruct audio from denoised spectrogram and phase
        print(X_denoise.shape)
        print(m_pha_audio.shape)
        audio_denoise_recons = matrix_spectrogram_to_numpy_audio(X_denoise, m_pha_audio, args['frame_length'], args['hop_length_fft'])
        #Number of frames
        nb_samples = audio_denoise_recons.shape[0]
        #Save all frames in one file
        denoise_long = audio_denoise_recons.reshape(1, nb_samples * (args['frame_length']))*10
        sf.write(args['dir_save_prediction'] + noise, denoise_long[0, :], args['sample_rate'])


#noise()

