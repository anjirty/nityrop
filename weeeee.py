X='[!] No valid passwords were found'
W='green'
V=RuntimeError
Q='pdf'
P='rar'
O='clear'
K='cls'
J='nt'
N='zip'
M=exit
L=open
E='red'
D='bold'
B=print
try:import os as F,time as R,string as H,zipfile as S,rarfile as T,itertools as Y,string as H,argparse as Z,pikepdf as U;from termcolor import colored as C;import threading as a;from pathlib import Path as G
except ImportError as A:B('Please install the following modules: {}'.format(A))
def b(min_length,max_length,char_set):
	A=[]
	for B in range(min_length,max_length+1):A.extend(''.join(A)for A in Y.product(char_set,repeat=B))
	return A
def I(file_path,password,file_name,file_type):
	D=file_name;A=password
	with L(file_path,'r')as E:
		F=E.readlines()
		if f"To access {D}, use the password {A}\n"in F:R.sleep(2);B(C(f"To access {D}, use the password {A}\n",'blue'))
		else:
			with L(f"{file_type.upper()}.txt",'a')as E:R.sleep(2);E.write(f"To access {D}, use the password {A}\n");B(C(f"To access {D}, use the password {A}\n",W))
def c(zip_file,passwords):
	H=zip_file
	with S.ZipFile(H)as L:
		for A in passwords:
			try:M=H;P=G(M).stem+'.zip';L.extractall(pwd=A.encode());I('ZIP.txt',A,P,N);return A
			except(S.BadZipFile,V):B(C(f"[-] Incorrect Password: {A}",E,attrs=[D]));F.system(K if F.name==J else O)
	B(C(X,E,attrs=[D]))
def d(rar_file,passwords):
	H=rar_file
	with T.RarFile(H)as M:
		for A in passwords:
			try:N=H;L=G(N).stem+'.rar';M.extractall(pwd=A.encode());B(C(f"[+] Password found: {A}. File: {L}",W,attrs=[D]));I('RAR.txt',A,L,P);return A
			except(T.BadRarFile,V):B(C(f"[-] Incorrect Password: {A}. File: {H}",E,attrs=[D]));F.system(K if F.name==J else O)
	B(C(X,E,attrs=[D]))
def e(pdf_file,passwords):
	H=pdf_file
	for A in passwords:
		try:
			with U.open(H,password=A)as N:L=H;M=G(L).stem+'.pdf';I('PDF.txt',A,M,Q);return A
		except U.PasswordError:B(C(f"[-] Incorrect Password: {A}",E,attrs=[D]));F.system(K if F.name==J else O)
	B(C('[!] No valid passwords were found !!',E,attrs=[D]))
def f(file_type,file_path,passwords):
	G=passwords;F=file_path;A=file_type
	if A==N:return c(F,G)
	elif A==P:return d(F,G)
	elif A==Q:return e(F,G)
	else:B(C(f"[!] Error: Invalid file format. Please try with a ZIP, RAR, or PDF file.",E,attrs=[D]));return
def g():
	K=False;G=Z.ArgumentParser(description='Decrypt ZIP, RAR, or PDF files using a password list or generation');G.add_argument('-t','--type',required=True,choices=[N,P,Q],help='Type of file to decrypt (zip, rar, or pdf)');G.add_argument('-f','--file',required=True,nargs='+',help='Path to the ZIP, RAR, or PDF file(s)');R=G.add_mutually_exclusive_group();R.add_argument('-l','--list',help='Path to a password list file (optional)');R.add_argument('-g','--generate',action='store_true',help='Generate passwords (default: False)');G.add_argument('-min','--min-length',type=int,default=6,required=K,help='Minimum length of passwords to generate');G.add_argument('-max','--max-length',type=int,default=12,required=K,help='Maximum length of passwords to generate');G.add_argument('-c','--char-set',type=str,default=H.ascii_letters+H.digits,required=K,help='Character set to use for password generation');A=G.parse_args()
	for I in A.file:
		if not F.path.isfile(I):B(C(f"[!] Error: File '{I}' not found.",E,attrs=[D]));M(1)
	if not A.list and not A.generate:A.generate=K;A.list=None;A.min_length=4;A.max_length=12;A.char_set=H.ascii_letters+H.digits
	if A.list:
		try:
			with L(A.list)as T:O=[A.strip()for A in T]
		except FileNotFoundError:B(C(f"[!] Error: Password list file '{A.list}' not found.",E,attrs=[D]));M(1)
		B(f"[=] Using passwords from file '{A.list}':")
	elif A.generate:O=b(A.min_length,A.max_length,A.char_set);B(f"[=] Generated {len(O)} passwords:")
	else:B(C(f"[!] Error: Please specify either a password list file or use the generation option.",E,attrs=[D]));M(1)
	S=[]
	for I in A.file:J=a.Thread(target=f,args=(A.type,I,O));S.append(J);J.start()
	for J in S:J.join()
if __name__=='__main__':g()