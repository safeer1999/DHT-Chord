import random
import pandas as pd
import numpy as np
from RSA import RSA
import pickle
import os.path
import math

users_df = pd.read_csv("users.csv", index_col=False)
user = "user"
curr_user = ''

class Node :
	def __init__(self,key,address=None):
		self.key = key
		self.address = address
		self.pred = []
		self.next = None
		self.route_table = []
		self.data = []
		

class DataFile:
	def __init__(self,name,content='',pubkey=0,expo=-1):
		self.name=name
		self.content=content
		self.pubkey=pubkey
		self.expo=expo

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

	def search(self,key) :
		temp = self.head

		found = None

		while temp != self.end :
			if temp.key == key :
				found = temp
				break
			temp = temp.next

		if key == self.end.key :
			found = self.end

		return found




		


	def disp_ring(self) :

		temp = self.head
		print(temp.key,temp.pred,list(map(lambda x: x.key, temp.route_table)))

		while(temp.next != self.head):
		  	temp = temp.next
		  	print(temp.key,temp.pred,list(map(lambda x: x.key, temp.route_table)))

	def disp_ring_data(self):
		acc=RSA()
		temp = self.head
		print("------- Node", temp.key,"-------")
		for entry in temp.data:
			print("\t<---->")
			print(">>FILE NAME:\n", entry.name)
			print(">>PUBLIC KEY:\n", entry.pubkey)
			content=entry.content
			if not users_df[users_df['user']==curr_user][entry.name].isna().values[0]:
				print("Decrypting with private key...")
				print(">>CONTENT:\n", acc.decipher_text(content,int(users_df[users_df['user']==curr_user][entry.name].values[0]),entry.pubkey))
			else:
				print("Unable to decrypt without private key.")
				print(">>ENCRYPTED CONTENT:\n", entry.content)
			print("\t<---->\n")

		while(temp.next != self.head):
			temp = temp.next
			print("------- Node", temp.key,"-------")
			for entry in temp.data:
				print("\t<---->")
				print(">>FILE NAME:\n", entry.name)
				print(">>PUBLIC KEY:\n", entry.pubkey)
				content=entry.content
				if not users_df[users_df['user']==curr_user][entry.name].isna().values[0]:
					print("Decrypting with private key...")
					print(">>CONTENT:\n", acc.decipher_text(content,int(users_df[users_df['user']==curr_user][entry.name].values[0]),entry.pubkey))
				else:
					print("Unable to decrypt without private key.")
					print(">>ENCRYPTED CONTENT:\n", entry.content)
				print("\t<---->\n")



		

class Chord :

	def __init__(self,max_nodes=16) :
		self.max_nodes= max_nodes
		self.net_nodes = 0
		self.existing_keys = []


	def init_ring(self,num_nodes = 2):

		
		self.ring_list = List(self.max_nodes)

		for i in range(num_nodes) :
			self.insert_node(self.create_node())

		print("Ring created!\n")

		#self.ring_list.disp_ring()

	def create_node(self):
		key = self.gen_key()
		addr = input('Address of node: ')
		newNode = Node(key,addr)
		return newNode


	def update_pred(self,node):

		if self.ring_list.node_count == 1 :
			self.ring_list.head.pred = [i for i in range(self.max_nodes)]
			return

		succ = node.next

		keys = succ.pred
		succ.pred = []
		data = succ.data
		succ.data = []

		if succ.key < node.key :
			node,succ = succ,node

		while keys != [] :
			key = keys.pop()

			if key > node.key and key <= succ.key :
				succ.pred.append(key)

			else :
				node.pred.append(key)

		while data != [] :
			data_file = data.pop()

			if self.hash_key(data_file.name) > node.key and self.hash_key(data_file.name) <= succ.key :
				succ.data.append(data_file)

			else :
				node.data.append(data_file)



	def update_pred_post_removal(self,node):
		succ=node.next

		while node.pred != []:
			succ.pred.append(node.pred.pop())

		while node.data != []:
			succ.data.append(node.data.pop())




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
		print("inserted with key:",node.key)	

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
			i=0
			while (2**(i+1)) <= key :
				i+=1

			return self.search(node.route_table[i],key)

	def hash_key(self,string):
		return sum(list(map(ord,[i for i in string])))%self.max_nodes


def menu():
	print()
	print("------------------------EDIT MENU-------------------------")
	print("1.Insert a node")
	print("2.Remove a node")
	print("3.Use a node")
	print("4.Exit")
	print("5.Access View Menu")
	print()
	option = int(input("Enter choice: "))
	return option

def registration():
	print("Please enter details\n")
	global curr_user
	curr_user=input("Username: ")
	global users_df
	if curr_user in list(users_df['user']):
		print("Welcome back", curr_user,"\n")
		password=input("Password: ")
		while password != str(users_df[users_df['user']==curr_user]['pass'].values[0]):
			print("Incorrect password, re-enter\n")
			password=input("Password: ")
		else:
			print("Success!\n")
	else:
		print("New user detected, register now")
		password=input("Password: ")
		entry_df=pd.DataFrame({
			'user':[curr_user],
			'pass':[password]
		})
		users_df=pd.concat([users_df,entry_df],sort=True)
		users_df.to_csv("users.csv",index=False)
		print("Registration successful.\n")
	return curr_user
	
