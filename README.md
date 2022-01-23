# VGP parameter optimization

## Workflow details:

### Full purge_dups pipeline

It includes the [full post-assembly pipeline](https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_genome_assembly/tutorial.html#post-assembly-processing): read-depth analysis, generation of all versus all self-alignment and resolution of haplotigs and overlaps. In addition, it runs QUAST and Merqury both at the beginning and the end.

- Workflow ID: 69be0fb8276753ec
    
- Input files:
  - Pacbio HiFi reads
  - Draft assembly
  - K-mer database

### Partial purge_dups pipeline

In includes only the thid stage of the purge_dups pipeline (resolution of haplotics and overlaps) and a final report by running QUAST and Merqury.

- Workflow ID: 3480204a99bf4a35
- Input files:
  - Draft assembly
  - K-mer database
  - Pacbio HiFi reads
  - Calcuts report
  - PBCSTAT report
  - Self-homologous map