import pandas as pd
import numpy as np
import random
import composicao_m21
import music21 as m21





df_gini = pd.read_csv('tables/gdp.csv', index_col="Country Name")
df_coord = pd.read_csv('tables/countries.csv', index_col="name")
df = df_gini.join(df_coord).fillna(0)

'''
composicao_m21.gera_melodias_extremais(df)
composicao_m21.gera_melodias_aleatorias(df, "GDP per capita", n_notas=20, ampliacao=2, nota_central="C4",
 nome_arq="sdd_3_1.xml", tonalidades=['c', 'c'])
 '''

a,b,c,u = composicao_m21.conjuntos_de_paises(df, "GDP per capita")
na = u-a
nb = u-b
nc = u-c

set_config = [(16, [('p', u), ('p', u)]),
              (16, [('pp', a.intersection(b)), ('mp', b.intersection(c))]),
              (16, [('mp', a.intersection(b).union(na.intersection(nb))), ('mf', a.intersection(b).intersection(c))])
]

s = composicao_m21.compose_with_sets(set_config, 2)
s.write('xml', 'sets0.xml')




