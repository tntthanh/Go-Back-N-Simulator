import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
print("enter window size") 
windowsize = int(input())
print("enter number of frame") 
numberOfFrame= int(input())
ys=[]
yr=[]
yacks=[]
yackr=[]

Tp=2
scale=8
scaleTimeOut=1
Tp=Tp*scale #Scale
Tix=4
Tix=Tix*scale #Scale
Tout=15
Tout=Tout*scale #Scale
plt.grid(True)
ax = plt.gca()
font = 10

plt.text(0, 10, "Sender", fontsize=font, color = "blue")
plt.text(-4, 10, "Buffer", fontsize=font, color = "blue")
plt.text(6, 10, "Receiver", fontsize=font, color = "red")
plt.text(9, 10, "Buffer", fontsize=font, color = "red")


def Type1Arrow(base_coor, head_coor, length, type, file_name, color, buffer, text_visible):
	if text_visible:
		if buffer:
			rect2=patches.Rectangle((5.9,head_coor-Tix),1.8, Tix*1.,linewidth=1,edgecolor='red',facecolor='none')
			plt.text(6.2, head_coor-Tix*0.65, "{}(".format(type)+str(file_name)+")", fontsize=font, color = color)
			ax.add_patch(rect2)
		rect3=patches.Rectangle((0.15,base_coor-Tix),1.8, Tix*1.,linewidth=1,edgecolor='blue',facecolor='none')
		plt.text(0.4, base_coor-Tix*0.65, "{}(".format(type)+str(file_name)+")", fontsize=font, color = color)
		ax.add_patch(rect3)

	if buffer:
		rect1=patches.Rectangle((8.9,head_coor-Tix),1.7, Tix*1.,linewidth=1,edgecolor='red',facecolor='none')
		# Add the patch to the Axes
		ax.add_patch(rect1)
		plt.text(7.7, head_coor-Tix*0.65, "---->", fontsize=font, color = "black")
		plt.text(9.2, head_coor-Tix*0.65, "{}(".format(type)+str(buffer)+")", fontsize=font, color = color)

	if length=="full":
		plt.annotate("", xytext=(2, base_coor), xy=(6, head_coor), arrowprops=dict(arrowstyle="->, head_length = 0.5, head_width = .2", color = color))
	if length=="half":
		plt.annotate("", xytext=(2, base_coor), xy=(6, head_coor), arrowprops=dict(arrowstyle="->, head_length = 0.5, head_width = .2", linestyle="--", color = color))
def Type2Arrow(base_coor, head_coor, length, type, file_name, color, text_visible):
	if text_visible:
		plt.text(2, head_coor, "{}(".format(type)+str(file_name)+")", fontsize=font, color = color)
	if length=="full":
		plt.annotate("", xytext=(6, base_coor), xy=(2, head_coor), arrowprops=dict(arrowstyle="->, head_length = 0.5, head_width = .2", color = color))
	if length=="half":
		plt.annotate("", xytext=(6, base_coor), xy=(2, head_coor), arrowprops=dict(arrowstyle="->, head_length = 0.5, head_width = .2", linestyle="--", color = color))

def SenderBuffer(coor, first, final):
	rect=patches.Rectangle((-5,coor-Tix),3.9, Tix*1.,linewidth=1,edgecolor='blue',facecolor='none')
	plt.text(-1.1, coor-Tix*0.65, "---->", fontsize=font, color = "black")
	plt.text(-4.8, coor-Tix*0.65, "I("+str(final)+") <- I("+str(first)+")", fontsize=font, color = "blue")
	ax.add_patch(rect)

# Init value
# For HDLC:
Tackr=Tp
# For normal:
# Tackr=Tp+Tix
Tacks=Tackr+Tp
Ts=0
Tr=Tp
sent_frame=0
sent_ack=0

