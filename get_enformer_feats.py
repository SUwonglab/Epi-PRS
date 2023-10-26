import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import os, sys
from pyfasta import Fasta
import math
import h5py


enformer_model = hub.load("https://tfhub.dev/deepmind/enformer/1").model
SEQ_LENGTH = 393216
interval = 896*128

chr_id = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
parent = sys.argv[4]
fasta_path = sys.argv[5]
save_path =sys.argv[6]

#one-hot coding
def seq_to_mat(seq):
    d = {'a':0, 'A':0, 'c':1, 'C':1, 'g':2, 'G':2, 't':3, 'T':3, 'N':4, 'n':4}
    mat = np.zeros((5,len(seq)))
    for i in range(len(seq)):
        mat[d[seq[i]],i] = 1
    mat = mat[:4,:]
    return mat

def main():
    chr_id, start, end 
    center = (start+end) // 2
    nb_regions = math.ceil((end-start-interval)/(2*interval))
    genome = Fasta(fasta_path)
    enformer_feats = []
    for coor in range(center-interval*nb_regions, center+interval*(nb_regions+1),interval):
        seq = genome['chr%s_%s'%(chr_id,parent)][(coor-SEQ_LENGTH//2):(coor+SEQ_LENGTH//2)]
        onehot_mat = seq_to_mat(seq).T
        onehot_mat = np.expand_dims(onehot_mat,0)
        enformer_feats.append(enformer_model.predict_on_batch(onehot_mat)['human'])
    enformer_feats = np.squeeze(np.stack(enformer_feats))
    enformer_feats = enformer_feats.astype(np.float16)
    print(each, enformer_feats.shape)
    f_out = h5py.File(save_file,'w')
    _, nb_bins, _ = enformer_feats.shape
    for i in range(nb_bins):
        f_out.create_dataset('bin_%d'%i, data=enformer_feats[:,i,:], dtype='float32')
    f_out.close()

if __name__=="__main__":
    main()
