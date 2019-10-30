# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import xml.dom
from langdetect import detect

#stage ouvrier pas de spec
#stage fin d'etude a partie filliere

def create_element(doc, tag, attr):
	# 创建一个元素节点
	elementNode = doc.createElement(tag)
	# 创建一个文本节点
	textNode = doc.createTextNode(attr)
	# 将文本节点作为元素节点的子节点
	elementNode.appendChild(textNode)
	return elementNode

def create_node(doc_, corpus_, numero_, titre_, period_, niveau_, branche_, filliere_, description_, entreprise_, adresse_,
                ):
	sujet = doc_.createElement('sujet')
	# sNode.setAttribute('id',str(book['id']))
	numero = create_element(doc_, 'numero', numero_)
	titre = create_element(doc_, 'titre', titre_)
	period = create_element(doc_, 'period', period_)
	niveau = create_element(doc_, 'niveau', niveau_)
	branche = create_element(doc_, 'branche', branche_)
	filliere = create_element(doc_, 'filliere', filliere_)
	description = create_element(doc_, 'description', description_)
	entreprise = create_element(doc_, 'entreprise', entreprise_)
	adresse = create_element(doc_, 'adresse', adresse_)
	# codePostal = create_element(doc_, 'codePostal', codePostal_)
	# ville = create_element(doc_, 'ville', ville_)
	# pays = create_element(doc_, 'pays', pays_)
	sujet.appendChild(numero)
	sujet.appendChild(titre)
	sujet.appendChild(period)
	sujet.appendChild(niveau)
	sujet.appendChild(branche)
	sujet.appendChild(filliere)
	sujet.appendChild(description)
	sujet.appendChild(entreprise)
	sujet.appendChild(adresse)
	# sujet.appendChild(codePostal)
	# sujet.appendChild(ville)
	# sujet.appendChild(pays)
	corpus_.appendChild(sujet)  # 将遍历的节点添加到根节点下