while 1:
	i=0
	j=0
	print('Please enter the error frame received: ')
	lastack = int(input()) 
	while lastack>numberOfFrame-1:
		print('Please enter the error frame received: ')
		lastack = int(input())
	
	# Transmit corrected Iframe with ACK
	while i< numberOfFrame: 
		
		if i>lastack:
			break
		if i==0:
			SenderBuffer(-Ts,j,j+(windowsize-1))
		else:
			SenderBuffer(-Ts,j-1,j-1+(windowsize-1))
		print('Frame ' + str(sent_frame) + ' has been transmitted') 		
		Tr=Ts+Tp
		if i>lastack-1:
			if i==(lastack):
				Type1Arrow(-Ts, -Tr, "half", "I", "X", "blue", 0, "");				
			else: 
				Type1Arrow(-Ts, -Tr, "full", "I", sent_frame, "blue", 0, "on");
		else:
			Type1Arrow(-Ts, -Tr, "full", "I", sent_frame, "blue", str(sent_frame), "on");	
		
		if j< lastack: 
			print('RR(' + str(sent_ack+1) + ') has been transmitted') 		
			sent_ack=int(sent_ack)+1			
			Type2Arrow(-(Tackr+Tix), -(Tacks+Tix), "full", "RR", j+1, "red", "on");
			if windowsize==1:
				Tackr=Tackr+2*Tix
				Tacks=Tackr+Tp	
			else:
				Tackr=Tackr+Tix
				Tacks=Tackr+Tp				
			j+=1 
		Type1Arrow(-Ts, -Tr, "", "I", sent_frame, "blue", 0, "on");

		sent_frame=int(sent_frame)+1
		# if sent_frame == windowsize: 
		# 	break
		if windowsize==1:
			Ts=Ts+2*Tix
			Tr=Tr+2*Tix
		else: 
			Ts=Ts+Tix
			Tr=Tr+Tix		
		i+=1 
		lastackNew=lastack
	if lastack>=numberOfFrame-1:
		break
	#LOOP
	while 1:
		Tackr=Tackr+Tix
		Tacks=Tackr+Tp		
		# NAK test
		NAKerror="y"
		n=0
		j=lastackNew
		while NAKerror=="y":
			print('NAK frame error?[y/n]')
			NAKerror = input()
			Tcheck=0		
			if NAKerror=="n":

				while 1:
					if Ts+Tix>=Tacks+1:
						break
					if sent_frame-(lastackNew)+1>windowsize or sent_frame>=numberOfFrame:
						break
					#SenderBuffer(-(Ts),j,j+(windowsize-1))	
					# if sent_frame==lastackNew:
					# 	Type1Arrow(-Ts, -Tr, "half", "I", sent_frame, "blue", 0, "on")
					# else:
					Type1Arrow(-Ts, -Tr, "full", "I", sent_frame, "blue", 0, "on")
					SenderBuffer(-Ts, sent_frame-2, sent_frame-2+(windowsize-1))	

					Ts+=Tix
					Tr+=Tix
					sent_frame+=1
				break
			n+=1
			if windowsize==1 and n==1:
				Tackr=Tackr-2*Tix+Tout
				Tacks=Tackr+Tp
			Type2Arrow(-Tackr, -Tacks,"half", "not receive SREJ", j, "green",0);
			
			#### Send the rest frames in sliding window 
			while 1:
				if Ts>Tackr-Tix+Tp+Tout*n-Tix:
					break
				if sent_frame-(lastackNew)+1>windowsize or sent_frame>=numberOfFrame:
					break
				#SenderBuffer(-(Ts-Tix),j,j+(windowsize-1))	
				Type1Arrow(-Ts, -Tr, "full", "I", sent_frame, "blue", 0, "on")
				SenderBuffer(-(Ts),i+2,i+2+(windowsize-1))	

				if windowsize==1:
					Ts=Ts+2*Tix
					Tr=Tr+2*Tix
				else: 
					Ts=Ts+Tix
					Tr=Tr+Tix
				sent_frame+=1
			#SenderBuffer(-(Ts-Tix),j,j+(windowsize-1))		
				
			Tackr=Tackr+Tout
			Tacks=Tackr+Tp
			####

			scaleTimeOut+=0.2
		Ts-=Tix
		Tr-=Tix
		sent_frame-=1
		
		# NAK sent successfully
		if NAKerror=="n":
			if windowsize==1 and n==0:
				Tackr=Tackr-2*Tix+Tout
				Tacks=Tackr+Tp
			Type2Arrow(-Tackr, -Tacks, "full","SREJ", j, "green","on");
			if n==0:
				if windowsize!=1:
					Type1Arrow(-(Ts), -(Tr), "full", "I", sent_frame, "blue", 0, "on");
			#SenderBuffer(-(Ts),j+1,j+1+(windowsize-1))
		print('Please enter the error frame received: ')
		lastackNew=int(input())
		while lastackNew<lastack:
			print('Please enter the error frame received: ')
			lastacknew = int(input()) 
		
		# Transmit again the error frame
		#################
		Ts=Tacks
		################
		Tackr=Ts+Tp
		Tacks=Tackr+Tp
		i=lastack
		while 1: 
			if i>lastackNew:
				break
			if i>=numberOfFrame:
				break
			print('Frame ' + str(i) + ' has been transmitted')		
			Tr=Ts+Tp
			if i==lastackNew:
				Type1Arrow(-Ts, -Tr, "half", "I", "X", "blue", 0, "")
			else:
				Type1Arrow(-Ts, -Tr, "full", "I", i, "blue", i, "on")
				if i==lastack+1:
					if windowsize==1:
						SenderBuffer(-(Ts),i,i+(windowsize-1))
					else:
						SenderBuffer(-(Ts),i-1,i-1+(windowsize-1))	
				else:
					if windowsize==1:
						SenderBuffer(-(Ts),i,i+(windowsize-1))	
					else:					
						SenderBuffer(-(Ts),i,i+(windowsize-1))	
			if windowsize==1:
				Ts=Ts+2*Tix
				Tr=Tr+2*Tix
			else: 
				Ts=Ts+Tix
				Tr=Tr+Tix		
			i+=1

		# Send ACKs
		yacks=[]
		yackr=[]
		j=lastack
		sent_frame=lastack
		while 1: 
			if j>lastackNew-1:
				break
			if j>=numberOfFrame:
				break
			print('RR(' + str(sent_ack+1) + ') has been transmitted') 		
			sent_ack=int(sent_ack)+1			
			Type2Arrow(-(Tackr+Tix), -(Tacks+Tix), "full", "RR", j+1, "red", "on");	
			if windowsize==1:
				Tackr=Tackr+2*Tix
				Tacks=Tackr+Tp
			else:
				Tackr=Tackr+Tix
				Tacks=Tackr+Tp

			j+=1 
		if windowsize!=1:
			if lastackNew!=numberOfFrame:
				Type1Arrow(-(Ts-Tix), -(Tr-Tix), "half", "I", lastackNew, "blue", 0, "on");
				SenderBuffer(-(Ts-Tix),lastackNew,lastackNew+(windowsize-1))	
		else:
			if windowsize!=1:
				Type1Arrow(-(Ts-2*Tix), -(Tr-2*Tix), "half", "I", lastackNew, "blue", 0, "on");
				SenderBuffer(-(Ts-2*Tix),lastackNew,lastackNew+(windowsize-1))	

		b=Tp/Tix
		# if b>=1:
		# 	Ts=Tacks-(b+1)*Tix
		# else:
		# 	Ts=Tacks
		if windowsize==1:
			Ts=Ts+Tix
			Tr=Tr+Tix
		else: 
			Ts=Ts+Tix
			Tr=Tr+Tix

		Tackr=Tackr+(lastackNew-j)*Tix
		lastack=j
		sent_frame=lastackNew+1
		print('Stop? [y/n] ') 
		stop=input()
		if stop=='y':
			break
	break
	print('Stop? [y/n] ') 
	stop=input()
	if stop=='y':
		break

plt.rcParams["figure.figsize"] = [16,9]
plt.xlim([-6, 12])
plt.ylim([50, -numberOfFrame*1.7*Tix*scaleTimeOut])
plt.gca().invert_yaxis()
plt.axis('off')
plt.show()