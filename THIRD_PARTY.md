# Sources and scope

## Cortical area graph
Downloaded from https://s3.amazonaws.com/connectome-graphs/cat/mixed.species_brain_1.graphml through the Cat entry at https://neurodata.io/project/connectomes/ . The upstream filename says mixed.species; its classification as Cat comes from that catalog. Graph metadata cites https://doi.org/10.1523/JNEUROSCI.1448-13.2013 and tract tracing. The graph is unweighted, directed, 65 nodes / 1,139 edges. Missing edges are not proof of biological absence. No synapse counts, neurotransmitters or physiological parameters are supplied. Retain upstream rights and attribution; no new data license is asserted.

## Anatomy
CATLAS, Daniel Stolzberg, Christina Wong, Blake E. Butler and Stephen G. Lomber (2017), https://doi.org/10.1002/cne.24271 ; https://github.com/CerebralSystemsLab/CATLAS .

The existing project conversion takes 74 original Slicer VTK region surfaces, removes duplicate aliases for regions 32 and 36, converts triangle strips to triangles, changes RAS to Y-up (x,z,-y), uniformly centers/scales, and divides surfaces by triangle centroid at the midsagittal plane. The result has 148 display pieces, not 148 independent regions. The original repository has no explicit standalone data license. Attribution does not assign one; rights remain with the original authors. No anatomy-to-graph registration has been established.

## Gameplay and demonstration
A five-second excerpt (source 26–31 seconds) of the user-supplied local MSTQX gameplay recording: https://www.youtube.com/watch?v=eKc0W0xMYkI . Resized/cropped for a small research fixture, original source audio retained. Subway Surfers and its audiovisual content belong to their respective rights holders. The demonstration screenshot was generated in this project from the same supplied footage and CATLAS geometry; synthetic cortical animation is not biological measurement. These materials are not relicensed as project code.

## Reference implementation
Stonkfly by nftechie, https://github.com/nftechie/stonkfly , inspected at revision 78ef3e05ab0fa086032098558d893667068944a0. Used as an architectural reference for asset verification, sensory isolation, offline execution and reproducibility. No Stonkfly code or MaleCNS dataset is copied into this repository.

## Optional physiology
CRCNS pvc-3: https://crcns.org/data-sets/vc/pvc-3/about/ . The evoked subset contains ten simultaneously recorded cells in cat area 17; spontaneous recordings are not substitutes for paired image-response examples. Raw data and trained weights are not included. Access and permitted reuse are governed by CRCNS and the data contributors.
