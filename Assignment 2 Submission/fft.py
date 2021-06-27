#Aleksas Murauskas and Jacob McConnell
#ECSE 316 Signals and Networks 
#Fast Fourier Tranform 


#TODO
#Implememnt two types of DFT 
#Understand why one version 
#Extend the FFT algo to a 2 Dimensions 
# Use FFT to denoise an image 
# Use FFT to compress a file 

import sys
import matplotlib
import numpy 
import numpy.fft
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import math
#default input values 
mode =1
image_filename="moonlanding.png";



for x in range(0,len(sys.argv)):
	if sys.argv[x]=="-m":
		mode = int(sys.argv[x+1])
	elif sys.argv[x]=="-i":
		image_filename = sys.argv[x+1]
'''
'''

#[Default] if mode =1 
#For Fast mode, image is converted into FFT and displayed 

# Mode =2
# denoise [truncate high frequencies]

# Mode =3
#Compression and save image 

# Mode =4 
#plot the runtime graphs for the report 
def pad(img_data):
    height = len(img_data)
    width = len(img_data[0])
    if width==height:
        return img_data
    elif width>height:
        x = width-height
        addition= [0.0]*x
        for i in range (0,len(img_data)):
            i= numpy.concatenate((i,addition), axis=0)
            #print (len(i))
        return img_data
    
    else:
        x= height - width
        for i in range (0,x):
            img_data.append([0.0]*width)
        return img_data
def f_filter(ffimg,cut_offl, cut_offh):
    for row in ffimg:
        for element in row:
            x= numpy.real(element)%(2*numpy.pi)
            if x<cut_offh*numpy.pi and x>cut_offl*numpy.pi:
                element= 0j
    return ffimg
            
    
            
def mode2(name):
    img =cv2.imread(image_filename,0)
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(img,cmap='gray')
    axs[0].set_title('original')
    img=pad_for_two(img)
   
    
    ff=two_ddft(img)
    ff= f_filter(ff,0.5,1.5)
    
    result = i2ddft(ff)
    
    axs[1].imshow(numpy.real(result), cmap='gray')
    axs[0].set_title('result')
    plt.show()
    
    
    
    
            
def mode1(name):
    img =cv2.imread(image_filename,0)
  
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(img,cmap='gray')
    axs[0].set_title('original')
    
    img=pad_for_two(img)
    ff= numpy.log(two_ddft(img))
    axs[1].imshow(numpy.real(ff), norm = matplotlib.colors.LogNorm())
    axs[0].set_title('ft')
    plt.show()
    


    
def next_power2(number):
    return 2**math.ceil(numpy.log2(number))
def pad_for_two(img):
    #makes sure both sides are powers of twos f
    height= len(img)
    width = len(img[0])
    new_height =next_power2(height)
    new_width= next_power2(width)
    new_array =numpy.empty(shape=(new_height, new_width))
    new_array.fill(0)
    new_height= len(new_array)
    new_width= len(new_array[0])
    #print("width"+str(width))
    #print("height"+str(height))
    #print("new_width"+str(new_width))
    #print("new_height"+str(new_height))
    for y in range (0,height):
        for x in range (0,width):
            new_array[y][x]=img[y][x]
    return new_array

def dftELEMENT(data, element_num):
    N=len(data)
    sum=0.0
    for n in range (0, len(data)):
        sum= sum+ data[n]*numpy.exp(-2j*numpy.pi/N*element_num*n)
    return sum
def dftSLOW(data):
    new_array= numpy.copy(data)
    new_array = new_array.astype(numpy.complex128, copy=False)
    for k in range (0, len(data)):
        new_array[k] =dftELEMENT(data,k)
    return new_array

            
def jacobfft(x):
    N= len(x)
    if N==1:
        #return idftSLOW(x)
        return numpy.array([numpy.complex(x[0])])
    else:
        even =numpy.array(x[0:N:2])
        odd = numpy.array(x[1:N:2])
        result_even= jacobfft(even)
        result_odd= jacobfft(odd)
        result =numpy.array([0j]*N)
        for k in range (0,N//2):
            t= numpy.exp(-2j*numpy.pi*k/N)*result_odd[k]
            result[k]= result_even[k]+t
            result[k+N//2]=result_even[k]-t
        return result



def ifftCON(X):
    N=len(X)
    return (1/N)*numpy.conj(jacobfft(numpy.conj(X)))
    
def idft(x):
    return ifftCON(x)
          
 
def dft(data):
    #return numpy.fft.fft(data)
    return jacobfft(data)
        
def two_ddft(img_data):
    #dft the rows
    img_data= pad_for_two(img_data)
    changed_rows= list(map(lambda x: dft(x),img_data))
    return numpy.transpose(list(map(lambda x: dft(x),numpy.transpose(changed_rows))))

def i2ddft(img_data):
    #img_data= pad_for_two(img_data)
    #print(math.log2(len(img_data)))
    #print(math.log2(len(img_data[0])))
   
    changed_rows= list(map(lambda x: idft(x),img_data))
    
    return numpy.transpose(list(map(lambda x: idft(x),numpy.transpose(changed_rows))))
    
    
def SLOW(img_data):
    #dft the rows
    img_data= pad_for_two(img_data)
    changed_rows= list(map(lambda x: dftSLOW(x),img_data))
    return numpy.transpose(list(map(lambda x: dftSLOW(x),numpy.transpose(changed_rows))))
    
    
def read_png(file_name):
	f= open(file_name,'r')
	png_values= f.read().split()
	f.close()
	for x, val in enumerate(png_values): #convert all values into floats 
		png_values[x] = float(png_values)
	return png_values

def write_png(file_name, data_returned):
	f = open(file_name,'w')
	f.write(data_returned)
	f.close()

import time
		
def mode4():
    tests=[0]*(13-5)
    for p in range (5,13):
        twotoP=2**p;
        test=numpy.empty((twotoP),(twotoP))
        test.fill(1)
        entry=[p,test]
        tests[p]=entry
    results=[0]*13-5
    for i in range(0,len(tests)):
        entry= tests[i]
        start_time= time.time()
        jacobfft(entry[1])
        end_time =time.time()
        time_fast= end_time-start_time
        start_time=time.time()
        SLOW(entry[1])
        end_time=time.time()
        time_slow= end_time-start_time
        results[i]=[i+5,time_fast,time_slow]
    plt.plot(results)
    
    
if mode==4:
    mode4()
elif mode==2:
    mode2(image_filename)
else:
    mode1(image_filename)


