'''
Created on Jul 26, 2016

@author: cesar
'''

from matplotlib import pyplot as plt


def levelMarkGraphsLabels(marksDictionary,date0,datef,rates=True,save=None):
    """
    Plots of the marks
    """
    levels = marksDictionary.keys()
    levels.sort()
    levelToIndices = dict(zip(levels,range(len(levels))))

    fig, axes = plt.subplots(nrows=len(levels),ncols=1, figsize=(6,6))

    for wa, dateTimes in marksDictionary.iteritems():
        marks = [(d-date0).total_seconds() for d in dateTimes]
        w = levelToIndices[wa]
        axes[w].vlines(marks, ymin=0,ymax=1)
        axes[w].get_xaxis().set_visible(False)
        ax2 = axes[w].twinx()
        ax2.set_ylabel(str(w))
        ax2.set_yticks([])
        if(rates):
            axes[w].set_ylabel(len(marks))
        axes[w].set_yticks([])
        axes[w].tick_params(axis=u'both', which=u'both',length=0)
    if save != None:
        plt.savefig(save)
        
def levelMarkGraphs(marksDictionary,date0,datef):
    """
    Plots of the marks
    """
    levels = marksDictionary.keys()
    levels.sort()
    levelToIndices = dict(zip(levels,range(len(levels))))
    fig, axes = plt.subplots(nrows=len(levels),ncols=1, figsize=(6,6))
    for wa, dateTimes in marksDictionary.iteritems():
        marks = [(d-date0).total_seconds() for d in dateTimes]
        w = levelToIndices[wa]
        axes[w].vlines(marks, ymin=0,ymax=1)
        axes[w].get_xaxis().set_visible(False)
        axes[w].get_yaxis().set_visible(False)
    plt.show()