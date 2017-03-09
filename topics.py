from collections import Counter


class Topics(object):
	"""The Topics class keeps track of a bunch of topics

	Attributes

	topics A list of topics
	top20 A counter that is useful for finding the top20 topics efficiently

	"""

	def __init__(self, topics = None):
		if not topics:
			topics = []
		self.topics = topics
		self.top20 = Counter()

	# A simple function to add a topic to the list of topics
	def addTopic(self, topic):
		self.top20[topic] = topic.getScore()
		self.topics.append(topic)
		topic.id = self.getNumberOfTopics()-1

	# Updates top20 whenever a new topic is read
	def refreshTop20(self, topic):
		self.top20[topic] = topic.getScore()

	# A simple function to read the number of topics
	def getNumberOfTopics(self):
		return len(self.topics)

	# A simple function to get topics in a paginated manner.
	def getTopics(self, page = 0, pageSize= 20):
		number_of_topics = self.getNumberOfTopics()

		if not page:
			return self.topics

		if (page-1)*pageSize > number_of_topics:
			return []
		else:
			return self.topics[(page-1)*pageSize: min(number_of_topics, (page-1)*pageSize + 20)]

	# A function that returns top 20 topics
	def getTop20(self):
		return self.top20.most_common(20)

	# A function to fetch a particular topic by ID
	def getTopic(self, topic_id):
		if topic_id < self.getNumberOfTopics():
			return self.topics[topic_id]
		else:
			return False
