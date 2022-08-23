# Export Draw io to MD
This small utility converts tree-like structures from draw io to lists in markdown, where each point's indentation level corresponds to "depth" in tree from draw io.
I wrote it quickly so don't expect great code, but it does its work well.

## Use
``` python
python exportDrawioToMD.py [inputFilepath] [outputFilepath
```

### Examples
It's working for structures like
``` mermaid
graph RL
  Master --> A & B & C
  C --> D & F
```
or 
``` mermaid
graph RL
  Master2 --> A1 & B2 & C3
  C3 --> D4 & F5
  A1 & B2 & D4 & F5 --> End
```
in which case in your markdown file this last entity is going to be repeated as many times as there are arrow connected to it.
but it's breaking on
``` mermaid
graph RL
A ---> B
B ---> A
```

### To be done
- [ ] Refactor the code
