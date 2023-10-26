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

**Step 2**: 2)	Genomic features extraction

Use genomic large language model (e.g., [Enformer](https://www.nature.com/articles/s41592-021-01252-x)) to extract the genomic features, including gene expression, chromatin accessibility, ChIP-seq and histone modification signals across a diverse panel of cell lines and tissues, for each maternal and paternal sequence.












