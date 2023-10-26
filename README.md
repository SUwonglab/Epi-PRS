# Epi-PRS
We present Epi-PRS, a polygenic prediction method that leverages genomic large language models to transform personal sequences to personal genomic and epigenomic features for disease risk modeling.

# Environment
- Python=3.9.0
- TensorFlow == 2.8.0
- TensorFlow-hub == 0.11.0
- Java JDK == 1.8.0
- h5py == 3.6.0

# Installation
Epi-PRS can be downloaded by
```shell
git clone https://github.com/kimmo1019/hicGAN
```
Installation has been tested in a Linux platform.

# Instructions
We provide detailed step-by-step instructions for running Epi-PRS.

**Step 1**: Personal genome construction

Given the variant call format (VCF) file that contains the genetics profile of all individuals, we first use Vcftools to remove all the indels and only keep the SNPs. Second, we use the reference-free Beagle software for phasing genotypes. Third, we use a personal genome construction tool vcf2diploid to obtain the paternal and maternal personal genome for each individual.






