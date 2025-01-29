# Nanopore

Hi Dr. Sahoo,

This is the whole pipeline of Nanopore Sequencing Data that I have created.
It includes five four coding files:
dam_basecall.job
dam_agg_info_2.job
bw.job
GATC.py

It also includes a file of annotation for human genome:
hg38.chrom.sizes

Besides that, I have also used human reference genome downloaded from NCBI, but it can't be wrong and it is too big (3gb) to put into the github, so it is not here.

In **dam_basecall.job**, there are two major functions that I have used: 
dorado(https://github.com/nanoporetech/dorado)
modkit(https://github.com/nanoporetech/modkit)
The raw nanopore files are in *.pod5 filetypes, which are the raw signal file. Using dorado for basecalling, we transfer pod5->bam files. Using modkit, we can process bam->bed files.
The final version is bed files, and these are their annotation and description (https://github.com/nanoporetech/modkit?tab=readme-ov-file#bedmethyl-column-descriptions). 
Here is a sample of the first few lines of a bed file:
(base) [wzhao@login02 bed]$ head -n 20 PBA04723_d2e2fe71_b55ea731_31.sorted.bed
NC_000001.11    11690   11691   a       1       -       11690   11691   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11692   11693   a       1       -       11692   11693   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11693   11694   a       1       -       11693   11694   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11699   11700   a       1       -       11699   11700   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11700   11701   a       1       -       11700   11701   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11701   11702   a       1       -       11701   11702   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11706   11707   a       1       -       11706   11707   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11713   11714   a       1       -       11713   11714   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11719   11720   a       1       -       11719   11720   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11721   11722   a       1       -       11721   11722   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11723   11724   a       1       -       11723   11724   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11725   11726   a       1       -       11725   11726   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11726   11727   a       1       -       11726   11727   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11727   11728   a       1       -       11727   11728   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11728   11729   a       1       -       11728   11729   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11729   11730   a       1       -       11729   11730   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11730   11731   a       1       -       11730   11731   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11731   11732   a       1       -       11731   11732   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11735   11736   a       1       -       11735   11736   255,0,0 1       0.00    0       1       0       0       0       0       0
NC_000001.11    11736   11737   a       1       -       11736   11737   255,0,0 1       0.00    0       1       0       0       0       0       0

After dam_basecall.job, we have a folder of bed files. We need to aggregate all the information into one files. The columns that we are interested in is 1,2,6,10,12, which are chromosome, start position, strand, Nvalid_cov, and Nmod. So that I use **dam_agg_info_2.job** to aggregate information. I use chromosome, start position and strand as a key to iterate through every file and get the cumulative sum of Nvalid_cov and Nmod. After this step, we have aggregate all information that we need for analysis.

Since Dr. Rao likes us to visualize them in UCSC genome browser, we need a specific filetype: bigwig. The **bw.job** file is to transfer the file into bigwig file type and also calculate the mean and std of coverage. Since DAM methylates A in GATC motif, **GATC.py** is to find the A position in GATC motif in the whole genome.

Note: every position here should zero based, which means that the start position of every chromosome should be 0. 




