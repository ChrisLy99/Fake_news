def graph(mdl, outpath=None, **kwargs):

    img = mdl.graph # visualization of graph structure
    
    if outpath is not None:
        img.save(outpath)

    return