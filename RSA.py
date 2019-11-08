from decimal import Decimal 
import sympy

class RSA:
	def __init__(self):
		self.exp=0
		self.n=0
		self.d = 0

	def public_key(self):
		return self.n

	def private_key(self) :
		return self.d


	def gcd(self,a,b): 
		if b==0: 
			return a 
		else: 
			return self.gcd(b,a%b) 

	def generate(self) :
		p = sympy.randprime(0,1000)
		q = sympy.randprime(0,1000)
		self.n = p*q
		t = (p-1)*(q-1) 

		e=2
		while(e<t): 
			if self.gcd(e,t)== 1: 
				break
			e+=1

		self.exp = e

		for i in range(1,10): 
			x = 1 + i*t 
			if x % e == 0: 
				self.d = int(x/e) 
				break


	def encrypt(self,no):
		ctt = Decimal(0) 
		ctt =pow(no,self.exp) 
		ct = ctt % self.n
		return ct

	def decrypt(self,enc):
		dtt = Decimal(0) 
		dtt = pow(enc,self.d) 
		dt = dtt % self.n 

		#print('n = '+str(n)+' e = '+str(e)+' t = '+str(t)+' d = '+str(d)+' cipher text = '+str(ct)+' decrypted text = '+str(dt)) 
		return dt

	def cipher_text(self,text) :

		cipher = str("")
		for i in text :
			enc_char =self.encrypt(ord(i))
			cipher += str(enc_char)
			cipher+= ','

		return cipher[:-1]

	def decipher_text(self,text):
		
		text_num = list(map(int,text.split(',')))
		deciphered = str("")

		for i in text_num:
			deciphered+= chr(self.decrypt(i))

		return deciphered


def main():
	no = input('Enter the text = ')

	access = RSA()
	access.generate()
	print("public key:",access.public_key(),"private key:",access.private_key(),"encrypted:",access.cipher_text(no),"decrypted:",access.decipher_text(access.cipher_text(no)))


if __name__ == '__main__':
	main()

