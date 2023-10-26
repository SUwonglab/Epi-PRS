# Epi-PRS
We present Epi-PRS, a polygenic prediction method that leverages genomic large language models to transform personal sequences to personal genomic and epigenomic features for disease risk modeling.

# Environment
- Python=3.9.0
- TensorFlow == 2.8.0
- TensorFlow-hub == 0.11.0
- Java JDK == 1.8.0
- h5py == 3.6.0
- pyfasta == 0.5.2

# Installation
Epi-PRS can be downloaded by
```shell
git clone https://github.com/kimmo1019/hicGAN
```
Installation has been tested in a Linux platform.

# Instructions
We provide detailed step-by-step instructions for running Epi-PRS.

**Step 1**: Personal Genome Construction

Given the variant call format (VCF) file that contains the genetics profile of all individuals, we first use [VCFtools](https://vcftools.sourceforge.net/) to remove all the indels and only keep the SNPs. Second, we use the reference-free [Beagle software](https://faculty.washington.edu/browning/beagle/beagle.html#download) for phasing genotypes. Third, we use a personal genome construction tool [vcf2diploid](https://github.com/abyzovlab/vcf2diploid) to obtain the paternal and maternal personal genome for each individual.

Phasing genotypes using 

```shell
java -jar beagle.22Jul22.46e.jar gt=<Genotype> out=<Haplotype> map=plink.$3.GRCh37.map
```
where `beagle.22Jul22.46e.jar` can be downloaded from [here](https://faculty.washington.edu/browning/beagle/beagle.22Jul22.46e.jar). Both genotype and haplotype are in `.vcf` format.

Constructing personal genome using

```shell
java -jar vcf2diploid.jar -outDir <Per_Genome>  -id <ID>  -chr <Ref_Genome> -vcf <Haplotype>
```
where `Per_Genome` is the output personal genome in FASTA format. `ID` is the individual ID from the vcf file. `Ref_Genome` is the reference genome (e.g., chr4.fa). `Haplotype` is the haplotype file (.vcf) from the last step. Note that this command needs to be run multiple times to extract the personal genome for all the individuals. For a given LD, you only need to construct the personal genome for the corresponding chromosome.

**Step 2**:	Genomic Features Extraction

Use genomic large language model (LLM) (e.g., [Enformer](https://www.nature.com/articles/s41592-021-01252-x)) to extract the genomic features, including gene expression, chromatin accessibility, ChIP-seq and histone modification signals across a diverse panel of cell lines and tissues, for each maternal and paternal sequence.

Obtaining the genomic LLM features using
```shell
python3 get_enformer_feats.py <chrom> <start> <end> <parent> <fasta_path> <save_path>
[chrom] - chromosome ID (e.g., 1 to 22)
[start] - start position
[end] - end position
[parent] - paternal or maternal
[fasta_path] - path to the personal genome FASTA file in the last step
[save_path] - path to save the genomic LLM features (end with .hdf5)
```
Note that the first three parameters `chrom`,`start`,and `end` can be obtained from the LD list in both `breast` or `diabetes` folder. This program also needs to be run multiple times in order to get the genomic LLM features for all the individuals.

**Step 3**:	Risk Prediction

A logistic regression model for binary classification setting and an elastics-net model for regression setting will be built based on the individual reduced-dimension features and the phenotype. We randomly select 80% of both case and control subjects as training set and the remaining 20% as testing set.

Risk prediction using
```shell
python3 risk_prediction.py <PATH> <pheno> <chrom> <start> <end>
[PATH] - path to the project (e.g., ./)
[pheno] - phenotype (e.g., breast or diabetes)
[chrom] - chromosome ID (e.g., 1 to 22)
[start] - start position
[end] - end position
```
We applied a dimension reduction using PCA for each 128 bp bin and only kept 5 PCs, then the PCs are pooled for all bins and fed to a logistic regression for predicting the phenotype.












