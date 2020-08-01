'''This script demonstrates how to build a variational autoencoder with Keras.
 #Reference
 - Auto-Encoding Variational Bayes
   https://arxiv.org/abs/1312.6114
'''
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from keras.layers import Input, Dense, Lambda
from keras.models import Model
from keras import backend as K
from keras import metrics
from keras.models import load_model
from keras import objectives
from keras.datasets import mnist
from keras.utils.generic_utils import get_custom_objects
from Hcluster import hcluster
import pickle
import readcsv

def normalize(vec):
    minimum = 100
    maximum = -100
    for item in vec:
        if item < minimum:
            minimum = item
        if item > maximum:
            maximum = item
    for i in range(len(vec)):
        vec[i] = 0.01+0.99*(vec[i]-minimum)/(maximum-minimum)
    return  


with open("realVec.txt", 'rb') as savefile:    
    realVec = pickle.load(savefile)
with open("virVec.txt", 'rb') as savefile:    
    virVec = pickle.load(savefile)
with open("vectorslice.pickle", 'rb') as savefile:    
    symVec = pickle.load(savefile)


inputVec = []
for i in range(len(realVec)):
    inputVec.append([])
    normalize(realVec[i])
    normalize(virVec[i])
    normalize(symVec[i])
    for item in realVec[i]:
        inputVec[i].append(item)
    for item in virVec[i]:
        if item > - 0.1 and item < 1.5:
            inputVec[i].append(item)
        else:
            inputVec[i].append(0.01)
    for item in symVec[i]:
        inputVec[i].append(item)
# inputVec is the combination of three kinds of information
inputVec = np.array(inputVec)

print(inputVec[130])
print(realVec[130])
print(virVec[130])
print(symVec[130])


# VAE parameters
batch_size = 32
original_dim = len(inputVec[0])
latent_dim = 20
intermediate_dim = 80
epochs = 100
epsilon_std = 1.0

print(original_dim)

def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(K.shape(z_mean)[0], 20), mean=0.,
                              stddev=1.0)
    return z_mean + K.exp(z_log_var / 2) * epsilon

x = Input(shape=(original_dim,))
h = Dense(intermediate_dim, activation='relu',name="midh")(x)
z_mean = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)


# note that "output_shape" isn't necessary with the TensorFlow backend
#z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])
z = Lambda(sampling)([z_mean, z_log_var])

# we instantiate these layers separately so as to reuse them later
decoder_h = Dense(intermediate_dim, activation='relu')
decoder_mean = Dense(original_dim, activation='sigmoid')
h_decoded = decoder_h(z)
x_decoded_mean = decoder_mean(h_decoded)

# instantiate VAE model
vae = Model(x, x_decoded_mean)

# Compute VAE loss
def vae_loss(x, x_decoded_mean):
    xent_loss = original_dim * objectives.binary_crossentropy(x, x_decoded_mean)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    return xent_loss + kl_loss


vae.compile(optimizer='rmsprop',loss = vae_loss)
vae.summary()


# train the VAE
vae.fit(inputVec,inputVec,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size)

# build a model to project inputs on the latent space
encoder = Model(x, z_mean)



# result 
inputVec_encoded = encoder.predict(inputVec, batch_size=batch_size)
encoder.save_weights("encoderModel.h5",overwrite=True)

print (inputVec_encoded[130])
#（num,url,title,content ---> vector）
vectordatabase = readcsv.make_original_dataset()
database=['dsjwz.csv','gkw.csv','jqzx.csv','ktx.csv','mm.csv','xkd.csv','xsx.csv']
seq = 0
for entry in database:
    for i in range(len(vectordatabase[entry])):
        vectordatabase[entry][i][3] =  inputVec_encoded[seq]
        seq+=1
with open("vectordatabase.txt", 'wb') as savefile:    
    pickle.dump(vectordatabase,savefile)





