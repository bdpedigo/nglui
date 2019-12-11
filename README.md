Google's [Neuroglancer](https://github.com/google/neuroglancer) is an incredibly useful tool for connectomics and large 3d datasets, and a fork developed by the Seung lab is critical to the connectomics proofreading infrastructure here. One of Neuroglancer's best features is an incredibly robust python scripting interface, allowing a lot of programmatic interaction with states.

This is a set of tools designed to ease the programmatic generation of Neuroglancer states and close the loop between analysis and raw data. One component is an extension of the Neuroglancer 'viewer' object with a number of convenience functions for frequent operations and added functions to interact with new features in the Seung-lab fork such as a graphene segmentation layer backend. The other component, StateBuilder, is a framework to easily specify how to buid neuroglancer states out of schematized dataframes or numpy-style data. It's also designed to operate easily with [DashDataFrame](https://github.com/AllenInstitute/DashDataFrame) to interactively explore complex data.
