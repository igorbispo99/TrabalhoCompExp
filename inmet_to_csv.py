import sys, os


#mdct,date,yr,mo,da,hr,prcp,stp,smax,smin,gbrd,temp,dewp,tmax,dmax,tmin,dmin,hmdy,hmax,hmin,wdsp,wdct,gust
inmet_to_csv = {
'Data'                                                 : "date",
'DATA (YYYY-MM-DD)'                                    : "date",
'Hora UTC'                                             : "hr",
'HORA (UTC)'                                           : "hr",
'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'                     : "prcp",
'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': "stp",
'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)'      : "smax",
'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)'     : "smin",
'RADIACAO GLOBAL (KJ/m²)'                              : "gbrd",
'RADIACAO GLOBAL (Kj/m²)'                              : "gbrd",
'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'         : "temp",
'TEMPERATURA DO PONTO DE ORVALHO (°C)'                 : "dewp",
'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'           : "tmax",
'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'           : "tmin",
'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)'     : "dmax",
'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)'     : "dmin",
'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)'             : "hmax",
'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'             : "hmin",
'UMIDADE RELATIVA DO AR, HORARIA (%)'                  : "hmdy",
'VENTO, DIREÇÃO HORARIA (gr) (° (gr))'                 : "wdct",
'VENTO, RAJADA MAXIMA (m/s)'                           : "gust",
'VENTO, VELOCIDADE HORARIA (m/s)'                      : "wdsp",
}


def read_metadata(file):
	head = []
	data = []

	sl = file.readline().split(';')
	assert(sl[0] == "REGI?O:" or sl[0] == "REGIÃO:" or sl[0] == "REGIAO:")
	data.append(sl[1].strip())
	head.append("region")

	sl = file.readline().split(';')
	assert(sl[0] == "UF:")
	data.append(sl[1].strip())
	head.append("prov")

	sl = file.readline().split(';')
	assert(sl[0] == "ESTAC?O:" or sl[0] == "ESTAÇÃO:" or sl[0] == "ESTACAO:")
	data.append(sl[1].strip())
	head.append("wsnm")

	sl = file.readline().split(';')
	assert(sl[0] == "CODIGO (WMO):")
	data.append(sl[1].strip())
	head.append("inme")

	sl = file.readline().split(';')
	assert(sl[0] == "LATITUDE:")
	data.append(sl[1].strip().replace(',','.'))
	head.append("lat")

	sl = file.readline().split(';')
	assert(sl[0] == "LONGITUDE:")
	data.append(sl[1].strip().replace(',','.'))
	head.append("lon")

	sl = file.readline().split(';')
	assert(sl[0] == "ALTITUDE:")
	data.append(sl[1].strip().replace(',','.'))
	head.append("elvt")

	sl = file.readline().split(';')
	assert(sl[0] == "DATA DE FUNDAC?O:" or sl[0] == "DATA DE FUNDAÇÃO (YYYY-MM-DD):" or sl[0] == "DATA DE FUNDACAO:")
	#data.append(sl[1].strip())
	#head.append("found")

	return (head,data)


def read_header(file):
	sl = file.readline().split(';')
	assert(sl[0] == 'Data' or "DATA (YYYY-MM-DD)")
	return [inmet_to_csv[x] for x in sl if x != '\n']


def replace_commas_strip_newline(l0):
	l1 = [x.replace(',','.') for x in l0 if x != '\n']
	l2 = [x
		.replace('00 UTC',':00')
		.replace('/','-')
		.replace('-9999', '')
		for x in l1
	]
	return l2

def read_csv(path):
	head = []
	meta = []
	body = []
	with open(path, "r") as file:
		head, meta = read_metadata(file)
		head += read_header(file)
		for line in file:
			sl = line.split(';')
			body.append(meta + replace_commas_strip_newline(sl))
	return (head, body)

def write_csv(head, body):
	with open("test.csv", "w") as file:
		file.write(','.join(head))
		file.write('\n')
		for line in body:
			file.write(','.join(line))
			file.write('\n')

paths = sorted([os.path.basename(f.path) for f in os.scandir(os.getcwd()) if f.is_dir()])
#paths = ['2019']
fpath = []

for path in paths:
	for f in os.scandir(path):
		if(f.path.find('BRASILIA') != -1):
			fpath.append(f.path)


#print(fpath)
csvs = []
for file_path in fpath:
	print(file_path)
	csvs.append(read_csv(file_path))

for csv0 in csvs:
	for csv1 in csvs:
		assert(csv0[0] == csv1[0])

with open("brasilia.csv", "w") as file:
	file.write(','.join(csvs[0][0]))
	file.write('\n')
	for csv in csvs:
		for line in csv[1]:
			file.write(','.join(line))
			file.write('\n')


#data = read_csv(fpath[0])
#write_csv(*data)



