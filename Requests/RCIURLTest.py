# import required libraries
print("importing libraries")
import requests
from lxml import html

# html request
print("processing get")
payload = {'login': 'rodcolson', 'password': '', 'remember_me': '1'}
url = 'https://members.holidayinnclub.com/hicv/hicv'
# Use 'with' to ensure the session context is closed after use
with requests.Session() as s:
	r = s.post(url, data=payload, headers = dict(referer=url))
	print("get response code: {}".format(r.status_code))
	
	# write html to a file
	print("writing to file")
	fobj = open("01HICLoginResponse.html", "w", encoding=r.encoding)
	fobj.write(r.text)
	fobj.close()

	# jump to RCI
	# first get to RCI jump page
	rciJump = 'https://members.holidayinnclub.com/hicv/pages/rci'
	r = s.get(rciJump, headers = dict(referer = rciJump))
	tree = html.fromstring(r.text)
	clubId = list(set(tree.xpath("//input[@name='clubId']/@value")))[0]
	clubMemberId = list(set(tree.xpath("//input[@name='clubMemberId']/@value")))[0]
	memberBalance = list(set(tree.xpath("//input[@name='memberBalance']/@value")))[0]
	referenceURL = list(set(tree.xpath("//input[@name='referenceURL']/@value")))[0]
	emailAddress = list(set(tree.xpath("//input[@name='emailAddress']/@value")))[0]

	print('clubID: {}'.format(clubId))
	print('clubMemberId: {}'.format(clubMemberId))
	print('memberBalance: {}'.format(memberBalance))
	print('referenceURL: {}'.format(referenceURL))
	print('emailAddress: {}'.format(emailAddress))

	payload = {
	"clubId": clubId, 
	"clubMemberId": clubMemberId, 
	"memberBalance": memberBalance,
	"referenceURL": referenceURL, 
	"emailAddress": emailAddress
	}

	rciUrl = 'https://b2b.rci.com/club'
	r = s.post(rciUrl, data = payload, headers = dict(referer = rciUrl))
	
	# write html to a file
	print("writing to file")
	fobj = open("02RCIJumpResponse.html", "w", encoding=r.encoding)
	fobj.write(r.text)
	fobj.close()

	# next go to RCI home page
	rciHome = 'https://b2b.rci.com/club-home'
	r = s.get(rciHome, headers = dict(referer = rciHome))

	# write html to a file
	print("writing to file")
	fobj = open("03RCIHomeResponse.html", "w", encoding=r.encoding)
	fobj.write(r.text)
	fobj.close()

	# go to resort page
	rciResort = 'https://b2b.rci.com/resort-directory/resortDetails?resortCode=0902'
	r = s.get(rciResort, headers = dict(referer = rciResort))

	# write html to a file
	print("writing to file")
	fobj = open("04RCIResortResponse.html", "w", encoding=r.encoding)
	fobj.write(r.text)
	fobj.close()

	# Search for available units given a resort code
	payload = {
	"resortIdForTA": "0902", 
	"isReviewTabSelectedPtsEx": "", 
	"enableTripAdvFlag": "false"
	}

	rciSearchUrl = 'https://b2b.rci.com/points-search/PointsExchange/available-units'
	r = s.post(rciSearchUrl, data = payload, headers = dict(referer = rciSearchUrl))
	
	# write html to a file
	print("writing to file")
	fobj = open("05RCISearchResponse.html", "w", encoding=r.encoding)
	fobj.write(r.text)
	fobj.close()

	# Should return a page with either:
	#  Sorry, we did not find any results for your search criteria
	# OR
	#  Please select a Check-In and Check-Out date to see available units at this resort.

print("DONE!")
