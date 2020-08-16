import collections
from collections import deque

class TrackableObject:
	def __init__(self, objectID, centroid, buffer):
		# store the object ID, then initialize a list of centroids
		# using the current centroid
		self.objectID = objectID
		self.centroids = [centroid]

		# initialize a deque for trail drawing
		self.deque = deque(maxlen = buffer)