#!/usr/bin/python
# -*- coding: utf-8 -*-


import urlparse,json,zlib,hashlib,time,re,os,sys,xbmc,xbmcgui,xbmcplugin,xbmcvfs,pprint, base64
import unicodedata
import controlo
import Player
import URLResolverMedia
import Downloader
import Database
import Trakt
reload(sys)  
sys.setdefaultencoding('utf8')
class mrpiracy:

	def __init__(self):
		self.API = base64.urlsafe_b64decode('aHR0cDovL215YXBpbXAudGsv')
		self.API_SITE = base64.urlsafe_b64decode('aHR0cDovL215YXBpbXAudGsvYXBpLw==')
		self.SITE = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5Lm1sLw==')
	
	def definicoes(self):
		controlo.addon.openSettings()
		controlo.addDir('Entrar novamente','url', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
		#vista_menu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	def menu(self):
		login = self.login()
		database = Database.isExists()

		if login:
			controlo.addDir('Filmes', self.API_SITE+'filmes', 'menuFilmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
			controlo.addDir('Séries', self.API_SITE+'series', 'menuSeries', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
			controlo.addDir('Animes', self.API_SITE+'animes', 'menuAnimes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
			controlo.addDir('Pesquisa', self.API_SITE+'pesquisa', 'pesquisa', os.path.join(controlo.artFolder, controlo.skin, 'procurar.png'))
			controlo.addDir('', '', '', os.path.join(controlo.artFolder, controlo.skin, 'nada.png'))
			if Trakt.loggedIn():
				self.getTrakt()
				controlo.addDir('Trakt', self.API_SITE+'me', 'menuTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
			controlo.addDir('A Minha Conta '+self.getNumNotificacoes(), self.API_SITE+'me', 'conta', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			controlo.addDir('Definições', self.API_SITE, 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			
			
		else:
			controlo.addDir('Alterar Definições', 'url', 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			controlo.addDir('Entrar novamente', 'url', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
	def loginTrakt(self):
		Trakt.traktAuth()
	def getTrakt(self):
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/movies' % controlo.addon.getSetting('utilizadorTrakt')
		filmes = Trakt.getTrakt(url, login=False)
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt')
		series = Trakt.getTrakt(url, login=False)
		#insertTraktDB(filmes, series, data)
		url = 'https://api-v2launch.trakt.tv/sync/watchlist/movies'
		watchlistFilmes = Trakt.getTrakt(url)
		url = 'https://api-v2launch.trakt.tv/sync/watchlist/shows'
		watchlistSeries = Trakt.getTrakt(url)
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt')
		progresso = Trakt.getTrakt(url, login=False)
		Database.insertTraktDB(filmes, series, watchlistFilmes, watchlistSeries, progresso, controlo.dataHoras)
	def menuFilmes(self):
		controlo.addDir('Todos os Filmes', self.API_SITE+'filmes', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		controlo.addDir('Filmes em Destaque', self.API_SITE+'filmes/destaque', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		controlo.addDir('Filmes por Ano', self.API_SITE+'filmes/ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Filmes por Genero', self.API_SITE+'filmes/categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
	def menuTrakt(self):
		controlo.addDir('Progresso', self.API_SITE+'filmes', 'progressoTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Filmes', self.API_SITE+'filmes/destaque', 'traktWatchlistFilmes', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Series', self.API_SITE+'filmes/ano', 'traktWatchlistSeries', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
	def menuSeries(self):
		controlo.addDir('Todos as Séries', self.API_SITE+'series', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		controlo.addDir('Séries em Destaque', self.API_SITE+'series/destaque', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		controlo.addDir('Séries por Ano', self.API_SITE+'series/ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Séries por Genero', self.API_SITE+'series/categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
	def menuAnimes(self):
		controlo.addDir('Todos os Animes', self.API_SITE+'animes', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		controlo.addDir('Animes em Destaque', self.API_SITE+'animes/destaque', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		controlo.addDir('Animes por Ano', self.API_SITE+'animes/ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Animes por Genero', self.API_SITE+'animes/categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
	def login(self):
		"""if controlo.addon.getSetting('loggedin') != '':
			xbmc.executebuiltin("XBMC.Notification(MrPiracy, Sessão iniciada: "+controlo.addon.getSetting('loggedin')+", '10000', "+controlo.addonFolder+"/icon.png)")
			return True"""
		if controlo.addon.getSetting('email') == '' or controlo.addon.getSetting('password') == '':
			controlo.alerta('MrPiracy', 'Precisa de definir o seu email e password')
			return False
		else:
			try:
				post = {'username': controlo.addon.getSetting('email'), 'password': controlo.addon.getSetting('password'),'grant_type': 'password', 'client_id': 'kodi', 'client_secret':'pyRmmKK3cbjouoDMLXNtt2eGkyTTAG' }

				resultado = controlo.abrir_url(self.API_SITE+'login', post=json.dumps(post), header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				xbmc.log(resultado)
				resultado = json.loads(resultado)
				#colocar o loggedin
				token = resultado['access_token']
				refresh = resultado['refresh_token']
				headersN = controlo.headers
				headersN['Authorization'] = 'Bearer %s' % token
				
				resultado = controlo.abrir_url(self.API_SITE+'me', header=headersN)
				resultado = json.loads(resultado)
				try:
					username = resultado['username'].decode('utf-8')
				except:
					username = resultado['username'].encode('utf-8')
				

				if resultado['email'] == controlo.addon.getSetting('email'):
					xbmc.executebuiltin("XBMC.Notification(MrPiracy, Sessão iniciada: "+username+", '10000', "+controlo.addonFolder+"/icon.png)")
					controlo.addon.setSetting('tokenMrpiracy', token)
					controlo.addon.setSetting('refreshMrpiracy', refresh)
					controlo.addon.setSetting('loggedin', username)
					return True
			except:
				controlo.alerta('MrPiracy', 'Não foi possível abrir a página. Por favor tente novamente')
	        	return False

	def getNumNotificacoes(self):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(self.API_SITE+'me', header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		devolve = '[B][COLOR red]'
		devolve += str(resultado['notificacoes'])+' notificacoes e '+str(resultado['mensagens'])+' mensagens'
		devolve += '[/COLOR][/B]'
		return devolve

	def conta(self):
		controlo.addDir('Favoritos', self.API_SITE+'favoritos', 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'favoritos.png'))
		controlo.addDir('Agendados', self.API_SITE+'verdepois', 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'agendados.png'))
		controlo.addDir('Notificações', self.API_SITE+'notificacoes', 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
		controlo.addDir('Mensagens', self.API_SITE+'mensagens', 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
	def favoritos(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		vistos = Database.selectTraktDB()
		for i in resultado['data']:
			categoria = i['categoria1']
			if i['categoria2'] != '':
				categoria += ','+i['categoria2']
			if i['categoria3'] != '':
				categoria += ','+i['categoria3']
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			cor = "white"
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if i['visto'] == 1:
				visto = True
				
			else:			
				if Trakt.loggedIn():
					for v in json.loads(vistos[1]):
						if v["movie"]["ids"]["imdb"] is None:
							continue
						if v["movie"]["ids"]["imdb"] == i['IMBD']:
							visto = True
							cor = "blue"
							break
						else:
							visto = False
				else:
					visto = False

			try:
				nome = i['nome_ingles'].decode('utf-8')
			except:
				nome = i['nome_ingles'].encode('utf-8')
			if 'http' not in i['foto']:
				i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
			if i['tipoVideo'] == 'filme':
				infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }
				controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(i['id_video']), 'player', i['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+i['background'], trailer=i['trailer'])
			elif i['tipoVideo'] == 'serie' or i['tipoVideo'] == 'anime':
				infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
				controlo.addDir('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+i['tipoVideo']+'/'+str(i['id_video']), 'temporadas', i['foto'], tipo='serie', infoLabels=infoLabels, poster=self.SITE+i['background'],visto=visto)
		current = resultado['meta']['pagination']['current_page']
		total = resultado['meta']['pagination']['total_pages']
		try: proximo = resultado['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

	def verdepois(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		vistos = Database.selectTraktDB()
		for i in resultado['data']:
			categoria = i['categoria1']
			if i['categoria2'] != '':
				categoria += ','+i['categoria2']
			if i['categoria3'] != '':
				categoria += ','+i['categoria3']
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			cor = "white"
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if i['visto'] == 1:
				visto = True
			
			else:
				if Trakt.loggedIn():
					for v in json.loads(vistos[1]):
						if v["movie"]["ids"]["imdb"] is None:
							continue
						if v["movie"]["ids"]["imdb"] == i['IMBD']:
							visto = True
							cor = "blue"
							break
						else:
							visto = False
				else:
					visto = False
			try:
				nome = i['nome_ingles'].decode('utf-8')
			except:
				nome = i['nome_ingles'].encode('utf-8')
			if 'http' not in i['foto']:
				i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
			if i['tipoVideo'] == 'filme':
				infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }
				controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(i['id_video']), 'player', i['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+i['background'], trailer=i['trailer'])
			elif i['tipoVideo'] == 'serie' or i['tipoVideo'] == 'anime':
				infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
				controlo.addDir('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+i['tipoVideo']+'/'+str(i['id_video']), 'temporadas', i['foto'], tipo='serie', infoLabels=infoLabels, poster=self.SITE+i['background'],visto=visto)
		current = resultado['meta']['pagination']['current_page']
		total = resultado['meta']['pagination']['total_pages']
		try: proximo = resultado['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

	def notificacoes(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultadoa = controlo.abrir_url(url, header=controlo.headers)
		if resultadoa == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultadoa = json.loads(resultadoa)
		vistos = Database.selectTraktDB()
		for i in resultadoa["data"]:
			if i['tipoVideo'] == 'filme':
				resultado = controlo.abrir_url(self.API_SITE+'filme/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				pt = ''
				br = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				cor = "white"
				if 'PT' in resultado['IMBD']:
					resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if resultado['visto'] == 1:
					visto = True
				
				else:			
					if Trakt.loggedIn():
						for v in json.loads(vistos[1]):
							if v["movie"]["ids"]["imdb"] is None:
								continue
							if v["movie"]["ids"]["imdb"] == resultado['IMBD']:
								visto = True
								cor = "blue"
								break
							else:
								visto = False
					else:
						visto = False
			
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
		
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot':resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
				controlo.addVideo('[COLOR white]'+i['mensagem']+'[/COLOR]', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+resultado['background'], trailer=resultado['trailer'])
			elif i['tipoVideo'] == ('serie' or 'anime'):
				resultado = controlo.abrir_url(self.API_SITE+i['tipoVideo']+'/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				pt = ''
				br = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if 'PT' in resultado['IMBD']:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
		
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
				controlo.addDir('[COLOR white]'+i['mensagem']+'[/COLOR]', self.API_SITE+i['tipoVideo']+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels, poster=self.SITE+resultado['background'])

		current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))


	def mensagens(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultadoa = controlo.abrir_url(url, header=controlo.headers)
		if resultadoa == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultadoa = json.loads(resultadoa)
		for i in resultadoa["data"]:
			controlo.addDir(i['mensagem'], url, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))

		current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

	def filmes(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		vistos = Database.selectTraktDB()
		for i in resultado['data']:
			categoria = i['categoria1']
			if i['categoria2'] != '':
				categoria += ','+i['categoria2']
			if i['categoria3'] != '':
				categoria += ','+i['categoria3']
			pt = ''
			cor = "white"
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if i['visto'] == 1:
				visto = True
			
			else:			
				if Trakt.loggedIn():
					for v in json.loads(vistos[1]):
						if v["movie"]["ids"]["imdb"] is None:
							continue
						if v["movie"]["ids"]["imdb"] == i['IMBD']:
							visto = True
							cor = "blue"
							break
						else:
							visto = False
				else:
					visto = False

			infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }
			
			try:
				nome = i['nome_ingles'].decode('utf-8')
			except:
				nome = i['nome_ingles'].encode('utf-8')
			if 'http' not in i['foto']:
				i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
			controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(i['id_video']), 'player', i['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+i['background'], trailer=i['trailer'])
			
		current = resultado['meta']['pagination']['current_page']
		total = resultado['meta']['pagination']['total_pages']
		try: proximo = resultado['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
	def series(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'serie'
		elif 'anime' in url:
			tipo = 'anime'
		for i in resultado['data']:
			categoria = i['categoria1']
			if i['categoria2'] != '':
				categoria += ','+i['categoria2']
			if i['categoria3'] != '':
				categoria += ','+i['categoria3']
			br = ''
			pt = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in i['IMBD']:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
		
			try:
				nome = i['nome_ingles'].decode('utf-8')
			except:
				nome = i['nome_ingles'].encode('utf-8')
			if 'http' not in i['foto']:
				i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
			if i['visto'] == 1:
				visto=True
			else:
				visto=False
			controlo.addDir(pt+br+nome+' ('+i['ano']+')', self.API_SITE+tipo+'/'+str(i['id_video']), 'temporadas', i['foto'], tipo='serie', infoLabels=infoLabels,poster=self.SITE+i['background'],visto=visto)
		current = resultado['meta']['pagination']['current_page']
		total = resultado['meta']['pagination']['total_pages']
		try: proximo = resultado['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'series', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

	def temporadas(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		j=1
		while j <= resultado['temporadas']:
			controlo.addDir("[B]Temporada[/B] "+str(j), url+'/temporada/'+str(j), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporada'+str(j)+'.png'),poster=self.SITE+resultado['background'])
			j+=1

	def episodios(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'serie'
		elif 'anime' in url:
			tipo = 'anime'
		
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultadoS = controlo.abrir_url(self.API_SITE+tipo+'/'+url.split('/')[5], header=controlo.headers)
		resultadoS = json.loads(resultadoS)
		vistos = Database.selectTraktDB()
		for i in resultado['data']:
			if i['URL'] == '' and i['URL2'] == '':
				continue
			pt = ''
			categoria = resultadoS['categoria1']
			if resultadoS['categoria2'] != '':
				categoria += ','+resultadoS['categoria2']
			if resultadoS['categoria3'] != '':
				categoria += ','+resultadoS['categoria3']
			infoLabels = {'Title': i['nome_episodio'], 'Code': i['IMBD'], 'Episode': i['episodio'], 'Season': i['temporada'] }
			try:
				nome = i['nome_episodio'].decode('utf-8')
			except:
				nome = i['nome_episodio'].encode('utf-8')
			br = ''
			final = ''
			semLegenda = ''
			if i['fimtemporada'] == 1:
				final = '[B]Final da Temporada [/B]'
			if i['semlegenda'] == 1:
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			vistoe = False
			cor = 'white'
			if i['visto'] == 1:
				visto = True
			
			else:
				if Trakt.loggedIn():			
					ep = i['episodio']
					if '/' in i['episodio']:
						ep = i['episodio'].split('/')[0]
					if 'e' in i['episodio']:
						ep = i['episodio'].split('e')[0]
					for v in json.loads(vistos[2]):
						if v["show"]["ids"]["imdb"] is None:
							visto = False
							continue
						if v["show"]["ids"]["imdb"] != i['imdbSerie']:
							visto = False
							continue
						else:
							for s in v["seasons"]:
								if int(s['number']) == int(i['temporada']):
									for e in s['episodes']:
										if int(e["number"]) == int(ep):
											vistoe = True
											break
										else:
											vistoe = False
				else:
					visto = False
						
			if vistoe:
				visto = True
				cor = 'blue'


			if i['imagem'] == 1:
				imagem = self.SITE+'images/capas/'+i['IMBD']+'.jpg'
			elif i['imagem'] == 0:
				if 'http' not in resultadoS['foto']:
					imagem = self.SITE+'images/capas/'+resultadoS['foto'].split('/')[-1]
				else:
					imagem = resultadoS['foto']
			
			controlo.addVideo(pt+br+final+semLegenda+'[COLOR '+cor+'][B]Episodio '+str(i['episodio'])+'[/B][/COLOR] '+nome, self.API_SITE+tipo+'/'+str(i['id_serie'])+'/episodio/'+str(i['id_episodio']), 'player', imagem, visto, 'episodio', i['temporada'], i['episodio'], infoLabels, self.SITE+i['background'])
	def listagemAnos(self, url):
		anos = [
			'2016',
			'2015',
			'2014',
			'2013',
			'2012',
			'2011',
			'2010',
			'2009',
			'2008',
			'2007',
			'2006',
			'2000-2005',
			'1990-1999',
			'1980-1989',
			'1970-1979',
			'1960-1969',
			'1950-1959',
			'1900-1949'
		]
		for i in anos:
			controlo.addDir(i, url+'/'+i, 'anos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
	def listagemGeneros(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(self.API_SITE+'categorias', header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)

		for i in resultado:
			if i['id_categoria'] == 0:
				continue
			if 'filme' not in url and i['tipo'] == 1:
				continue
			controlo.addDir(i['categorias'], url+'/'+str(i['id_categoria']), 'categorias', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))

	def anos(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultadoa = json.loads(resultado)
		vistos = Database.selectTraktDB()

		for i in resultadoa["data"]:
			if 'filme' in url:
				resultado = controlo.abrir_url(self.API_SITE+'filme/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']

				pt = ''
				br = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				cor = "white"
				if 'PT' in i['IMBD']:
					i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if i['visto'] == 1:
					visto = True
				
				else:			
					if Trakt.loggedIn():
						for v in json.loads(vistos[1]):
							if v["movie"]["ids"]["imdb"] is None:
								continue
							if v["movie"]["ids"]["imdb"] == i['IMBD']:
								visto = True
								cor = "blue"
								break
							else:
								visto = False
					else:
						visto = False
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
		
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot':resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
				controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+resultado['background'], trailer=resultado['trailer'])
			elif 'serie' in url or 'anime' in url:
				if 'serie' in url:
					tipo = 'serie'
				elif 'anime' in url:
					tipo = 'anime'
				resultado = controlo.abrir_url(self.API_SITE+tipo+'/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				br = ''
				
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if 'PT' in resultado['IMBD']:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['visto'] == 1:
					visto=True
				else:
					visto=False
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
				controlo.addDir(pt+br+nome+' ('+i['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels, poster=self.SITE+resultado['background'],visto=visto)

		current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'anos', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
	def categorias(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultadoa = json.loads(resultado)
		vistos = Database.selectTraktDB()
		for i in resultadoa["data"]:
			if 'filme' in url:
				resultado = controlo.abrir_url(self.API_SITE+'filme/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
				pt = ''
				br = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				cor = "white"
				if 'PT' in i['IMBD']:
					i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if i['visto'] == 1:
					visto = True
				
				else:			
					if Trakt.loggedIn():
						for v in json.loads(vistos[1]):
							if v["movie"]["ids"]["imdb"] is None:
								continue
							if v["movie"]["ids"]["imdb"] == i['IMBD']:
								visto = True
								cor = "blue"
								break
							else:
								visto = False
					else:
						visto = False
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot':resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
				controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+resultado['background'], trailer=resultado['trailer'])
			elif 'serie' in url or 'anime' in url:
				if 'serie' in url:
					tipo = 'serie'
				elif 'anime' in url:
					tipo = 'anime'
				resultado = controlo.abrir_url(self.API_SITE+tipo+'/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				categoria = resultado['categoria1']
				pt = ''
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				br = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if 'PT' in resultado['IMBD']:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['visto'] == 1:
					visto=True
				else:
					visto = False
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
				controlo.addDir(pt+br+nome+' ('+i['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels, poster=self.SITE+resultado['background'],visto=visto)

		current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'categorias', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))


	def player(self, url):

		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		
		resultado = json.loads(resultado)
		infolabels = dict()

		if 'filme' in url:
			infolabels['Code'] = resultado['IMBD']
			infolabels['Year'] = resultado['ano']
			idVideo = resultado['id_video']
			nome = resultado['nome_ingles']
			temporada = 0
			episodio = 0
		else:
			idVideo = resultado['id_serie']
			nome = resultado['nome_episodio']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
		controlo.mensagemprogresso.create('MrPiracy', u'Abrir emissão','Por favor aguarde...')
		controlo.mensagemprogresso.update(25, "", u'Obter video e legenda', "")
		stream, legenda, ext_g = self.getStreamLegenda(resultado)
		controlo.mensagemprogresso.update(50, "", u'Prepara-te, vai começar!', "")
		playlist = xbmc.PlayList(1)
		playlist.clear()
		iconimage = ''

		listitem = xbmcgui.ListItem(nome, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

		#liz.setInfo( type="Video", infoLabels=infolabels )
		listitem.setInfo(type="Video", infoLabels=infolabels)
		#listitem.setInfo("Video", {"title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		listitem.setPath(path=stream)
		playlist.add(stream, listitem)

		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

		controlo.mensagemprogresso.update(75, "", u'Boa Sessão!!!', "")

		if stream == False:
			controlo.mensagemprogresso.close()
			controlo.alerta('MrPiracy', 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
		else:

			player_mr = Player.Player(url=url, idFilme=idVideo, pastaData=controlo.pastaDados, temporada=temporada, episodio=episodio, nome=nome, logo=os.path.join(controlo.addonFolder,'icon.png'))

			controlo.mensagemprogresso.close()
			player_mr.play(playlist)
			player_mr.setSubtitles(legenda)

			while player_mr.playing:
				xbmc.sleep(5000)
				player_mr.trackerTempo()

	def getStreamLegenda(self, resultado):

		i = 0
		servidores = []
		titulos = []
		nome = ''
		if resultado['URL'] != '':
			i+=1
			servidores.append(resultado['URL'])
			if 'openload' in resultado['URL']:
				nome = "OpenLoad"
			elif 'vidzi' in resultado['URL']:
				nome = 'Vidzi'
			elif 'google' in resultado['URL'] or 'cloud.mail.ru' in resultado['URL']:
				nome = 'MrPiracy'
			elif 'uptostream.com' in resultado['URL']:
				nome = 'UpToStream'
			elif 'rapidvideo.com' in resultado['URL']:
				nome = 'RapidVideo'
			titulos.append('Servidor #%s: %s' % (i, nome))
		if resultado['URL2'] != '':
			i+=1
			servidores.append(resultado['URL2'])
			if 'openload' in resultado['URL2']:
				nome = "OpenLoad"
			elif 'vidzi' in resultado['URL2']:
				nome = 'Vidzi'
			elif 'google' in resultado['URL2'] or 'cloud.mail.ru' in resultado['URL2']:
				nome = 'MrPiracy'
			elif 'uptostream.com' in resultado['URL2']:
				nome = 'UpToStream'
			elif 'rapidvideo.com' in resultado['URL2']:
				nome = 'RapidVideo'
			titulos.append('Servidor #%s: %s' % (i, nome))
		try:
			if resultado['URL3'] != '':
				i+=1
				servidores.append(resultado['URL3'])
				if 'openload' in resultado['URL3']:
					nome = "OpenLoad"
				elif 'vidzi' in resultado['URL3']:
					nome = 'Vidzi'
				elif 'google' in resultado['URL3'] or 'cloud.mail.ru' in resultado['URL3']:
					nome = 'MrPiracy'
				elif 'uptostream.com' in resultado['URL3']:
					nome = 'UpToStream'
				elif 'rapidvideo.com' in resultado['URL3']:
					nome = 'RapidVideo'
				titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass
		try:
			if resultado['URL4'] != '':
				i+=1
				servidores.append(resultado['URL4'])
				if 'openload' in resultado['URL4']:
					nome = "OpenLoad"
				elif 'vidzi' in resultado['URL4']:
					nome = 'Vidzi'
				elif 'google' in resultado['URL4'] or 'cloud.mail.ru' in resultado['URL4']:
					nome = 'MrPiracy'
				elif 'uptostream.com' in resultado['URL4']:
					nome = 'UpToStream'
				elif 'rapidvideo.com' in resultado['URL4']:
					nome = 'RapidVideo'
				titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass
		legenda = ''

		if '://' in resultado['legenda'] or resultado['legenda'] == '':
			legenda = self.API+'subs/%s.srt' % resultado['IMBD']
		elif resultado['legenda'] != '':
			if not '.srt' in resultado['legenda']:
				resultado['legenda'] = resultado['legenda']+'.srt'
			legenda = self.API+'subs/%s' % resultado['legenda']
		try:
			if resultado['semlegenda'] == 1:
				legenda = ''
		except:
			pass
		ext_g = 'coiso'
		if len(titulos) > 1:
			servidor = controlo.select('Escolha o servidor', titulos)
			if 'vidzi' in servidores[servidor]:
				vidzi = URLResolverMedia.Vidzi(servidores[servidor])
				stream = vidzi.getMediaUrl()
				legenda = vidzi.getSubtitle()
			elif 'uptostream.com' in servidores[servidor]:
				stream = URLResolverMedia.UpToStream(servidores[servidor]).getMediaUrl()
			elif 'server.mrpiracy.win' in servidores[servidor]:
				stream = servidores[servidor]
			elif 'openload' in servidores[servidor]:
				stream = URLResolverMedia.OpenLoad(servidores[servidor]).getMediaUrl()
				legenda = URLResolverMedia.OpenLoad(servidores[servidor]).getSubtitle()
			elif 'drive.google.com/' in servidores[servidor]:
				stream, ext_g = URLResolverMedia.GoogleVideo(servidores[servidor]).getMediaUrl()
			elif 'cloud.mail.ru' in servidores[servidor]:
				stream, ext_g = URLResolverMedia.CloudMailRu(servidores[servidor]).getMediaUrl()
			elif 'rapidvideo.com' in servidores[servidor]:
				rapid = URLResolverMedia.RapidVideo(servidores[servidor])
				stream = rapid.getMediaUrl()
				legenda = rapid.getLegenda()
		else:
			if 'vidzi' in servidores[0]:
				vidzi = URLResolverMedia.Vidzi(servidores[0])
				stream = vidzi.getMediaUrl()
				legenda = vidzi.getSubtitle()
			elif 'uptostream.com' in servidores[0]:
				stream = URLResolverMedia.UpToStream(servidores[0]).getMediaUrl()
			elif 'server.mrpiracy.win' in servidores[0]:
				stream = servidores[servidor]
			elif 'openload' in servidores[0]:
				stream = URLResolverMedia.OpenLoad(servidores[0]).getMediaUrl()
				legenda = URLResolverMedia.OpenLoad(servidores[0]).getSubtitle()
			elif 'drive.google.com/' in servidores[0]:
				stream, ext_g = URLResolverMedia.GoogleVideo(servidores[0]).getMediaUrl()
			elif 'cloud.mail.ru' in servidores[0]:
				stream, ext_g = URLResolverMedia.CloudMailRu(servidores[0]).getMediaUrl()
			elif 'rapidvideo.com' in servidores[servidor]:
				rapid = URLResolverMedia.RapidVideo(servidores[servidor])
				stream = rapid.getMediaUrl()
				legenda = rapid.getLegenda()
		

		return stream, legenda, ext_g

	def pesquisa(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		vistos = Database.selectTraktDB()
		if 'filmes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.mrpiracy')

			tipo = 0
		elif 'series' in url:
			ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.mrpiracy')
			tipo = 1
		elif 'animes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.mrpiracy')
			tipo = 2

		if 'page' not in url:
			tipo = controlo.select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes'])
			teclado = controlo.teclado('', 'O que quer pesquisar?')
			
		
			if tipo == 0:
				url = self.API_SITE+'filmes/pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.mrpiracy')
			elif tipo == 1:
				url = self.API_SITE+'series/pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.mrpiracy')
			elif tipo == 2:
				url = self.API_SITE+'animes/pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.mrpiracy')

			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				teclado.setDefault(texto)
			teclado.doModal()

			if teclado.isConfirmed():
				strPesquisa = teclado.getText()
				dados = {'pesquisa': strPesquisa}
				try:
					f = open(ficheiro, mode="w")
					f.write(strPesquisa)
					f.close()
				except:
					traceback.print_exc()
					print "Não gravou o conteudo em %s" % ficheiro

				resultado = controlo.abrir_url(url,post=json.dumps(dados), header=controlo.headers)
		else:
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
			dados = {'pesquisa': texto}
			resultado = controlo.abrir_url(url,post=json.dumps(dados), header=controlo.headers)
		
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		
		resultado = json.loads(resultado)

		if resultado['data'] != '':
			if tipo == 0:
				for i in resultado['data']:
					categoria = i['categoria1']
					if i['categoria2'] != '':
						categoria += ','+i['categoria2']
					if i['categoria3'] != '':
						categoria += ','+i['categoria3']
					infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'IMDBNumber': i['IMBD'] }				
					try:
						nome = i['nome_ingles'].decode('utf-8')
					except:
						nome = i['nome_ingles'].encode('utf-8')
					pt = ''
					br = ''
					if 'Brasileiro' in categoria:
						br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
					if 'Portu' in categoria:
						pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
					cor = "white"
					if 'http' not in i['foto']:
						i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
					if 'PT' in i['IMBD']:
						i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
						pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
					if i['visto'] == 1:
						visto = True
				
					else:			
						if Trakt.loggedIn():
							for v in json.loads(vistos[1]):
								if v["movie"]["ids"]["imdb"] is None:
									continue
								if v["movie"]["ids"]["imdb"] == i['IMBD']:
									visto = True
									cor = "blue"
									break
								else:
									visto = False
						else:
							visto = False
							
					controlo.addVideo('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filme/'+str(i['id_video']), 'player', i['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+i['background'], trailer=i['trailer'])
			elif tipo == 1 or tipo == 2:
				for i in resultado['data']:
					
					categoria = i['categoria1']
					if i['categoria2'] != '':
						categoria += ','+i['categoria2']
					if i['categoria3'] != '':
						categoria += ','+i['categoria3']
					pt = ''
					br = ''
					if 'Brasileiro' in categoria:
						br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
					if 'Portu' in categoria:
						pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
					infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': i['trailer'], 'Director': i['diretor'], 'Rating': i['imdbRating'], 'Code': i['IMBD'] }
					cor = "white"
					if 'PT' in i['IMBD']:
						i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
						pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
					try:
						nome = i['nome_ingles'].decode('utf-8')
					except:
						nome = i['nome_ingles'].encode('utf-8')
					if 'http' not in i['foto']:
						i['foto'] = self.SITE+'images/capas/'+i['foto'].split('/')[-1]
					if tipo == 1:
						link = 'serie'
					elif tipo == 2:
						link = 'anime'
					if i['visto'] == 1:
						visto=True
					else:
						visto=False
					controlo.addDir('[COLOR '+cor+']'+pt+br+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+link+'/'+str(i['id_video']), 'temporadas', i['foto'], tipo='serie', infoLabels=infoLabels,poster=self.SITE+i['background'],visto=visto)

			current = resultado['meta']['pagination']['current_page']
			total = resultado['meta']['pagination']['total_pages']
			try: proximo = resultado['meta']['pagination']['links']['next']
			except: pass 
			if current < total:
				controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'pesquisa', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

	def marcarVisto(self, url):

		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		links = url.split('/')
		
		if 'filme' in url:
			id_video = links[-1]
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['IMBD']
			post = {'id_filme': id_video}
			url = self.API_SITE+'filmes/marcar-visto'
			tipo = 0
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_serie': id_video, 'temporada': temporada, 'episodio':episodio}
			url = self.API_SITE+'series/marcar-visto'
			tipo = 1
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_anime': id_video, 'temporada': temporada, 'episodio':episodio}
			url = self.API_SITE+'animes/marcar-visto'
			tipo = 2


		
		resultado = controlo.abrir_url(url, post=json.dumps(post), header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
	
		resultado = json.loads(resultado)
		if Trakt.loggedIn():
			if tipo == 2 or tipo == 1:
				if '/' in episodio:
					ep = episodio.split('/')
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[1])
				elif 'e' in episodio:
					ep = episodio.split('e')
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[1])
				else:
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, episodio)
			elif tipo == 0:
				Trakt.markwatchedFilmeTrakt(imdb)
			self.getTrakt()
		if resultado['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		if resultado['codigo'] == 201:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		elif resultado['codigo'] == 204:
			controlo.alerta('MrPiracy', 'Ocorreu um erro ao marcar como visto')
	def marcarNaoVisto(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		links = url.split('/')
		
		if 'filme' in url:
			id_video = links[-1]
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['IMBD']
			post = {'id_filme': id_video}
			url = self.API_SITE+'filmes/marcar-visto'
			tipo = 0
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_serie': id_video, 'temporada': temporada, 'episodio':episodio}
			url = self.API_SITE+'series/marcar-visto'
			tipo = 1
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_anime': id_video, 'temporada': temporada, 'episodio':episodio}
			url = self.API_SITE+'animes/marcar-visto'
			tipo = 2


		
		resultado = controlo.abrir_url(url, post=json.dumps(post), header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
	
		resultado = json.loads(resultado)
		if Trakt.loggedIn():

			if tipo == 2 or tipo == 1:
				if '/' in episodio:
					ep = episodio.split('/')
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[1])
				elif 'e' in episodio:
					ep = episodio.split('e')
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[1])
				else:
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, episodio)
			elif tipo == 0:
				Trakt.marknotwatchedFilmeTrakt(imdb)
			self.getTrakt()
		if resultado['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		if resultado['codigo'] == 201:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		elif resultado['codigo'] == 204:
			controlo.alerta('MrPiracy', 'Ocorreu um erro ao marcar como visto')

	def download(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		links = url.split('/')
		
		if 'filme' in url:
			id_video = links[-1]
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['IMBD']
			tipo = 0
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			tipo = 1
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			tipo = 2

		

		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		
		resultado = json.loads(resultado)
		legendasOn = False
		stream, legenda, ext_g = self.getStreamLegenda(resultado)
		
		folder = xbmc.translatePath(controlo.addon.getSetting('pastaDownloads'))
		if legenda != '':
			legendasOn = True
		if tipo > 0:
			if tipo == 1:
				resultadoa = controlo.abrir_url(self.API_SITE+'serie/'+str(id_video), header=controlo.headers)
			elif tipo == 2:
				resultadoa = controlo.abrir_url(self.API_SITE+'anime/'+str(id_video), header=controlo.headers)
			resultadoa = json.loads(resultadoa)
			if not xbmcvfs.exists(os.path.join(folder,'series')):
				xbmcvfs.mkdirs(os.path.join(folder,'series'))
			if not xbmcvfs.exists(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']))):
				xbmcvfs.mkdirs(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles'])))
			if not xbmcvfs.exists(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']),"Temporada "+str(temporada))):
				xbmcvfs.mkdirs(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']),"Temporada "+str(temporada)))
			folder = os.path.join(folder, 'series', self.remove_accents(resultadoa['nome_ingles']), "Temporada "+str(temporada))
			name = "e"+str(episodio)+" - "+self.remove_accents(resultado['nome_episodio'])
		else:
			if not xbmcvfs.exists(os.path.join(folder,'filmes')):
				xbmcvfs.mkdirs(os.path.join(folder,'filmes'))
			folder = os.path.join(folder,'filmes')
			name = self.remove_accents(resultado['nome_ingles'])

	
		streamAux = self.clean(stream.split('/')[-1])
		extensaoStream = self.clean(streamAux.split('.')[-1])

		if '?mim' in extensaoStream:
			extensaoStream = re.compile('(.+?)\?mime=').findall(extensaoStream)[0]


		if ext_g != 'coiso':
			extensaoStream = ext_g

		nomeStream = name+'.'+extensaoStream	

		Downloader.Downloader().download(os.path.join(folder.decode("utf-8"), nomeStream), stream, name)
		
		if legendasOn:
			legendaAux = self.clean(legenda.split('/')[-1])
			extensaoLegenda = self.clean(legendaAux.split('.')[1])
			nomeLegenda = name+'.'+extensaoLegenda
			self.download_legendas(legenda, os.path.join(folder, nomeLegenda))

	def download_legendas(self,url,path):
		contents = controlo.abrir_url(url, header=controlo.headers)
		if contents:
			fh = open(path, 'w')
			fh.write(contents)
			fh.close()
		return
	def clean(self, text):
		command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
		regex = re.compile("|".join(map(re.escape, command.keys())))
		return regex.sub(lambda mo: command[mo.group(0)], text)
	def progressoTrakt(self):

		vistos = Database.selectTraktDB()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')

		for serie in json.loads(vistos[5]):
			url = 'https://api-v2launch.trakt.tv/shows/%s/progress/watched?hidden=false&specials=false' % serie["show"]["ids"]["slug"]
			data = Trakt.getTrakt(url)
			if data == "asd":
				continue
			data = json.loads(data)
		
			try:
				episodioN = str(data["next_episode"]["number"])
				temporadaNumero = str(data["next_episode"]["season"])
			except:
				continue

			if serie["show"]["ids"]["imdb"] is None:
				continue

			
			url = self.API_SITE+'serie/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue

			if resultado['URL'] == '' and resultado['URL2'] == '':
				continue

			infoLabels = {'Title': resultado['nome_episodio'], 'Code': resultado['IMBD'], 'Episode': resultado['episodio'], 'Season': resultado['temporada'] }
			try:
				nome = resultado['nome_episodio'].decode('utf-8')
			except:
				nome = resultado['nome_episodio'].encode('utf-8')
			
			if resultado['imagem'] == 1:
				imagem = self.SITE+'images/capas/'+resultado['IMBD']+'.jpg'
			elif resultado['imagem'] == 0:
				if 'http' not in resultado['fotoSerie']:
					imagem = self.SITE+'images/capas/'+resultado['fotoSerie'].split('/')[-1]
				else:
					imagem = resultado['fotoSerie']
			controlo.addVideo('[B]'+resultado['nomeSerie']+'[/B] '+temporadaNumero+'x'+episodioN+' . '+nome, self.API_SITE+tipo+'/'+str(resultado['id_serie'])+'/temporada/'+str(resultado['temporada'])+'/episodio/'+str(resultado['episodio']), 'player', imagem, False, 'episodio', resultado['temporada'], resultado['episodio'], infoLabels, self.SITE+resultado['background'])

	def watchlistFilmes(self):
		vistos = Database.selectTraktDB()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		for f in json.loads(vistos[3]):
			if f["movie"]["ids"]["imdb"] is None:
				continue
			imdb = f["movie"]["ids"]["imdb"]
			url = self.API_SITE+'filme/%s/imdb' % (imdb)
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			if 'codigo' in resultado:
				continue
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			
			pt = ''
			br = ''
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'

			if 'PT' in resultado['IMBD']:
				resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if resultado['visto'] == 1:
				visto = True
			else:			
				visto = False
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
			
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
			controlo.addVideo(pt+br+nome+' ('+resultado['ano']+')', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.SITE+resultado['background'], trailer=resultado['trailer'])
		 

	def watchlistSeries(self):
		vistos = Database.selectTraktDB()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		for s in json.loads(vistos[4]):
			if s["show"]["ids"]["imdb"] is None:
				continue
			imdb = s["show"]["ids"]["imdb"]
		
			
			url = self.API_SITE+'serie/%s/imdb' % (s["show"]["ids"]["imdb"] )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/imdb' % (s["show"]["ids"]["imdb"] )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue
			

			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']

			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
		
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.SITE+'images/capas/'+resultado['foto'].split('/')[-1]
			if resultado['visto'] == 1:
				visto=True
			else:
				visto=False
			controlo.addDir(nome+' ('+resultado['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels,poster=self.SITE+resultado['background'],visto=visto)
	def remove_accents(self, input_str):
		input_str = input_str.replace("/", "")
		nkfd_form = unicodedata.normalize('NFKD', unicode(self.clean(input_str)))
		return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

	