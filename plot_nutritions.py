import matplotlib.pyplot as plt
import numpy as np

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')

class plot_nutritions():

    def __init__(self, dic):
        self.dic=dic

    def plot_figure(self):
        img = BytesIO()
        fig, ax = plt.subplots()

        font = {'family': 'serif',
                'weight': 'normal',
                'size': 20,
                }

        y=[]
        x=[]
        for item in self.dic:
            if item != 'Calories':
                y.append(item)
                x.append(self.dic[item])
        y_pos = np.arange(len(y))/4

        ax.barh(y_pos, x, height = 0.1, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(y, fontdict=font)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlim(0, max(x)+max(x)*0.4)
        ax.set_xlabel('g', fontdict=font)
        ax.set_title(f"Total {self.dic['Calories']} Calories", fontdict=font)
        ax.tick_params(axis="x", labelsize=20)
        


        for i in range(len(x)):
            index=y_pos[i]
            value=x[i]
            ax.text(value, index, str(value)+'g', fontdict=font)

        fig.savefig(img, format='png',bbox_inches='tight', transparent=True)
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return plot_url
