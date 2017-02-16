
people.json:
	curl 'http://scholarslab.org/wp-json/posts?type=people' | python -m json.tool > people.json