class web_craw:
	def __init__(self):
		self.stage_id = []
		self.stage_numero = []
		self.stage_titre = ''
		self.stage_period = ''
		self.stage_niveau = ''
		self.stage_branche = ''
		self.stage_filliere = ''
		self.stage_description = ''
		self.stage_entreprise = ''
		self.stage_adresse = ''
		self.req_data = []
		self.index_fr = 0
		self.index_en = 0
		self.niveau = ''
		self.debut = '200201'
		self.fin = '201903'
		self.url = 'https://demeter.utc.fr/portal/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show'

	def login(self):

		s = requests.Session()
		login_url = 'https://cas.utc.fr/cas/login'
		while 1:
			username = input('Veuillez saisir votre username:\n')
			mot = input('Veuillez saisir votre password:\n')
			os.system("cls")  # windows
			payload = {
				'execution': '9978c947-de3a-4598-823b-40e35be306b2_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuckFoOGNpalpTK1NzNWZEQXZVK2l1dlJORnVr'
				             'a1dCUUlYbWZxUjlsNU5TdU53WWZrY2FScC95MkkzeDM4VndOUTZNSnBybzMzbjJoa0doUUd2OVQwSmkwMnM4RU1ZRjE1MXZ5YTVyO'
				             'UtIWkdVelFrRVVqSFMvZUtpNmlKSmVqRE9hckgzUUN3SFNmZjFvK21Kbk1OL1ppNDdMRlpDR3RNMWF3MmtkdUVyM1QveHhNNzR1S0'
				             'JSUW55dDd5QUNkejlidDRKVGw0eWo4OGhLRjBDdWd0QlJ4ZTA0OHpvWHRKRDhKbTBWYStxbzhWYml0bmFRVm1EcGZpa0xoVFd6azV'
				             'aSytETHdvdnZqOGJWMlM4dWJ5TDhwZlZ5ajg5N0QyVlFlK3NGSGNxY2JIcWN6RjRsY1N0QittWG1YZUhyZ1hpeTR4R01Cb2MycUtS'
				             'YVU1dS9jaU9vT2tKRXNubzRic2l2WjZwVFE0Q0dhZHU3NFlMV2lscUdQekxDcFpSWDFmUk1CV0FYSDY5ekVkTjNBRUQwUTZDR3FUO'
				             'VJsSmo2YmFwdFZZbU95MjRjRjJsczY2MlBSeXRBK1JmT1daRWYvSmpNaWk2ZGpxWFNXUzBDelpJY2ltYTZDUHV6NmpNeWVWVFlTdk'
				             '0zeitYeEJGZjhEK0ZVVEY1cVpHUFhiRlBkNFVHb3dxZVkydFh3WWZvUmJ6NTVPSjlhd2hXUFF1M1FKbjFPaHUydVF0WkE1aXFhaEQ'
				             '2TEgzTzJPUXNZZlRKN2VkbzlJSFUvRkZtT3hpUjhtMUtTSEpjSTJRc0EzYS9rczJzalQxMnRWbHcvZXo0YUJLRTVkNWNjZkQxR0ZH'
				             'ZjcvVVI5SGRHK0g3ekE2cm55TlQ1amtrSFJWOE9rRkM2OXZVRE5pSkVXQUpPS2ZpbStMZUNKbWQ3ME9DWXFXNlA0dlVick9kQW4vb'
				             'EJlaUZLeFcwSFhYMGtKcmJMTXNobFVSMGFudTRtN2NPZHFmL1pxbTlEcEpDVVhGNlBPeEtLYUhycVVpUzJnRk1Cdm55SzdPNk4xa0'
				             'U2dHhTZUUrSENGYUV3aVNObVlqWERZOVM4QVlFUENwV0FDZ2NrNEdqYkRWaXpqMVdRcDFJYUE2b1ZIcytRRzBpWldQc3pUWmlySzB'
				             'CTWRlenMrQTUySUg5L2ZKdG5QQjBVTGJsekZTa3RtdEZMdy93UWp5NFc4MTRlWDhJOThMVkpZSWNxYTlRQVlzVjdsMXpQdGJHdFpr'
				             'N2hiNERUTlBxczBYVnZ3dmkvK01JY2ZFcWtEYVJWZ1gyNk9iMHVxbGRIY3pLQkpvNmsvdEVSeFloTWEwQ0hENXdaSGVtMktPNVhxa'
				             'WoxTlJJOHpJSUNFRFpQa0VMM2V3TG8vWm5Hd0JlbXNXNjd2QzBkN2gyMlpBeGgxL0NZOXJsdG0ranNLblZpUGxiL2xjODFzdm1nWk'
				             'd6S3RodWpQTWJSQWZ2M1RXakJGRTJWSEE3QlY0eGJHUTdGS0hzL241dlQ5Ri9kU1QyZU8wQWpjTjhCWnBZRXprUFozOEJmVGF5Tnh'
				             'tL3RhQlJrZTJNVmx3QkcrUGxYbG9YazYrenY4S00wTXVhUVd6VEhJemFyYW9QcEdpVEU5S2R2VkF3WjVxenBZM3ltcWVqZHJSZUNX'
				             'NTUzSFFIV0ZidldiOVNSWU5DVEoyaWJFRXJlUnZ2bTNTN3phL2tqOGpSWHA3aCszZmZPNFViNE42MDNqVmNjblk5WTdaRnRpTjJ4d'
				             'k91bWZNd0xvUlI4RS8vR0dEaElIU2c0RGVTenU0Q1Fhck1vM0pvd1VpNTM4cGd5eUt0Smthd1hqNUhKR04wR0l5aUdtREp2eEdLcV'
				             'Vkb3o0ay9DNmZnR1owOXRlVW1FQTUvZlJEWGQvMExJSUx6MkdqeUxCZjkrMWxMekVEeXBKNjZDWXdDb3p5S3JPVEsxeVpxRjhySUx'
				             'GVDFCZ3dQY2Q3QnJJcVd4M1NJSGdoajF3UXRuL3hkaGNwV0l4QytNdjE5NlJwQ2hhMzRLZ2hxeXZRWWJUM2V0L3JYUXlBQkpoaElQ'
				             'ZjNqRi82eWd4Q24zaE9KWlB5UzJUR2lFY1lod0lCMzBLZ3NVNGIzTWpzYUh2MnJ2aGdFMU16dGkxekdXK1ozSFRER0tCbjhDM2NzY'
				             'jVJK3lCeVNTeDFzWlpFTldabnRqTHQ3ZlhGbG9JMk5VWmFrZUxXMmZUVTV1YWRieGVob2ZtSVhQd3BkSFZTY1F6QUlqdlo0SC9weH'
				             'pRb1lLczVYRGNuNWdVMk56enhEUWtMZnJtRkRkdkRiSnI2TU1rS2lFNlFyc3ByL3hqVHI3Q0FWS0dHNHpkeTFQZ1FSaVJ5ZnZHVVY'
				             'yZ3RVOFNqdXROVUpqL3FteFNCa2FRVUVMbXoyd0dERUhnUCtCQ2JMS3Jra1AxNjB2VzNmMGFKTWk2K1c4L0VPNHJVeDZ2YlVIQVhy'
				             'ZzFTQWY0NXM3TXZSNlF6UkR4NmFJby9WZWJDR3pFL1VBNkxjZy80MGNOSHNiWXVOL05STjRLWk9JT1VXU2R5ZmNNWVlQZnZVTDV2N'
				             'Uw5eTIyeG5ydFo3c3ZQdUNwK3h3cUVOd3A0dnI1cm5qMzBYU2lnT1JjRHMzMlFoM2l0THIrV251UGRENjdVVkx5S3BxS1dGOWpkSV'
				             'ZwMkdnMFk1TnFJQ003UGJ5U3hVSS91VnRYRWZhSEdDbFI0dldyMjJTbUxPMU9aTEQ4dENPMWtIMEdZQi9rMGhUQ0tzTU44L0MycHh'
				             'IM0JuRE9zQjkyUjlrK3JJZzByUFJPSEVsRlgzb1NZZGh4elREa0pWcWluMjR5VHNIRnh4SG13aGdWYTBmc3c1TmlFb1JoalhVV1N4'
				             'cW1SbG13UlE4bjJQd3RiWEhob2o0Ymk4SXNZSFRkSXpHN0dTOWFpNXN3RW50REh3Rk84YURCSGw3N0psVmdhNGZvT28xdTkyRVVtM'
				             'zZYUzB6b3hhSytoSFdBaVFKSlJqdm9NT2tUUHdtdVpDL0tMRklXZWF0R0VoN3JiS1pySkZjQnVQSWNyQzNPTmxLeWNyWi95R2l4az'
				             'BYakJkTTdmODdqK1J5NkZVR3FNMFVsc2ZuQ2RqQVZYenJScTZ0a2xNZTNGWEdWa08vU3hIL1V2RmljckJvdzVtM0lxZXVkaWE1SWh'
				             'BVWg2YkhnRCtQbm5JRVZYWC9TRDU0cmpMWTFFNHg3bzY0UjFaTXRZL0pZM2NINHA2QkNWdFVWRlpSTUl0dHJyQWFHTzEwZ2ErbllG'
				             'RThNZUdEc1FDYThIK0NJRCtQS1A5ekp1Q3FVUEs5SnFld3drR3kvV3dWVVJ6a3BreExLV1BYcVd3UmJLQWE5S2trK1RnUVdWMXRTQ'
				             'TdMTzJ6Mkw2RVY4WkZSM21jRmw3NlVWSkhVV05JdGhNOVliRWR2SndEZFhqbUhhRDNJZVR6aXMyb0o4c3p3RTNQNUJQOVFlSHQ2TU'
				             'VjZXozL1dhdkZXanhvQi9PQXJpMXdIb0NrWndhZ0xncFI1TUVWTDQ4QWVYdFFIdVhyVDhneDF3WWdtS3RWeUxacVJXQjllQ0s2ZS9'
				             'Hd3F6WElCbHAzYmFqNlUrZHF4a1Z4cmdzbTg2Yi9lSitZY0JyUVJGVnAzNzU0cVBEdmhwTlNZYUxEWFJxYVVmTDVBMDc2ZTdiN2o5'
				             'MFgzOHBMZ2NDWkhPR0Znei9qVnBsVnhGK2NmdHh3bnBJU1JUQlVZNWo3dXI3S0NSVW9qWm94UHNUTFpxN0x2dXVXb3Q4WXA0T0hZW'
				             'E5Vb1RsZFl6eWYvNjdMN3EvRklKRTZkd216Mk4rYTZaQysva2NId0ZUYzh1OGlSN05WdUpSa2pCNjVOTjBlYXhZbzFiT0w2M0taa0'
				             'xoSkc2RHVqM0lGYzNTUEZKSnNQUGtTMGkvMDlsNFpRb1V6enIvUzRRK2QybmxoaDRzOUQ1ZisxTkVXUUwvb09rOTVhQUtFak1vYUR'
				             'pUXZnT3h0d2h6WmxQeHhJWWo5TmtTT3NTaHJqZVVFampZNHA3QjV2RkVyejMxTnM5anFGMXFpWDFpdnhpQVNPMXIxUDB2djk5eUZM'
				             'UkhxbktFNmNWRmNPT3FrRXVaQ1kyOEo0WGMydnFXVWlyODdINWRLUzQyVG9NTU95U29vcDRockMrbGZkMWxvdjBrUndOSVgvU2xzZ'
				             'kFQSGNNM2ZzTkE4Y000VXZ4T1crOFBhM0tvUU1VdmRTUHN1SEJ4cStZbGUwQUJ6WkRCM1ZMRGsvMldtNXZRVVBrcjA5Rlp1UWtrc2'
				             'NzMVpPM1RwWmZPQk1zT2dKamV4bU5FQ1FVdDVZUUhnbUM0WENGd0JoNGgzYXRURDNSaHpJT1AyY2VTMU8ycXRocUdMODZoblk1VlM'
				             '5NjQyUWNrOWZ2YkJGZnJXUisxYnRCQmZuWHlpTFYyaC9uazZYTXRvZGpRUzBoODhmK2Iydk9xOW9vZ3pGUG5kQmVPdjZBaDBMRC9J'
				             'TkFtL092NnVJMVdvTndISEV4ZmtFdGQxSFkrZDlNMlkxdjVOcTNWY05TVkNUM2xrb2tnWEx0akpMbHNpWjRTWkt3bnliRUxkcmsyd'
				             'nRnNkIwc1Z0d0g1cDcrbHRIaVUzTExXOGRXWEZnUjQ3UldpSVVYWnBVTnhDM3JITE5lZ2hJNHlxbjBzT0F3MVM3c2o1K2dNYkNZYU'
				             'hSNXlvbnFaMWdUbDRTV3pvb0pJbE9jdWpVREJUN1FUUTU5Z2NNOUFFdWh4RkhXSXFSMytMZWhQSTczbVdLK05adEdkOXk3elhpWGt'
				             'QQWNoYUhRaWJGWWdmMjRtTEhXUjgyT3l3d05idlhtc1VtaWpTa2ZHSWd2TGZLV0NGc3d5b25uZU55RklORDVzeDRpUWpZTks1NmxN'
				             'VFBmY1lWR0dVRklNWVhXK2pId2kwaUVMUjB0KzJGZ0J1eSt5SWJSNVFTV1phUjM5Z2IxcTNybUJrdTRJOWtGbnUraUF3NkV5TDVYR'
				             'ERNay9sQ1dRWkdtOTlWaUE9LlhJdkxMT3JqS29fZWJ5bE1wWjJEdUpPZkZqS3c4RVhHSGtsZlhMOGJlTjl3TExwTUoyWFFJS185b2'
				             'txMGhXX3ZXZERQSTkzZjM0UXZaVWF5c3UwZWZR',
				'_eventId': 'submit',
				'username': username,
				'password': mot
				}

			result = s.post(
			    login_url,
			    data=payload
			)
			if result.url == login_url:
				print("Username/Password incorrecte!")
				time.sleep(1)
				os.system("cls")  # windows
			else:
				break
		return s

	def open_page(self,s,index, niveau):
		self.niveau = niveau
		#print('open page!')
		select_headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Content-Length': '701',
			'Content-Type': 'application/x-www-form-urlencoded',
			#'Cookie': 'SSO_ID=v1.2~1~30816FB19D3882BACD053F01F5AADAB1E1D0E95EF5C5579257839DFB70542FB91866E9F1F1F81772A2044A1F8E84E2ED78F3A67F08EFC1CFB880B67E7C62118ECD9FE7621E511C9F30DF22560377F2C5B535601781025F02CCFC6EC9D9501922A34F9CC4AECF241CE2CF413D4DCA65AA3ADD0E85FF05F142AC40676D89C85760BE8618399B68CE423318FFC94ED2290948365930631C8EB11E1B557E99100B50B5D4DAF6AB2CF0B8D8B163445D22A876BD47FF5229F316F7B8792854AC9037E1128D563A16EBCC0ED2827104B02E5B44130A1F599D7806C47AF9A0F598152BBED36288000F93DA99034E7BA86E786C7B; portal30=9.0.3+en-us+us+AMERICA+94807AD6C4ED6E78E053418DA8C0C4EA+BD67D40D6AFE328519A90EA7BEF0589EE0CA24E1AEC3209C78FBA287487CC6A01ABD68311846AE3D44197DC6F77AFFA256F37AD9404D8A471329E119D40273055AF1E77D4F3B0B5298EFE4A17BF386F72EB754992343CED1; OSSO_USER_CTX=v1.0~30B6478536D7A42B86875623BB05A867181EBDADEA976E01C4CB9044FAFD470A2F5143165821D6062CDB14A9C11710128195D25A482E72051BFA8236D46CA412CFB3D3AE12A0C82F263294C904E3F50CE06393AB78CBE7D591CF64CEAC7E6A96568CA50E5AD792BD',
			'Host': 'demeter.utc.fr',
			'Origin': 'https://demeter.utc.fr',
			'Referer': 'https://demeter.utc.fr/portal/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.3'
		}

		req_data_init1 = 'p_arg_names=p_action&p_arg_values=2&p_arg_names=p_niveau_stage&p_arg_values='+self.niveau+'&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values='+self.debut+'&p_arg_names=p_periode_fin&p_arg_values='+self.fin+'&p_arg_names=p_rech_periode&p_arg_values=intervalle&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values=&p_arg_names=p_scroll&p_arg_values=0'
		#req_data_init = 'p_arg_names=p_action&p_arg_values=2&p_arg_names=p_niveau_stage&p_arg_values=ST&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201901&p_arg_names=p_periode_fin&p_arg_values=201901&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values=&p_arg_names=p_scroll&p_arg_values=0'
		#req_data_test = 'p_arg_names=p_action&p_arg_values=2&p_arg_names=p_niveau_stage&p_arg_values=PR&p_arg_names=p_spec&p_arg_values=GI&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201901&p_arg_names=p_periode_fin&p_arg_values=201901&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values=&p_arg_names=p_scroll&p_arg_values=0'
		if index == -1:
			result = s.post(
				self.url,
			    headers=select_headers,
			    data=req_data_init1
				)

		else:
			req_data_chaque = 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values='+self.niveau+'&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values='+self.debut+'&p_arg_names=p_periode_fin&p_arg_values='+self.fin+'&p_arg_names=p_rech_periode&p_arg_values=intervalle&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values='+self.stage_numero[index]+'&p_arg_names=p_scroll&p_arg_values=0'
			#u = 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=PR&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201901&p_arg_names=p_periode_fin&p_arg_values=201901&p_arg_names=p_rech_periode&p_arg_values=semestre  &p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values='+self.stage_numero[index]+'&p_arg_names=p_scroll&p_arg_values=0'			#self.req_data.append('p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values='+niveau+'&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%&p_arg_names=p_mot&p_arg_values=%&p_arg_names=p_periode_debut&p_arg_values='+self.debut+'&p_arg_names=p_periode_fin&p_arg_values='+self.fin+'&p_arg_names=p_rech_periode&p_arg_values=intervalle&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%&p_arg_names=p_dept&p_arg_values=%&p_arg_names=p_domaine&p_arg_values=%&p_arg_names=p_ape&p_arg_values=%&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values='+self.stage_numero[index]+'&p_arg_names=p_scroll&p_arg_values=0')
			result = s.post(
				self.url,
				headers=select_headers,
				data=req_data_chaque#self.req_data[index]
			)

		return result

	def deal_select(self,result):

		soup1 = BeautifulSoup(result.text, features='lxml')

		tags1 = soup1.find_all("tr", onclick=True)

		for tag1 in tags1 :
			self.stage_numero.append(re.sub(r'\D','',tag1['onclick']))
			tag_id = tag1.find(text=re.compile(r'^[A,P][0-9]*$'))
			if tag_id:
				self.stage_id.append(tag_id)

	def parse_onepage(self,result,niveau,doc_fr,corpus_fr,doc_en,corpus_en,numero):
		self.stage_titre = ''
		self.stage_period = ''
		self.stage_niveau = ''
		self.stage_branche = ''
		self.stage_filliere = ''
		self.stage_description = ''
		self.stage_entreprise = ''
		self.stage_adresse = ''
		self.niveau = niveau
		soup2 = BeautifulSoup(result.text, features='lxml')

		##description
		tags2 = soup2.find_all("textarea", class_="lecture_seule marge100")
		if len(tags2) != 0:
			for tag2 in tags2 :
				self.stage_description = tag2.get_text()
		else:
			self.stage_titre = ''
			self.stage_period = ''
			self.stage_niveau = ''
			self.stage_branche = ''
			self.stage_filliere = ''
			self.stage_description = ''
			self.stage_entreprise = ''
			self.stage_adresse = ''
			print("pas de contenu! : ",numero)
			return 0

		##entreprise adresse codePostal ville pays
		tags3 = soup2.find_all("div",{"class": "groupe left"})
		for tag3 in tags3:
			if tag3.span.string == "Partenaire":
				self.stage_entreprise = tag3.h3.string
				self.stage_adresse = tag3.p.text.replace('\n','')
				self.stage_adresse.replace(u'^\n','')


		##titre period niveau branche filliere
		tag5 = soup2.find("div",class_="groupe")

		if tag5.span.string == "Sujet de stage":
			self.stage_titre = tag5.h3.string
			period = tag5.p.find_next("label").string
			self.stage_period = re.sub(r':.*$', '', period, count=0, flags=re.M)
			niveau = tag5.p.find_next("span").string
			self.stage_niveau = re.sub(r'&nbsp', '', niveau, count=0, flags=re.M)
			spec = tag5.p.find_next("span").find_next("span").string
			spec.replace('\n', '').replace('\r', '')
			if spec.find(',')!=-1:
				self.stage_branche = re.sub(r'\n,.+$', '', spec, count=0, flags=re.M).replace('\n', '').replace('\r', '')
				filliere = re.sub(r'^.*\n, ', '', spec, count=0, flags=0)
				self.stage_filliere = re.sub(r'&nbsp', '', filliere, count=0, flags=re.M)
			else:
				self.stage_branche = spec
				self.stage_filliere = ''
		if self.stage_description and self.stage_description != 'Aucune description' and bool(re.search('[a-zA-Z]', self.stage_description)):
			lang = detect(self.stage_description)
			if lang == 'en':
				self.index_en = self.index_en + 1
				create_node(doc_en, corpus_en, str(self.index_en), str(self.stage_titre), str(self.stage_period), str(self.stage_niveau), str(self.stage_branche),
			            str(self.stage_filliere), str(self.stage_description), str(self.stage_entreprise), str(self.stage_adresse))
			else:
				self.index_fr = self.index_fr+1
				create_node(doc_fr, corpus_fr, str(self.index_fr), str(self.stage_titre), str(self.stage_period), str(self.stage_niveau), str(self.stage_branche),
			            str(self.stage_filliere), str(self.stage_description), str(self.stage_entreprise), str(self.stage_adresse))

		self.stage_titre = ''
		self.stage_period = ''
		self.stage_niveau = ''
		self.stage_branche = ''
		self.stage_filliere = ''
		self.stage_description = ''
		self.stage_entreprise = ''
		self.stage_adresse = ''


