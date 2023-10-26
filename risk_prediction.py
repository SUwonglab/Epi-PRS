import numpy as np
import os, sys
from sklearn.decomposition import PCA
import h5py
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

PATH = sys.argv[1]
pheno = sys.argv[2]
chr_id = sys.argv[3]
start = int(sys.argv[4])
end = int(sys.argv[5])

train_case_idx = []
train_control_idx = []
test_case_idx = []
test_control_idx = []


        
f_train_case = open("%s/%s_train_case_id.txt"%(PATH,pheno),"r")
f_test_case = open("%s/%s_test_case_id.txt"%(PATH,pheno),"r")
f_train_control = open("%s/%s_train_control_id.txt"%(PATH,pheno),"r")
f_test_control = open("%s/%s_test_control_id.txt"%(PATH,pheno),"r")

lines = f_train_case.readlines()
for i, line in enumerate(lines):
    data = line.strip().split()
    train_case_idx.append(data[0])
    
lines = f_train_control.readlines()
for i, line in enumerate(lines):
    data = line.strip().split()
    train_control_idx.append(data[0])

lines = f_test_case.readlines()
for i, line in enumerate(lines):
    data = line.strip().split()
    test_case_idx.append(data[0])
    
lines = f_test_control.readlines()
for i, line in enumerate(lines):
    data = line.strip().split()
    test_control_idx.append(data[0])

# load the genomic LLM features
X_train_case_p = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/case/%s_paternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in train_case_idx]) #(16000, 17, 5313)
X_train_case_m = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/case/%s_maternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in train_case_idx]) #(16000, 17, 5313)
X_test_case_p = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/case/%s_paternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in test_case_idx]) #(4000, 17, 5313)
X_test_case_m = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/case/%s_maternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in test_case_idx]) #(4000, 17, 5313)
X_train_control_p = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/control/%s_paternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in train_control_idx]) #(16000, 17, 5313)
X_train_control_m = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/control/%s_maternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in train_control_idx]) #(16000, 17, 5313)
X_test_control_p = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/control/%s_paternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in test_control_idx]) #(4000, 17, 5313)
X_test_control_m = np.stack([h5py.File('%s/enformer_h5/chr%s_%s_%s/control/%s_maternal.hdf5'%(PATH, chrom, start, end, item))['bin_%d'%bin_idx] 
            for item in test_control_idx]) #(4000, 17, 5313)


X_train =  np.concatenate([X_train_case_m,X_train_control_m,X_train_case_p,X_train_control_p],axis=0) #(64000, 17, 5313)
X_test =  np.concatenate([X_test_case_m,X_test_control_m,X_test_case_p,X_test_control_p],axis=0) #(16000, 17, 5313)

if not os.path.isdir('%s/feature/PCA/chr%s_%s_%s/'%(PATH, chrom, start, end)):
    os.mkdir('%s/feature/PCA/chr%s_%s_%s/'%(PATH, chrom, start, end))

if not os.path.isdir('%s/feature/mean/chr%s_%s_%s/'%(PATH, chrom, start, end)):
    os.mkdir('%s/feature/mean/chr%s_%s_%s/'%(PATH, chrom, start, end))

nb_regions = X_test_control_m.shape[1]
X_pca_train, X_pca_test = [], []
for i in range(nb_regions):
    pca = PCA(n_components=5)
    pca.fit(X_train[:,i,:])
    X_pca_train.append(pca.transform(X_train[:,i,:]))
    X_pca_test.append(pca.transform(X_test[:,i,:]))
X_pca_train = np.stack(X_pca_train)
X_pca_test = np.stack(X_pca_test)

np.save('%s/feature/mean/chr%s_%s_%s/chr%s_%s_%s_mean_train_feats_bin_%d.npy'%(PATH, chrom, start, end,chrom, start, end, bin_idx), np.mean(X_train,axis=1))

np.save('%s/feature/mean/chr%s_%s_%s/chr%s_%s_%s_mean_test_feats_bin_%d.npy'%(PATH, chrom, start, end,chrom, start, end, bin_idx), np.mean(X_test,axis=1))

np.save('%s/feature/PCA/chr%s_%s_%s/chr%s_%s_%s_PCA_train_feats_bin_%d.npy'%(PATH, chrom, start, end,chrom, start, end, bin_idx), X_pca_train)
np.save('%s/feature/PCA/chr%s_%s_%s/chr%s_%s_%s_PCA_test_feats_bin_%d.npy'%(PATH,chrom, start, end,chrom, start, end, bin_idx), X_pca_test)

#prediction
X_train =X_pca_train
X_test = X_pca_test
  
y_train = np.concatenate([np.ones(X_train.shape[0]//2),np.zeros(X_train.shape[0]//2)])
y_test = np.concatenate([np.ones(X_test.shape[0]//2),np.zeros(X_test.shape[0]//2)])

clf = LogisticRegression()
clf.fit(X_train, y_train)
auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
print(auc)
