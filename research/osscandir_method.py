import os


path =  "/home/alson-kali/PROGRAMMING"
result = os.scandir(path)

for entry  in result:
	print(f"Entry name s : {entry.name} ")
	print(f"Entry path: {entry.path} ")
	print(f"Is File: {entry.is_file()} ")
	print(f"Is Dir: {entry.is_dir()} ")


result.close()

"""
Entry name s : express_vercel 
Entry path: /home/alson-kali/PROGRAMMING/express_vercel 
Is File: False 
Is Dir: True 
Entry name s : MOOC 
Entry path: /home/alson-kali/PROGRAMMING/MOOC 
Is File: False 
Is Dir: True 
"""