def main():
	print('begin!')
	xmlfile_fr = open('fr1' + '.xml', 'w',encoding="utf-8")
	dom1_fr = xml.dom.getDOMImplementation()  # 创建文档对象，文档对象用于创建各种节点。
	doc1_fr = dom1_fr.createDocument(None, "corpus", None)
	corpus_fr = doc1_fr.documentElement  # 得到根节点
	xmlfile_en = open('en1' + '.xml', 'w',encoding="utf-8")
	dom1_en = xml.dom.getDOMImplementation()  # 创建文档对象，文档对象用于创建各种节点。
	doc1_en = dom1_en.createDocument(None, "corpus", None)
	corpus_en = doc1_en.documentElement  # 得到根节点
	niveaus = ['PR','ST']
	crawer = web_craw()
	session = crawer.login()
	for ni in niveaus:
		result1 = crawer.open_page(session, -1, ni)
		crawer.deal_select(result1)
		print("length: ", len(crawer.stage_numero))
		crawer.stage_numero = sorted(list(set(crawer.stage_numero)))
		proportion = int(len(crawer.stage_numero) / 6)
		for i in range(0, len(crawer.stage_numero)):
			if i%proportion == 0:
				print(i, " in ", len(crawer.stage_numero), ": ", crawer.stage_numero[i], "niveau: ", ni)

			try:
				result2 = crawer.open_page(session,i,ni)
				crawer.parse_onepage(result2,ni, doc1_fr, corpus_fr,doc1_en, corpus_en,crawer.stage_numero[i])
			except Exception:
				print(crawer.stage_numero[i])
			#time.sleep(0.1)

		crawer.stage_numero = []
	doc1_fr.writexml(xmlfile_fr, addindent=' ' * 4, newl='\n', encoding='utf-8')
	xmlfile_fr.close()
	doc1_en.writexml(xmlfile_en, addindent=' ' * 4, newl='\n', encoding='utf-8')
	xmlfile_en.close()
	print('fini!')

if __name__ == '__main__':
	main()