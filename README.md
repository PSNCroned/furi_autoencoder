# Autoencoder for changepoint detection

Software for training a deep learning autoencoder on multi-channel time series data and then applying the model on both pre-recorded and live data

## Extracting data

Before a new model can be trained, the dataset being used for training and testing must be extracted and parsed to a csv file. 

To extract the data as is with no cycling of the channels, modify the pathname in *extract_channels.py* and then run

    python extract_channels.py
    
If cycling of the channels is desired and it has not already been done in the original dataset, modify *extract_channels_cycle.py* with the desired pathname and method of cycling, and then run

    python extract_channels_cycle.py
    
    
## Training a model

The default network structure is 4 encoding layers at 80%, 60%, 40%, and 20% of the input layer size, and then four decoding layers increasing in the reverse order. By default, the network uses half of the extracted data for training and the other half for testing. To train the extracted data on this network, run 

    python autoencoder.py [num_epochs]

To continue training a previously trained model (stored at *models/encoder.h5* and *models/decoder.h5*) run

    python autoencoder.py load [num_epochs]
    
## Plotting the results

The data used for testing the model as well as the outputs of the encoder and decoder are stored in */results*. To view these plotted along with the changepoints, run

    python plot_channels.py [total_channels] original [num_data points]
    
To view a comparison between the original and decoded data, run

    python plot_channels.py [total_channels] original decoded [num_data_points] [channel_num]
    
Ground truth change points can be set in *plot_channels.py* by adding them to the *gTruths* array.


## Live EMG analysis

Ensure that node.js is installed and Myo Connect is running, and then run

    node index.js

from within the */live_myo_data* directory. Then run

    python live.py
    
from the root directory to see live analysis of the Myo emg data that uses the encoder.h5 model stored in */models*.
