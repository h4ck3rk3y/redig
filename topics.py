from collections import Counter


class Topics(object):

	def __init__(self, topics = None):
		if not topics:
			topics = []
		self.topics = topics
		self.top20 = Counter()
		self.least_frequent = None

	def addTopic(self, topic):
		self.top20[topic] = topic.getScore()
		self.topics.append(topic)
		topic.id = self.getNumberOfTopics()-1

	def refreshTop20(self, topic):
		self.top20[topic] = topic.getScore()

	def getNumberOfTopics(self):
		return len(self.topics)

	def getTopics(self, page = 0, pageSize= 20):
		number_of_topics = self.getNumberOfTopics()

		if not page:
			return self.topics

		if (page-1)*pageSize > number_of_topics:
			return []
		else:
			return self.topics[(page-1)*pageSize: min(number_of_topics, (page-1)*pageSize + 20)]

	def getTop20(self):
		return self.top20.most_common(20)

	def getTopic(self, topic_id):
		if topic_id < self.getNumberOfTopics():
			return self.topics[topic_id]
		else:
			return False
