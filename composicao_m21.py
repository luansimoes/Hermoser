import pandas as pd
import numpy as np
import random
import music21 as m21


#ALCANCE MIDI: 0-127   19G0 - C#8
def lat_p_nota(lat, mediana, nota_central="C3", escala=m21.scale.MajorScale('C')):
	passo = int((lat-mediana)/3)
	if passo!=0:
		return escala.next(pitchOrigin=nota_central, direction=passo)
	else:
		return m21.pitch.Pitch(nota_central)


#dur_central = log(num_duracao, 2)
def long_p_duracao(lon, mediana, dur_central=0):
	return 2**(dur_central + round((lon-mediana)/72))

def traduz_pais(pais, mediana_lat, mediana_lon, nota_central='A3', escala=m21.scale.ChromaticScale('C')):
	return (lat_p_nota(pais['latitude'], mediana_lat, nota_central=nota_central, escala=escala), long_p_duracao(pais['longitude'], mediana_lon))



def gera_melodia(df, param, n_notas=10, nota_central=48, nome_arq="teste.xml", ampliacao=1):
	pesos = [(dado**ampliacao) if dado!=0 else 0 for dado in df[param]]
	ids = range(len(pesos))

	mediana_lat = df["latitude"].median()
	mediana_lon = df["longitude"].median()

	notas = random.choices(ids, pesos, k=n_notas)
	melodia_de_saida = []
	batida = 0

	for i in range(len(notas)):
		altura = lat_p_nota(df["latitude"][notas[i]], mediana_lat, nota_central)
		duracao = long_p_duracao(df["longitude"][notas[i]] , mediana_lon)
		nota = m21.note.Note(altura, duration=m21.duration.Duration(duracao))
		nota.offset = batida
		nota.storedInstrument = m21.instrument.Piano()
		print(altura)
		print(duracao)
		print()
		melodia_de_saida.append(nota)
		batida+=duracao

	stream_xml = m21.stream.Stream(melodia_de_saida)
	stream_xml.write('xml', nome_arq)



def gera_melodias_aleatorias(df, param, n_notas=10, nota_central="C3", nome_arq="contraponto_teste.xml", ampliacao=1,
	tonalidades=['c','c']):
	pesos = [(dado**ampliacao) if dado!=0 else 0 for dado in df[param]]
	pesos_inversos = [(dado**(-ampliacao)) if dado!=0 else 0 for dado in df[param]]
	pesos_divisao = [2**i for i in range(3)]
	
	ids = range(len(pesos))

	mediana_lat = df["latitude"].median()
	mediana_lon = df["longitude"].median()

	sort_1 = random.choices(ids, pesos, k=n_notas*4)
	sort_2 = random.choices(ids, pesos_inversos, k=n_notas)
	duracoes_1 = random.choices(ids, pesos, k=n_notas)
	divisoes = random.choices(list(reversed(pesos_divisao)), pesos_divisao, k=n_notas)
	#duracoes_2 = random.choices(ids, pesos, k=n_notas)


	notas_1 = [lat_p_nota(df["latitude"][nota], mediana_lat, nota_central, escala=m21.scale.MajorScale(tonalidades[0])) for nota in sort_1]
	notas_2 = [lat_p_nota(df["latitude"][nota], mediana_lat, nota_central, escala= m21.scale.MajorScale(tonalidades[1])) for nota in sort_2]
	durs_1 = [long_p_duracao(df["longitude"][duracao], mediana_lon) for duracao in duracoes_1]
	#durs_2 = [long_p_duracao(df["longitude"][duracao], mediana_lon) for duracao in duracoes_2]


	s = m21.stream.Stream()
	p0 = m21.stream.Part(id='part0')
	p1 = m21.stream.Part(id='part1')


	soma = i = 0
	while i<len(durs_1):
		denominador = divisoes[i]
		for j in range(denominador):
			nota = m21.note.Note(notas_1[soma], duration=m21.duration.Duration(durs_1[i]/denominador))
			nota.storedInstrument = m21.instrument.Piano()
			p0.append(nota)
			soma+=1
		i+=1


	for i in range(len(notas_2)):
		nota = m21.note.Note(notas_2[i], duration=m21.duration.Duration(durs_1[i]))
		#nota.offset = batida
		nota.storedInstrument = m21.instrument.Piano()
		p1.append(nota)
	
	s.insert(0,p0)
	s.insert(0,p1)
	s.write('xml', nome_arq)

def generate_offset(note, cur_offset, length, resolution):
	pitch, dur = note
	offset = random.choice([cur_offset + (i*resolution) for i in range(int(length/resolution))])
	n = m21.note.Note(pitch, duration=m21.duration.Duration(dur))
	n.offset = offset
	return n

def compose_with_sets(set_partition, n_voices):
	s = m21.stream.Stream()
	parts = [m21.stream.Part() for v in range(n_voices)]

	current_offset = 0
	for max_time, config in set_partition:
		i=0
		for din, notes_set in config:
			parts[i].append(m21.dynamics.Dynamic(din))
			for note in notes_set:
				new_note = generate_offset(note, current_offset, max_time, 0.5)
				print(new_note.offset)
				parts[i].insert(new_note.offset, new_note)
			i+=1
		current_offset+=max_time
	[s.insert(0, v) for v in parts]
	return s


			


 
'''
def gera_melodias_extremais(df, n_notas=10, nota_central=48, nome_arq="teste2.xml", ampliacao=1):

	mediana_lat = df["latitude"].median()
	mediana_lon = df["longitude"].median()

	lats_up = [dado for dado in df.loc[df["latitude"]>mediana_lat]["latitude"]]
	lats_down = [dado for dado in df.loc[df["latitude"]<=mediana_lat]["latitude"]]
	

	notas_up = random.choices(lats_up, k=n_notas)
	notas_down = random.choices(lats_down, k=n_notas)

	s = m21.stream.Stream()
	p0 = m21.stream.Part(id='part0')
	p1 = m21.stream.Part(id='part1')


	for i in range(len(notas_up)):
		altura = lat_p_nota(notas_up[i], mediana_lat, nota_central)
		duracao = long_p_duracao(notas_up[i] , mediana_lon)
		nota = m21.note.Note(altura, duration=m21.duration.Duration(duracao))
		#nota.offset = batida
		nota.storedInstrument = m21.instrument.Piano()

		print(altura)
		print(duracao)
		print()
		p0.append(nota)

	for i in range(len(notas_down)):
		altura = lat_p_nota(notas_down[i], mediana_lat, nota_central)
		duracao = long_p_duracao(notas_down[i] , mediana_lon)
		nota = m21.note.Note(altura, duration=m21.duration.Duration(duracao))
		#nota.offset = batida
		nota.storedInstrument = m21.instrument.Piano()

		print(altura)
		print(duracao)
		print()
		p1.append(nota)


	s.insert(0,p0)
	s.insert(0,p1)
	s.write('xml', nome_arq)
'''
