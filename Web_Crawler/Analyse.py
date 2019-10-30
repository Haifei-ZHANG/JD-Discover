# -*- coding: utf-8 -*-
import requests
from lxml import html
from bs4 import BeautifulSoup
import re
from langdetect import detect
import time
import pandas as pd
import os
stage_titre = ''
stage_period = ''
stage_niveau = ''
stage_branche = ''
stage_filliere = ''
stage_description = ''
stage_entreprise = ''
stage_adresse = ''
stage_codePostal = ''
stage_ville = ''
stage_pays = ''
s = requests.Session()
login_url = 'https://demeter.utc.fr/portal/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show'
login_url2 = 'https://cas.utc.fr/cas/login'
ent_url = 'https://demeter.utc.fr/portal/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 '
	              'Safari/537.36'
}
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
	'username': 'wangyuhu',
	'password': '19971013xmY'
}
s.post(
    login_url2,
    data = payload,
	headers = headers
)
response = s.get(ent_url,headers = headers)
# print(response.status_code)
# print(response.text)

select_headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Content-Length': '701',
			'Content-Type': 'application/x-www-form-urlencoded',
			#'Cookie': '__utma=31043323.485713971.1566187434.1566187434.1566187434.1; __utmz=31043323.1566187434.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SSO_ID=v1.2~1~21C3C3B5140843332648371209D066DF6FAB61B94ECA8A831BC1BD4F34BDF15F93F725F3BFCDCFA3C95627762478EA23F8CA44A27621647CFCCFEF7CD6198CA26F43BBA746BFE59A258BB685343700D4CB8BC6B64C8AC1457E9445F50C5314F21C1304D16C7B97FA4461411E2FD7DD2BCAF6706B1BC64C72497D1B55CC1ECB07D2F7592459D9182226559C4D3150453AA4FEE763A1D849220141953CE7AB89207EF046BBFF4AADD888288B654C5A0E7A2C1C71A0C94C5B41053A44051F77DB171E2A65F6301E01A6B613775D2FD75A6EED8AEAC89E9033BDC1F7BFABFBDE1901D83A107523951EB7; portal30=9.0.3+en-us+us+AMERICA+932A81D45F7657D2E053418DA8C06637+73109994DA4A103C3FE6692E25922BA8F9D6CE7FF116DA0B80B6134C6E5359ACB22CD8CF6916E7BA25FD3226EC65DAEA060286BDA2D38B246A0F3D148988A7567D01783EBB3E2630CFAAD9D9C080E518AD8DF9461D9B8742; OSSO_USER_CTX=v1.0~9DC4EBD4EB338C6BC3B3BC0658484EA6092F84A255DDBFDEA1745B26AE6B2CE61843E0833262F71104875BEA2F1A0B4A4123335E0267F4A6A29E1F2577072B2EBF9230515C8087737E8093A5FF23810033C92AC92FF7945089899D8BB6D56B526FD879267494D7EF',
			'Host': 'demeter.utc.fr',
			'Origin': 'https://demeter.utc.fr',
			'Referer': 'https://demeter.utc.fr/portal/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.3'
		}
req_data_init = 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=PR&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=200201&p_arg_names=p_periode_fin&p_arg_values=201903&p_arg_names=p_rech_periode&p_arg_values=intervalle&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values=7808&p_arg_names=p_scroll&p_arg_values=0'
# 24:  3504
# 25:  2207
# 23:  2893
result = s.post(
	ent_url,
    headers=select_headers,
    data=req_data_init
	)
soup2 = BeautifulSoup(result.text, features='lxml')
##description
print(result.text)
tags2 = soup2.find_all("textarea", class_="lecture_seule marge100")
if len(tags2) != 0:
	for tag2 in tags2 :
		stage_description = tag2.get_text()#.replace('\n','').replace('\r','')
else:
	stage_description = ''
	print("pas de contenu")
print(type(bool(re.search('[a-zA-Z]', stage_description))))
print(re.search('[a-zA-Z]', stage_description))
print(bool(re.search('[a-zA-Z]', stage_description)))
if bool(re.search('[a-zA-Z]', stage_description)):
	lang = detect(stage_description)
	if lang == "fr":
		print(stage_description)
##entreprise adresse codePostal ville pays
tags3 = soup2.find_all("div",{"class": "groupe left"})
for tag3 in tags3:
	if tag3.span.string == "Partenaire":
		# self.stage_entreprise.append(tag3['h3'])
		stage_entreprise = tag3.h3.string
		stage_entreprise.replace(u'\xa0', u'').encode('utf-8')
		stage_adresse = tag3.p.text.replace('\n','')

	##titre period niveau branche filliere
	tag5 = soup2.find("div", class_="groupe")
	# print(result.text)
	if tag5.span.string == "Sujet de stage":
		stage_titre = tag5.h3.string
		period = tag5.p.find_next("label").string
		stage_period = re.sub(r':.*$', '', period, count=0, flags=re.M)
		niveau = tag5.p.find_next("span").string
		stage_niveau = re.sub(r'&nbsp', '', niveau, count=0, flags=re.M)
		spec = tag5.p.find_next("span").find_next("span").string
		spec.replace('\n','').replace('\r','')

		if spec.find(',')!=-1:
			stage_branche = re.sub(r',.+$', '', spec, count=0, flags=re.M).replace('\n', '').replace('\r', '')
			filliere = re.sub(r'^.+\n, ', '', spec, count=0, flags=0)
			stage_filliere = re.sub(r'&nbsp', '', filliere, count=0, flags=re.M)#.replace('\n','').replace('\r','')
			print("file: ",filliere, "br: ",stage_branche)
		else:
			stage_branche = spec
			print(stage_branche)

	# if self.stage_description:
	# 	ind = index + 1
	# 	create_node(doc, corpus, str(ind), stage_titre, stage_period, stage_niveau,
	# 	            stage_branche,
	# 	            stage_filliere, stage_description, stage_entreprise, stage_adresse,
	# 	            stage_codePostal, stage_ville, stage_pays)
	# lang = detect(stage_description)
	# if lang== 'en':
	# 	print('1lang:',lang)
	# else:
	# 	print('1not en :',lang)
# print(stage_titre,'\nperiod:' ,stage_period, '\nniveau:' ,stage_niveau,
#       '\nbr:',stage_branche,
#       '\nfil:',stage_filliere, '\ndesc:' ,stage_description, '\nentre:' ,stage_entreprise, '\nadr:' ,stage_adresse,
#       '\ncod:',stage_codePostal, '\nvill:' ,stage_ville, '\npays:' ,stage_pays)
# print(result.status_code)
print(stage_adresse)
