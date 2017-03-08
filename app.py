from flask import Flask, request, jsonify
from flask import render_template, send_from_directory, make_response
from time import time


app = Flask(__name__)
app.url_map.strict_slashes = False


topics=[]

class Topic(object):

	def __init__(self, topic, upvotes=1, downvotes=0):
		self.topic = topic
		self.upvotes = upvotes
		self.downvotes = downvotes
		self.id = len(topics)
		self.created_at = time.now()

	def upvote(self):
		self.upvotes +=1

	def downvote(self):
		self.downvotes+=1

	def getUpvotes(self):
		return self.upvotes

	def getDownVotes(self):
		return self.downvotes

	def getScore(self):
		return self.upvotes - self.downvotes

	def getId(self):
		return self.id

	def getTopic(self):
		return self.topic

	def getCreatedAt(self):
		return self.created_at

	def __str__(self):
		return "%s created at %s with score %d" %(self.topic, self.created_at, self.score)


# A function to serve basic webpages
@app.route('/')
@app.route('/about')
def basic_pages(**kwargs):
	return make_response(open('templates/index.html').read())

# API end to query the particular topic
@app.route('/api/topics/<topic_id>', methods=["GET"])
def get_topic(topic_id):
	pass

@app.route('/api/topics', methods=["POST"])
def new_topic():
	data = request.get_json(silent=True)
	if 'topic' in data or len(data['topic']) > 255:
		topic = Topic(data['topic'])
		topics.append(topic)
		result,status = {'status': 'success', 'id': topic.id}, 200
	elif 'topic' in data:
		result = {'status': 'error', 'message': 'Topics should be less than 255 characters.'}, 400
	else:
		result = {'status': 'error', 'message': 'Field topic not found'}

	return jsonify(**result), status

@app.route('/api/topics/upvote/<int:topic_id>', methods=["GET"])
def upvote(topic_id):
	if topic_id < len(topics):
		topic = topics[topic_id]
		topic.upvote()
		result,status = {'status': 'success', 'new-score': topic.getScore()}, 200
	else:
		result,status = {'status': 'error', 'message': 'topic not found'}, 400

	return jsonify(**result), status

@app.route('/api/topics/downvote/<int:topic_id>', methods=["GET"])
def upvote(topic_id):
	if topic_id < len(topics):
		topic = topics[topic_id]
		topic.downvote()
		result,status = {'status': 'success', 'new-score': topic.getScore()}, 200
	else:
		result,status = {'status': 'error', 'message': 'topic not found'}, 400

	return jsonify(**result), status

@app.route('/api/topics/all/<int:page>', methods=["GET"]):
@app.route('/api/topics/all/', methods=["GET"]):
def get_all_topics(page=0):

	if not topics:
		return jsonify(**{'status': 'success', 'count': 0}), 200

	result = []
	for topic in topics:
		data = {}
		data['topic'] = topic.getTopic()
		data['score'] = topic.getScore()
		data['created_at'] = topic.getCreatedAt()
		data['id'] = topic.getId()
		result.append(topic)

	return jsonify(**{'status': 'success', 'count': len(result), 'topics': result}), 200

@app.route('/api/topics/pages', methods=["GET"])
def get_pages():
	total_pages = len(topics)/20
	return jsonify(**{'status': 'success', 'pages': total_pages}), 200


@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static/img', 'favicon.ico')


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
        app.debug = True
        app.run()