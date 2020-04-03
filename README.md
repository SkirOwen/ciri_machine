# ciri_machine
## Installation

To use this repository you will need to get the submodule for the data called `data_repo_JH`.  
For that, clone this repository and in that directory execute:

```
# When you clone the repository
git clone --recurse-submodules https://github.com/SkirOwen/ciri_machine.git

# If you already clone the repository
git submodule update --init --recursive
```  
If you want to update the submodule yourself: **I DON'T ADVISE THAT**
```
git submodule update --remote
```

### Requirements


The packages `pandas` and `tabula` are needed, pandas is already included in Anaconda.

Tabula can easily be install using pip:

```
pip install tabula-py
```

