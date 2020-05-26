# NetOGlyc4.0-BulkAnalyzer

The NetOglyc server (http://www.cbs.dtu.dk/services/NetOGlyc/) produces neural network predictions of mucin type GalNAc O-glycosylation sites in mammalian proteins. This server receives input from a ".fasta" file of protein sequences and outputs data reflecting the likelihood that a given amino acid is O-glycosylated. This software is inherently difficult for bulk analysis of protein sequences. At most 50 sequences and 200,000 amino acids can be submitted at one time, with each sequence not to exceed more than 4,000 amino acids. 

The NetOGlyc4.0-BulkAnalyzer is an algorithm written in Python3 that is designed to specifically bypass these limitations. This algorithm takes a ".fasta" as an input file, breaks it down into parts, and systematically submits the data to the NetOGlyc server for prediction of O-glycosylation sites. The program will then query the result pages until all the results are processed, at which point the data will be output into a ".text" file.

I hope that this program enhances your ability to make scientific discoveries.

Zacko
