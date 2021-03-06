.. _loading_data:

*************************************
Loading Data
*************************************

HiFive data is handled using the :class:`FiveCData <hifive.fivec_data.FiveCData>` and :class:`HiCData <hfiive.hic_data.HiCData>` classes.

.. _fivec_data_loading:

Loading 5C data
===============

HiFive can load 5C data from one of two source file types.

BAM Files
---------

When loading 5C data from BAM files, they should always come in pairs, one for each end of the paired-end reads. HiFive can load any number of pairs of BAM files, such as when multiple sequencing lanes have been run for a single replicate. These files do not need to be indexed or sorted. All sequence names that these files were mapped against should exactly match the primer names in the BED file used to construct the Fragment object.

Count Files
------------

Counts files are tabular text files containing pairs of primer names and a count of the number of observed occurrences of that pairing.

::

  5c_for_primer1   5c_rev_primer2    10
  5c_for_primer1   5c_rev_primer4    3
  5c_for_primer3   5c_rev_primer4    18

.. _hic_data_loading:

Loading HiC Data
================

HiFive can load HiC data from three different types of source files.

BAM Files
---------

When loading HiC data from BAM files, they should always come in pairs, one for each end of the paired-end reads. HiFive can load any number of pairs of BAM files, such as when multiple sequencing lanes have been run for a single replicate. These files do not need to be indexed or sorted. For faster loading, especially with very large numbers of reads, it is helpful to parse out single-mapped reads to reduce the number of reads that HiFive needs to traverse in reading the BAM files.

RAW Files
---------

RAW files are tabular text files containing pairs of read coordinates from mapped reads containing the chromosome, coordinate, and strand for each read end. HiFive can load any number of RAW files into a single HiC Data object.

::

  chr1    30002023    +    chr3    4020235    -
  chr5    9326220     -    chr1    3576222    +
  chr8    1295363     +    chr6    11040321   +

MAT Files
---------

MAT files are in a tabular text format previously defined for `HiCPipe <http://www.wisdom.weizmann.ac.il/~eitany/hicpipe/>`_. This format consists of a pair of fend indices and a count of observed occurrences of that pairing. These indices must match those associated with the Fend object used when loading the data. Thus it is wise when using this format to also create the Fend object from a HiCPipe-style fend file to ensure accurate fend-count association.

::

  fend1    fend2    count
  1        4        10
  1        10       5
  1        13       1

.. note::
    In order to maintain compatibility with HiCPipe, both tabular fend files and MAT files are 1-indexed, rather than the standard 0-indexed used everywhere else with HiFive.

.. _matrix_files:

MATRIX Files
------------

HiC data may be loaded from matrix files in one of three formats: HDF5, NPZ, or TXT.

HDF5 Matrix Files
++++++++++++++++++

The data file format is inferred from the file extension ('.hdf5'). Heatmap HDF5 files generated by HiFive are compatible with loading. HiFive expects one numpy array per chromosome and chromosome pair (if trans data is included) and will search for files for corresponding to every chromosome and chromosome pair. Acceptable matrix names are '*', '*.counts', '*.observed', 'chr*', 'chr*.counts', and 'chr*.observed' where '*' is either a chromosome name or pair of chromsome names separated by '_by_' for trans interactions. Cis-interaction matrices may be in either square or upper-triangular matrices. Positions may be given by matrices names '*.positions' or 'chr*.positions' and contain two columns, starting and ending positions for each bin for a chromosome. If no positions are given, then bins are assumed to correspond to those found in the fend file associated with the data object. Further, if the matrix is one-dimensional and the attribute 'diagonal' is included and equals 'True', the upper triangular matrix is assumed to include the diagonal (self-interacting bins). Otherwise it is assumed to be absent.

NPZ Matrix Files
+++++++++++++++++

The data file format is inferred from the file extension ('.npz'). Heatmap NPZ files generated by HiFive are compatible with loading. HiFive expects one numpy array per chromosome and chromosome pair (if trans data is included) and will search for files for corresponding to every chromosome and chromosome pair. Acceptable matrix names are '*', '*.counts', '*.observed', 'chr*', 'chr*.counts', and 'chr*.observed' where '*' is either a chromosome name or pair of chromsome names separated by '_by_' for trans interactions. Cis-interaction matrices may be in either square or upper-triangular matrices. Positions may be given by matrices names '*.positions' or 'chr*.positions' and contain two columns, starting and ending positions for each bin for a chromosome. If no positions are given, then bins are assumed to correspond to those found in the fend file associated with the data object. Further, if the matrix is one-dimensional, the upper triangular matrix is assumed to include the diagonal (self-interacting bins).

TXT Matrix Files
++++++++++++++++++++

Text matrix files are inferred from the presence of the '*' character in the filename. A generic format filename with the chromosome name or chromosome pair should be passed and all chromosomes and pairs will be searched, replacing the '*' with the appropriate name (e.g. 40Kb_counts_*.matrix). Text matrix files are tab-separated files that contain a rectangular matrix of values corresponding to binned read counts. These files can contain labels with the first line containing a tab followed by a tab-separated list of bin labels and each subsequent line containing a label followed by bin values. Labels should be in a format such that the bin position occurs after the '|' character and in the form chrX:XXXX-XXXX (e.g. interval1|myexpriment|chr3:1000000-1040000). If no labels are provided, bins are assumed to be identical to the partitioning in the associated Fend object and starting with the first bin for the associated chromosome(s). Labeled matrices need not include all rows or columns for a given paritioning. Values falling outside of bins are discarded.

.. note::
  In order to pass the filename format with the '*' character, you must enclose the name in quotation marks (e.g. -X "your_name_*.matrix").