def viewer(DHT,dumpfile):
	print()
	DHT.ring_list.disp_ring_data()
	print()
	netUI(DHT,dumpfile)

def netUI(DHT,dumpfile):
	while(True):
		print()
		print("------------------------VIEW MENU------------------------")
		print("1.Edit/Define network")
		print("2.View network")
		print("3.Exit")
		print()
		ch=int(input("Enter choice: "))
		if ch==2:
			viewer(DHT,dumpfile)
		if ch==1:
			editor(DHT,dumpfile)
		else:
			pickle.dump(DHT,dumpfile)
			dumpfile.close()
			exit()
def UI(DHT,loadflag,dumpfile):
	print("\n-----------------------------------------DISTRIBUTED HASH TABLE-CHORD------------------------------------")
	print()
	global user
	user=registration()
	if loadflag:
		netUI(DHT,dumpfile)
	else:
		print("Begin by specifying number of nodes the P2P network should have intitially")
		num_init = int(input('Enter number of nodes: '))

		DHT.init_ring(num_init)
		pickle.dump(DHT,dumpfile)
		editor(DHT,dumpfile)

def editor(DHT,dumpfile):
	while(True) :
		option=menu()

		if option == 1 :
			newNode = DHT.create_node()
			DHT.insert_node(newNode)
			pickle.dump(DHT,dumpfile)

		elif option == 2 :
			key = int(input("Enter node to be removed: "))
			DHT.remove_node(key)
			pickle.dump(DHT,dumpfile)
			print("Node removed!")

		elif option == 3 :
			key = int(input("Enter node to be used: "))
			used_node = DHT.ring_list.search(key)
			if used_node==None:
				print("Node not found!")
				continue
			print("\nOptions:\n1.Search for data\n2.Insert Data\n")
			choice = int(input("Enter choice: "))

			if choice == 1 :
				search_file = input("Enter file name:")
				search_key = DHT.hash_key(search_file)

				node = DHT.search(used_node,search_key)

				for entry in node.data:
					if search_file == entry.name:
						print("Found file in node ",node.address)
						
						print(users_df.loc[users_df['user']==user,entry.name].values[0] == np.nan)
						if math.isnan(users_df.loc[users_df['user']==user,entry.name].values[0] )  :
							print("no access")
							break

						else:
							dec = RSA()
							content_copy = entry.content
							print(users_df.loc[users_df['user']==user,entry.name].values[0])
							print(entry.pubkey)
							content = entry.content
							print(dec.decipher_text(content_copy,int(users_df.loc[users_df['user']==user,entry.name].values[0]),entry.pubkey))
							break

				else :
					print("File not found")

			elif choice == 2 :
				acc_contrl = RSA()
				acc_contrl.generate()

				filename = input("Enter filename: ")
				print("Enter [multiline] content: ")
				lines = []
				while True:
					line = input()
					if line:
						lines.append(line)
					else:
						break
				content = '\n'.join(lines)
				content_copy=content
				ins_key = DHT.hash_key(filename)
				print("File_key",ins_key)
				ins_node = DHT.search(used_node,ins_key)
				
				print("File inserted at node:",ins_node.key)
				
				users_df[filename] = [np.nan for i in range(users_df.shape[0])]
				users_df.loc[users_df['user']==user,filename]=acc_contrl.private_key()
				
				ins_node.data.append(DataFile(filename, acc_contrl.cipher_text(content_copy,acc_contrl.public_key(),acc_contrl.exponent()), acc_contrl.public_key(), acc_contrl.exponent()))
				# pickle.dump(DHT,dumpfile)
				


				#ins_node.data.append(DataFile(filename, acc_contrl.cipher_text(content,acc_contrl.public_key(),acc_contrl.exponent()), acc_contrl.public_key(), acc_contrl.exponent()))
				print("File encrypted with public key", acc_contrl.public_key())
				if len(users_df['user'].values)!=1:
					permch=input("Do you wish to give permission to other users? (y/n): ")
					if permch=='y' or permch=='Y':
						print('Other users:')
						for name in list(users_df['user'].values):
							if name != curr_user:
								print(name)
						select_user=input("Selection: ")
						if select_user in list(users_df['user'].values):
							users_df.loc[users_df['user']==select_user,filename]=acc_contrl.private_key()
						else:
							print("Invalid input")

				users_df.to_csv("users.csv",index=False)
				pickle.dump(DHT,dumpfile)


		elif option==5:
			netUI(DHT,dumpfile)
		else:
			pickle.dump(DHT,dumpfile)	
			dumpfile.close()
			exit()









def main():
	loadflag=False
	if os.path.exists('DHT.obj'):
		print("\nSave file detected.")
		loadfile=open('DHT.obj','rb')
		DHT=pickle.load(loadfile)
		loadfile.close()
		print("Data loaded!")
		loadflag=True
	else:
		print("\nNo existing save file found.")
		DHT = Chord()
		dumpfile=open('DHT.obj','wb')
		pickle.dump(DHT,dumpfile)
		dumpfile.close()
	dumpfile=open('DHT.obj','wb')
	
	UI(DHT,loadflag,dumpfile)
	# DHT.init_ring(3)
	# print()
	# DHT.ring_list.disp_ring()
	# print()

	# print(DHT.ring_list.search(int(input())).key)


if __name__ == '__main__':
	main()







