# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.getcwd())

import matplotlib.pyplot as plt
from ABTestingFunctions import ABTesting
ABT = ABTesting() 
#pooled_SE, ab_dist, p_val

from PlottingFunctions import PlottingFunctions
PLTF = PlottingFunctions() 
#plot_null, plot_alt, show_area

class HypothesisPlot:
    def _init_(self):
        """
        Initializing HypothesisPlot class
        """
        
    def hypo_plot(self, Control, Exposed, bcr, mde, sig_level=0.05, show_power=False, show_beta=False,
                  show_alpha=False, show_p_value=False, show_legend=True):
        
        #create a plot object
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # define parameters to find pooled standard error
        X_C = bcr * Control
        X_E = (bcr + mde) * Exposed
        stderr = ABT.pooled_SE(Control, Exposed, X_C, X_E)
        
        # plot the distribution of the null and alternative hypothesis
        PLTF.plot_null(ax, stderr)
        PLTF.plot_alt(ax, stderr, mde)
        
        # set extent of plot area
        ax.set_xlim(-8 * stderr, 8 * stderr)
        
        # shade areas according to user input
        if show_power:
            PLTF.show_area(ax, mde, stderr, sig_level, area_type='power')
        if show_alpha:
            PLTF.show_area(ax, mde, stderr, sig_level, area_type='alpha')
        if show_beta:
            PLTF.show_area(ax, mde, stderr, sig_level, area_type='beta')
            
        # show p_value based on the binomial distributions for the two groups
        if show_p_value:
            null = ABT.ab_dist(stderr, 'control')
            p_value = ABT.p_val(Control, Exposed, bcr, bcr+mde)
            ax.text(3 * stderr, null.pdf(0),
                    'p-value = {0:.3f}'.format(p_value),
                    fontsize=12, ha='left')
            
        # option to show legend
        if show_legend:
            plt.legend()

        plt.xlabel('d')
        plt.ylabel('PDF')
        plt.show()
        
        
        