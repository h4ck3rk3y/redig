from datetime import datetime as dt


class Topic(object):

	"""
		The topics class represents a topic object.

		Attributes

		topic The topic iteslf, a string
		upvotes number of upvotes
		downvotes number of downvotes
		id The id of the topic
		created_at Keeps track of the creation of the topic

	"""

	def __init__(self, topic, upvotes=1, downvotes=0):
		self.topic = topic
		self.upvotes = upvotes
		self.downvotes = downvotes
		self.id = None
		self.created_at = dt.now()

	# Simply increases the number of upvotes
	def upvote(self):
		self.upvotes +=1

	# Simply increases the number  of downvotes
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
