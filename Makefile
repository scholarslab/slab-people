
# TODO: paginate
# TODO: the jq query is broken.

people.json:
	curl 'http://scholarslab.org/wp-json/posts?type=people' | python -m json.tool > people.json

people.csv: people.json
	echo "date,name,category,description" > people.csv
	cat people.json | jq -r '.[] | [.date, .title, .terms.people_category[].name|join(","), .content] | @csv' >> people.csv

