from .. import app
from .. import topics
import pytest
import json
import string
import random

@pytest.fixture
def client(request):
	client = app.app.test_client()
	return client

def topic_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def add_topic(client, topic):
	return client.post('/api/topics', data=json.dumps(dict(topic=topic)), content_type='application/json')

def fetch_topics(client, page):
	return client.get('/api/topics/all/%d'%(page))

def upvote_topic(client, topic_id):
	return client.get('/api/topics/upvote/%d'%(topic_id))

def downvote_topic(client, topic_id):
	return client.get('/api/topics/downvote/%d'%(topic_id))

def fetch_top20(client):
	return client.get('/api/topics/top')

def fetch_topic(client, topic_id):
	return client.get('/api/topics/%d' %(topic_id))

# Tests add topics
def test_add_topic(client):
	rv = add_topic(client, topic_generator())
	assert '"status": "success"' in rv.data
	rv = add_topic(client, topic_generator(256))
	assert '"status": "error"' in rv.data

# Tests fetching of paginated topics
def test_fetch_topics(client):
	app.topics = topics.Topics()

	for i in range(30):
		add_topic(client, topic_generator())

	rv = fetch_topics(client, 1)

	assert '"count": 20' in rv.data

	rv = fetch_topics(client, 2)

	assert '"count": 10' in rv.data

# Tests fetch topic
def test_fetch_topic(client):
	app.topics = topics.Topics()
	topic = topic_generator()
	rv = add_topic(client, topic)
	rv = fetch_topic(client, 0)
	assert topic in rv.data

# Creates a fixed topic, pushes it down in upvotes
# Creates random 30 topics and checks whether topic exists
# in top 20, it shoudlnt. It upvotes the topic madly
# and then rechecks it's existence in top20.
def test_upvote_downvote_fetch_top20(client):
	app.topics = topics.Topics()
	topic = topic_generator()
	rv = add_topic(client, topic)

	rv = upvote_topic(client, 0)

	assert '"new-score": 2' in rv.data

	rv = downvote_topic(client, 0)
	rv = downvote_topic(client, 0)
	rv = downvote_topic(client, 0)

	assert '"new-score": -1' in rv.data

	for i in range(30):
		add_topic(client, topic_generator())

	rv = fetch_top20(client)

	assert topic not in rv.data

	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)
	rv = upvote_topic(client, 0)

	rv = fetch_top20(client)

	assert topic in rv.data
