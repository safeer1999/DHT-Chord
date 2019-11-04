import random

class Node :
	def __init__(self,key,address=None):
		self.key = key
		self.address = address
		self.pred = []
		self.next = None
		self.route_table = []


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

	def remove(self,key):

		if self.head.key == key :
			popped = self.head
			self.head = self.head.next
			self.end.next = self.head
			return popped

		temp = self.head


		while temp.next.key != key :
			temp = temp.next

		popped = temp.next
		temp.next = temp.next.next
		return popped




		


	def disp_ring(self) :

		temp = self.head
		print(temp.key,temp.pred,list(map(lambda x: x.key, temp.route_table)))

		while(temp.next != self.head):
		  	temp = temp.next
		  	print(temp.key,temp.pred,list(map(lambda x: x.key, temp.route_table)))




		

class Chord :

	def __init__(self,max_nodes=16) :
		self.max_nodes= max_nodes
		self.net_nodes = 0
		self.existing_keys = []


	def init_ring(self,num_nodes = 2):
		
		self.ring_list = List(self.max_nodes)

		for i in range(num_nodes) :
			key = self.gen_key()
			newNode = Node(key)

			self.insert_node(newNode)

		print("Ring created!!!\n")

		#self.ring_list.disp_ring()

	def update_pred(self,node):

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

	def update_pred_post_removal(self,node):
		succ=node.next

		while node.pred != []:
			succ.pred.append(node.pred.pop())




	def gen_key(self):
		key = int(random.random()*16)
		while key in self.existing_keys:
			key = int(random.random()*self.max_nodes)

		self.existing_keys.append(key)

		return key

	def insert_node(self,node) :

		self.ring_list.insert(node)
		self.update_pred(node)
		self.build_route()
		self.net_nodes+=1
		#print("insert",node.key,self.net_nodes)	

	def remove_node(self,key) :
		popped=self.ring_list.remove(key)
		self.update_pred_post_removal(popped)
		self.build_route()	
		return popped

	def build_route(self) :

		temp = self.ring_list.head
		temp.route_table = []
		temp.route_table.append(self.find_route(temp,(temp.key+1)%self.max_nodes))
		temp.route_table.append(self.find_route(temp,(temp.key+2)%self.max_nodes))
		temp.route_table.append(self.find_route(temp,(temp.key+4)%self.max_nodes))
		temp.route_table.append(self.find_route(temp,(temp.key+8)%self.max_nodes))

		while temp.next != self.ring_list.head :
			temp = temp.next	
			temp.route_table = []
			temp.route_table.append(self.find_route(temp,(temp.key+1)%self.max_nodes))
			temp.route_table.append(self.find_route(temp,(temp.key+2)%self.max_nodes))
			temp.route_table.append(self.find_route(temp,(temp.key+4)%self.max_nodes))
			temp.route_table.append(self.find_route(temp,(temp.key+8)%self.max_nodes))

	def find_route(self,node,key):
		temp = node
		if key in temp.pred :
			return temp
		while temp.next != node :
			temp = temp.next
			if key in temp.pred :
				return temp

	def search(self,node,key):

		if key in node.pred :
			return node

		else :
			return self.search(node.route_table[0],key)





def main():
	DHT = Chord()
	DHT.init_ring(3)
	DHT.insert_node(Node(DHT.gen_key()))
	DHT.ring_list.disp_ring()
	print("\nAfter removal")
	popped=DHT.remove_node(DHT.ring_list.head.next.next.next.key)
	print("popped: ",popped.key)
	DHT.ring_list.disp_ring()
	print("\n")

	rand_key = int(random.random()*16)
	print("searching for ",rand_key)
	loc = DHT.find_route(DHT.ring_list.head,rand_key)
	print("found in node: ",loc.key)



if __name__ == '__main__':
	main()







