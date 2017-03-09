from flask import Flask, request, jsonify
from flask import render_template, send_from_directory, make_response

from topic import Topic
from topics import Topics

import math

app = Flask(__name__)
app.url_map.strict_slashes = False


topics=Topics()

# A function to serve basic webpages
@app.route('/')
@app.route('/about')
@app.route('/add')
@app.route('/all/<page>')
@app.route('/topic/<page>')
def basic_pages(**kwargs):
	return make_response(open('templates/index.html').read())

# API end to query the particular topic
@app.route('/api/topics/<int:topic_id>', methods=["GET"])
def get_topic(topic_id):
	topic = topics.getTopic(topic_id)
	result = {}
	if not topic:
		result['status'] = 'error'
		result['message'] = 'topic_id is invalid'
		return jsonify(**result), 400
	else:
		result['topic'] = topic.getTopic()
		result['score'] = topic.getScore()
		result['created_at'] = topic.getCreatedAt()
		result['id'] = topic.getId()
		result['status'] = 'success'
		return jsonify(**result), 200

@app.route('/api/topics', methods=["POST"])
def new_topic():
	data = request.get_json(silent=True)
	if 'topic' in data and len(data['topic']) <= 255:
		topic = Topic(data['topic'])
		topics.addTopic(topic)
		result,status = {'status': 'success', 'id': topic.id}, 200
	elif 'topic' in data:
		result = {'status': 'error', 'message': 'Topics should be less than 255 characters.'}, 400
	else:
		result = {'status': 'error', 'message': 'Field topic not found'}, 400

	return jsonify(**result), status

@app.route('/api/topics/upvote/<int:topic_id>', methods=["GET"])
def upvote(topic_id):
	if topic_id < topics.getNumberOfTopics():
		topic = topics.getTopic(topic_id)
		topic.upvote()
		result,status = {'status': 'success', 'new-score': topic.getScore()}, 200
	else:
		result,status = {'status': 'error', 'message': 'topic not found'}, 400

	topics.refreshTop20(topic)

	return jsonify(**result), status

@app.route('/api/topics/downvote/<int:topic_id>', methods=["GET"])
def downvote(topic_id):
	if topic_id < topics.getNumberOfTopics():
		topic = topics.getTopic(topic_id)
		topic.downvote()
		result,status = {'status': 'success', 'new-score': topic.getScore()}, 200
	else:
		result,status = {'status': 'error', 'message': 'topic not found'}, 400

	topics.refreshTop20(topic)

	return jsonify(**result), status

@app.route('/api/topics/all/<int:page>', methods=["GET"])
@app.route('/api/topics/all/', methods=["GET"])
def get_all_topics(page=0):

	if not topics:
		return jsonify(**{'status': 'success', 'count': 0}), 200

	result = []

	for t in topics.getTopics(page):
		topic = {}
		topic['topic'] = t.getTopic()
		topic['score'] = t.getScore()
		topic['created_at'] = t.getCreatedAt()
		topic['id'] = t.getId()
		result.append(topic)


	return jsonify(**{'status': 'success', 'count': len(result), 'topics': result}), 200

@app.route('/api/topics/pages', methods=["GET"])
def get_pages():
	if topics.getNumberOfTopics() == 0:
		total_pages = 0
	else:
		total_pages = math.ceil(topics.getNumberOfTopics()/20.0)
	return jsonify(**{'status': 'success', 'pages': total_pages}), 200

@app.route('/api/topics/top', methods=["GET"])
def get_top():
	top_topics = topics.getTop20()
	result = []
	for t,upvote in top_topics:
		topic = {}
		topic['topic'] = t.getTopic()
		topic['score'] = t.getScore()
		topic['created_at'] = t.getCreatedAt()
		topic['id'] = t.getId()
		result.append(topic)

	return jsonify(**{'status': 'success', 'topics': result, 'count': len(result)})

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static/img', 'favicon.ico')


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
        app.debug = True
        app.run()