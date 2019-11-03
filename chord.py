import random

class Node :
	def __init__(self,key,address=None):
		self.key = key
		self.address = address
		self.pred = []
		self.next = None


class List:
	def __init__(self,max_nodes):
		self.head = None
		self.end = None
		self.max_nodes = max_nodes
		self.node_count=0

	def insert(self,node):
		self.node_count+=1
		if self.head == None :
			self.head = node
			self.head.next = self.head
			self.end = self.head
			return


		if(node.key < self.head.key) :
			node.next = self.head
			self.head = node
			self.end.next = self.head
			return

		temp = self.head

		while((temp.next.key < node.key) and (temp.next != self.head)) :
			temp = temp.next

		if temp == self.end :
			self.end = node

		node.next = temp.next
		temp.next = node


	def disp_ring(self) :

		temp = self.head
		print(temp.key,temp.pred)

		while(temp.next != self.head):
		 	temp = temp.next
		 	print(temp.key,temp.pred)




		

class Chord :

	def __init__(self,max_nodes=16) :
		self.max_nodes= max_nodes
		self.net_nodes = 0
		self.existing_keys = []


	def init_ring(self,num_nodes = 2):
		
		self.net_nodes = num_nodes

		self.ring_list = List(self.max_nodes)

		for i in range(self.net_nodes) :
			key = self.gen_key()
			newNode = Node(key)

			self.ring_list.insert(newNode)
			self.update_pred(newNode)

		print("Ring created!!!\n")

		self.ring_list.disp_ring()

	def update_pred(self,node):
		print("node_count",self.ring_list.node_count)
		if self.ring_list.node_count == 1 :
			self.ring_list.head.pred = [i for i in range(self.max_nodes)]
			return

		succ = node.next

		keys = succ.pred
		succ.pred = []
		if succ.key < node.key :
			node,succ = succ,node

		while keys != [] :
			key = keys.pop()

			if key > node.key and key <= succ.key :
				succ.pred.append(key)

			else :
				node.pred.append(key)




	def gen_key(self):
		key = int(random.random()*16)
		while key in self.existing_keys:
			key = int(random.random()*self.max_nodes)

		self.existing_keys.append(key)

		return key


def main():
	DHT = Chord()
	DHT.init_ring(3)

if __name__ == '__main__':
	main()







