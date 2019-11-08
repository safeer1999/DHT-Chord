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

	def exponent(self):
		return self.exp


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


	def encrypt(self,no,pu_key,exp):
		ctt = Decimal(0) 
		ctt =pow(no,exp) 
		ct = ctt % pu_key
		return ct

	def decrypt(self,enc,pr_key,pu_key):
		dtt = Decimal(0) 
		dtt = pow(enc,pr_key) 
		dt = dtt % pu_key 

		return dt

	def cipher_text(self,text,pu_key,exp) :

		cipher = str("")
		for i in text :
			enc_char =self.encrypt(ord(i),pu_key,exp)
			cipher += str(enc_char)
			cipher+= ','

		return cipher[:-1]

	def decipher_text(self,text,pr_key,pu_key):
		
		text_num = list(map(int,text.split(',')))
		deciphered = str("")

		for i in text_num:
			deciphered+= chr(self.decrypt(i,pr_key,pu_key))

		return deciphered


def main():
	no = input('Enter the text = ')

	access = RSA()
	access.generate()
	print("public key:",access.public_key(),"private key:",access.private_key(),"encrypted:",access.cipher_text(no,access.public_key(),access.exponent()),"decrypted:",access.decipher_text(access.cipher_text(no,access.public_key(),access.exponent()),access.private_key(),access.public_key()))


if __name__ == '__main__':
	main()

