# load abaqus modules
from abaqusConstants import * 
from abaqus import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *


# load normal modulus 
from eclipse_function import * 
from math import * 
import numpy as np 
import sys 
import timeit
# from search import search
from math import * 
import numpy as np 
import sys 
import os 

# The read out values 
# UR1: +/-: flexion/extension 
# UR2: lateral bending 
# UR3: axial rotation 

def main():
	# E4=float(sys.argv[-1])
	# E3=float(sys.argv[-2])
	# E2=float(sys.argv[-3])
	# E1=float(sys.argv[-4])
	# E0=float(sys.argv[-5])
	E1= 515
	E2= 503
	E3= 455
	E4= 408
	E5= 360
	# factor_parameter=float(sys.argv[-2])
	# EList=[1.0,0.8,0.7,0.6,0.5];
	E_factor=np.array([E1,E2,E3,E4,E5])
	# E_factor=[100*i for i in EList]
	# print 'E_min=%f' %E_min
	# print 'E_max=%f' %E_max
	# xmin=0.8
	# x_max=1.0

	start = timeit.default_timer()
	FiberList=list()
	# print os.getcwd()
	# print '*'*100
	# N1 = 100 #number of divisions /(N1-1) number of lines to be divides

	# N2 = 17 #number of points/line
	N2 = 10
	# N3 = N2*(N1-1)+1 #number of points per layer
	N4 = 6 # number of layers in z direction

	# create fiber list
	# num_Fibers=(N1-1)* N2  #number of fibers
	# for i in range(N1-1):
		# for j in range(N2):
			# FiberList.append(FiberObject(i+1,j+1))

	# create eclipse
	laxis = 25
	saxis = 17.5
	height= 9
	n=1 #control the shape to be eclipse

	# job Control
	job_submit=True
	ifresultPlot=False

	# generate base footprint
	eclipse1 =supereclipse2d(laxis,saxis,n)
	print 'starting generate mesh'
	N1= int(eclipse1.generate()) #N1-1 LINES created
	print N1
	# eclipse1.check()
	# design variable
	# generate base mesh nodes
	# print os.getcwd()
	elemNode=point_along_line(eclipse1.cord,N2,height,N4)

	# np.savetxt('node.out',elemNode)
	

	# generate model
	model=LatticeModel()
	model.gen_Model()

	nodes=model.gen_Node(elemNode,height)
	model.gen_elements(N1,N2,N4,elemNode)
	model.gen_Sets()


	# radius assign
	# Youngs=[E_min, E_max]
	num_fiberlayer=6;
	fiber_radius=0.4; 
	fiber_fe_type ='beam'  # beam or truss 

	model.gen_Section(num_fiberlayer,fiber_radius,E_factor,fiber_fe_type)
	model.gen_BC()

	
	# compress_disp = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
	compress_disp=[1.575]; 
	# reference moment:    RM= [1.0,2.5,5.0,7.5,10.0]
	# flexion_angle = [0.75,3.13,5.02,6.19,7.14];
	flexion_angle=[7.14];
	# extension_angle = [0.66,1.89,3.14,4.10,4.92];
	extension_angle=[4.92];
	# lbend_angle = [1.28,2.81,4.19,5.15,6.12];
	lbend_angle=[6.12]
	# arotation_angle = [0.36,0.98,1.88,2.70,3.45];
	arotation_angle=[3.45]
	# responseCrv_flex=[]; responseCrv_ext=[]; responseCrv_lbend=[];responseCrv_arot=[];

	
	# compression curve calculate
	model.create_compress_step()
	for ii,disp in enumerate(compress_disp):
		stepName='compress'
		print '*' *100
		print 'the current disp= %f' %disp
		model.addDisp(disp)
		model.inputWrite(job_submit,'compress',ii)

	
	# flexion curve calculate
	model.create_flexion_step()
	for ii,angle in enumerate(flexion_angle):
		stepName='flexion'
		angle_radian = angle * pi/180.0
		print '*' *100
		print 'the current angle= %f' %angle_radian
		model.addAngle(stepName,angle_radian)
		model.inputWrite(job_submit,'flexion',ii)

		# result= model.read_Output(stepName,'RM')
		# print 'The reaction moment= %f N.m' %abs(result/1000)
		# print 'point on response curve [%f %f]' %(angle,abs(result/1000))

		# responseCrv_flex.append([angle,abs(result/1000)])
	# np.savetxt('responseCrv_flex.out',responseCrv_flex)

	model.create_extension_step()
	for ii,angle in enumerate(extension_angle):
		stepName='extension'
		angle_radian = angle * pi/180.0
		print '*' *100
		print 'the current angle= %f' %angle_radian
		model.addAngle(stepName,angle_radian)
		model.inputWrite(job_submit,'extension',ii)

		# result= model.read_Output(stepName,'RM')

		# print 'The reaction moment= %f N.m' %abs(result/1000)
		# print 'point on response curve [%f %f]' %(angle,abs(result/1000))

		# responseCrv_ext.append([angle,abs(result/1000)])
	# np.savetxt('responseCrv_extension.out',responseCrv_ext)

	model.create_lbend_step()
	for ii, angle in enumerate(lbend_angle):
		stepName='lbend'
		angle_radian = angle * pi/180.0
		print '*' *100
		print 'the current angle= %f' %angle_radian
		model.addAngle(stepName,angle_radian)
		model.inputWrite(job_submit,'lbend',ii)

		# result= model.read_Output(stepName,'RM')

		# print 'The reaction moment= %f N.m' %abs(result/1000)
		# print 'point on response curve [%f %f]' %(angle,abs(result/1000))

		# responseCrv_lbend.append([angle,abs(result/1000)])
	# np.savetxt('responseCrv_lbend.out',responseCrv_lbend)

	model.create_arotation_step()
	for ii,angle in enumerate(arotation_angle):
		stepName='arotation'
		angle_radian = angle * pi/180.0
		print '*' *100
		print 'the current angle= %f' %angle_radian
		model.addAngle(stepName,angle_radian)
		model.inputWrite(job_submit,'arotation',ii)
		# result= model.read_Output(stepName,'RM')

		# print 'The reaction moment= %f N.m' %abs(result/1000)
		# print 'point on response curve [%f %f]' %(angle,abs(result/1000))

		# responseCrv_arot.append([angle,abs(result/1000)])
	# np.savetxt('responseCrv_arotation.out',responseCrv_arot)

	stop = timeit.default_timer()
	print 'time used for one round'
	print stop - start



class LatticeModel(object):

	def __init__(self):
		import os
		self.nameModel='IVD'
		self.partName='IVD_part'
		self.nameAssembly='assemblyLattice'
		self.nameStep0='Step-1'
		self.setBC=[]
		self.setLC=[]
		self.set_2='set-elem-all'
		self.LC_0='point_load_1'
		self.BC_0='pinned_1'

		self.section_0='section_solid'
		self.material_0='material_steel'
		self.jobName_0='Job_LE'
		self.node=[]

		# store the element labels
		self.wedgeElement =[]
		self.solidElement =[]
		self.barElement =[]
		
		
		# the whole fiber layers
		self.ant=[]
		self.al=[]
		self.lat=[]
		self.pl=[]
		self.post=[]
		
		# last fiber layer: l = last 
		self.lant=[]
		self.lal=[]
		self.llat=[]
		self.lpl=[]
		self.lpost=[]
		self.set1=[]
		self.lastlayer=[]
		
		
		
		# 20 sets of variables
		self.lset1=[]; self.lset2=[]; self.lset3=[];self.lset4=[]; self.lset5=[]; 
		self.lset6=[]; self.lset7=[]; self.lset8=[]; self.lset9=[]; self.lset10=[]; 
		self.lset11=[]; self.lset12=[]; self.lset13=[];self.lset14=[]; self.lset15=[];
		self.lset16=[]; self.lset17=[]; self.lset18=[];self.lset19=[]; self.lset20=[];	
		

		# matrix sets
		self.fiber=[]
		self.afLat=[]
		self.afAnt=[]
		self.afPost=[]

		
		# define fiber layers: 0-9 layers of fibers
		self.fiberPly1=[]; self.fiberPly2=[]; self.fiberPly3=[];
		self.fiberPly4=[]; self.fiberPly5=[]; self.fiberPly6=[];
		self.fiberPly7=[]; self.fiberPly8=[]; self.fiberPly9=[];
		self.fiberPly10=[];

		# define AF, NP region
		self.nucleus=[];
		self.annulus=[];

	def gen_Model(self):
		# del mdb.models['Model-1']
		mdb.Model(self.nameModel);
		self.p= mdb.models[self.nameModel].Part(self.partName); #self.p= the model part

	def gen_Node(self,nodes,height):
		for node in nodes:
			objNode=self.p.Node([node[1],node[2],node[3]]) #generates nodes in abaqus
			if node[3]==0:
				self.setBC.append(node[0]) # node[0] is the label of the nodes: node[3] -> label = 4   (as here we need labels)
			elif node[3]==height:
				self.setLC.append(node[0])
			# append to the whole node
			self.node.append(objNode)

	def gen_elements(self,N1,N2,N4,nodes):
	# the elements are generated based on the nodes generated
	# plus, LC and BC ,some essential node sets need to be generated
	# generate wedge element
	# N1 = 100 #number of divisions /(N1-1) number of lines to be divides
	# N2 = 10  #number of points/line
	# N3 = N2*(N1-1)+1 #number of points per layer
	# N4 = 9  # number of layers in z direction
		# print [N1,N2,N3,N4]
		# *****************************************************************************************************************************
		# generate wedge elements

		# *********************************************
		# variable initialization

		N3 = N2*N1+1
		# ***********************************************************************************************************************************************************
		# wedge element
		for j in range(N1): # for each group of central axis, rotate one circle
			# clear the bar element in each column, after each column the list is initialized
			# bar element in 2 directions
			bar_dir1=[]
			bar_dir2=[]

			for i in range(N4-1): #z direction : checked
				p1 = 1+ i * N3  # [1+0, 1+7*N3] until the last but two layer
				p2 = p1 + 1 + j * N2
				
				# print i
				if j == N1-1:   #the end of loop
					p3 = 2 + i*N3
				else :
					p3 = p2 + N2
				p4 = p1 + N3  # [1+1N3, 1+8*N3] shift p1 by one layer
				p5 = p2 + N3
				p6 = p3 + N3

				# ********************************************************************************************************************
				# generate wedge element
				# return wedge element object
				wedgeEl=self.p.Element([self.node[p1-1],self.node[p2-1],self.node[p3-1],self.node[p4-1],self.node[p5-1],self.node[p6-1]],WEDGE6)
				# print wedgeEl.label
				self.wedgeElement.append(wedgeEl.label);
				self.nucleus.append(wedgeEl.label)

				#*******************************************************************************************************************
				# get node cordinates
				pt1 = np.asarray(nodes[p1-1][1:])
				pt2 = np.asarray(nodes[p2-1][1:])
				pt3 = np.asarray(nodes[p3-1][1:])
				pt4 = np.asarray(nodes[p4-1][1:])
				pt5 = np.asarray(nodes[p5-1][1:])
				pt6 = np.asarray(nodes[p6-1][1:])


		# ***************************************************************************************************************
		# ***************************************************************************************************************
		# generate solid element
		for k in range(N2-1):  # every fiber layer
			# *******************************************************************************************************************
			# variable initialization
			print 'the current k=' 
			print k 
			for j in range(N1):    # loop over one circle

				for i in range(N4-1):        # z direction

					p1 = 2 + i * N3 +j * N2 + k    # p1, p2 is the behind edge, so it will not reach limit first
					p2 = p1 + 1
					if j == N1-1:                  #the end of loop
						p3 = 2 + i * N3 + k + 1
						p4 = p3 - 1
					else :
						p3 = p2 + N2
						p4 = p1 + N2

					# get next layer
					p5 = p1 + N3
					p6 = p2 + N3
					p7 = p3 + N3
					p8 = p4 + N3


					#*******************************************************************************************************************
					# get node cordinates
					pt1 = np.asarray(nodes[p1-1][1:])
					pt2 = np.asarray(nodes[p2-1][1:])
					pt3 = np.asarray(nodes[p3-1][1:])
					pt4 = np.asarray(nodes[p4-1][1:])
					pt5 = np.asarray(nodes[p5-1][1:])
					pt6 = np.asarray(nodes[p6-1][1:])
					pt7 = np.asarray(nodes[p7-1][1:])
					pt8 = np.asarray(nodes[p8-1][1:])

					#*******************************************************************************************************************
					# return solid element objects
					
					
					
					solidElement= self.p.Element([self.node[p1-1],self.node[p2-1],self.node[p3-1],self.node[p4-1],self.node[p5-1],self.node[p6-1],self.node[p7-1],self.node[p8-1]],HEX8)
			

					# append nucleus and annulus parts
					if k<=3: self.nucleus.append(solidElement.label)
					else: self.annulus.append(solidElement.label)
						# if 0<=j<=9 or 47<=j<=63 or 15<=j<=39:
							# self.afLat.append(solidElement.label); 
						# elif 10<=j<=14: 
							# self.afAnt.append(solidElement.label);
						# elif 40<=j<=46: 
							# self.afPost.append(solidElement.label);							

					# Achtung!!!
					# we only add fibers to the outside of the nucleus (40% volumn ratio)
					if (k>=3):
						barElement1=self.p.Element([self.node[p2-1],self.node[p7-1]],LINE2); 
						barElement2=self.p.Element([self.node[p3-1],self.node[p6-1]],LINE2); 
						
						self.barElement.append(barElement1.label); 
						self.barElement.append(barElement2.label); 
						
						
						# if k==4: 
							# self.set1.append(barElement1.label); 
							# self.set1.append(barElement2.label);
						fiber_layer_order = k - 2; 
						
						# create alternative layer of fibers 
						
						# if fiber_layer_order % 2 ==0: 
							# barElement=self.p.Element([self.node[p2-1],self.node[p7-1]],LINE2)
						# else: 
							# barElement=self.p.Element([self.node[p3-1],self.node[p6-1]],LINE2)
						
						if fiber_layer_order==1: self.fiberPly1.append(barElement1.label); self.fiberPly1.append(barElement2.label); 
						elif fiber_layer_order==2: self.fiberPly2.append(barElement1.label); self.fiberPly2.append(barElement2.label); 
						elif fiber_layer_order==3: self.fiberPly3.append(barElement1.label); self.fiberPly3.append(barElement2.label); 
						elif fiber_layer_order==4: self.fiberPly4.append(barElement1.label); self.fiberPly4.append(barElement2.label); 
						elif fiber_layer_order==5: self.fiberPly5.append(barElement1.label); self.fiberPly5.append(barElement2.label); 
						elif fiber_layer_order==6: self.fiberPly6.append(barElement1.label); self.fiberPly6.append(barElement2.label); 
						# elif fiber_layer_order==7: self.fiberPly7.append(barElement.label); 
						# elif fiber_layer_order==8: self.fiberPly8.append(barElement.label); 
						# elif fiber_layer_order==9: self.fiberPly9.append(barElement.label); 
						# elif fiber_layer_order==10: self.fiberPly10.append(barElement.label); 
						
						
						# we have 64 points here 
						
						if 10<=j<=14:
							if barElement1:
								self.ant.append(barElement1.label); 
							if barElement2:
								self.ant.append(barElement2.label);		
							if k ==8:
								self.lant.append(barElement1.label); 
								self.lant.append(barElement2.label);		
		
						elif 6<=j<=9 or 15<=j<=17:
							self.al.append(barElement1.label); self.al.append(barElement2.label);
							if k ==8:
								self.lal.append(barElement1.label); 
								self.lal.append(barElement2.label);		
								
						elif 0<=j<=5 or 57<=j<=63 or 18<=j<=33:
							self.lat.append(barElement1.label); self.lat.append(barElement2.label);
							if k == 8:
								self.llat.append(barElement1.label); 
								self.llat.append(barElement2.label);								
						elif 34<=j<=39 or 47<=j<=52 or 53<=j<=56:
							self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							if k == 8:
								self.lpl.append(barElement1.label); 
								self.lpl.append(barElement2.label);	
						elif 40<=j<=46:
							self.post.append(barElement1.label); self.post.append(barElement2.label);
							if k == 8:
								self.lpost.append(barElement1.label); 
								self.lpost.append(barElement2.label);	


						# if j==12:
							# if barElement1:
								# self.ant.append(barElement1.label); 
							# if barElement2:
								# self.ant.append(barElement2.label);		
							# if k == 8:
								# self.lset1.append(barElement1.label); 
								# self.lset1.append(barElement2.label);		
		
						# elif j==11 or j==13:
							# self.al.append(barElement1.label); self.al.append(barElement2.label);
							# if k ==8:
								# self.lset2.append(barElement1.label); 
								# self.lset2.append(barElement2.label);		
								
						# elif j==10 or j==14:
							# self.lat.append(barElement1.label); self.lat.append(barElement2.label);
							# if k == 8:
								# self.lset3.append(barElement1.label); 
								# self.lset3.append(barElement2.label);								
						
						# elif j==9 or j==15:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset4.append(barElement1.label); 
								# self.lset4.append(barElement2.label);	
						
						# elif j==8 or j==16:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset5.append(barElement1.label); 
								# self.lset5.append(barElement2.label);	
						
						# elif j==7 or j==17:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset6.append(barElement1.label); 
								# self.lset6.append(barElement2.label);													
						
						# elif j==6 or j==18:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset7.append(barElement1.label); 
								# self.lset7.append(barElement2.label);	
								
						# elif j==5 or j==19:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset8.append(barElement1.label); 
								# self.lset8.append(barElement2.label);													
						
						# elif j==4 or j==20:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset9.append(barElement1.label); 
								# self.lset9.append(barElement2.label);							
						
						# elif j==3 or j==21:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset10.append(barElement1.label); 
								# self.lset10.append(barElement2.label);	
						
						# elif j==2 or j==22:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset11.append(barElement1.label); 
								# self.lset11.append(barElement2.label);		
						
						# elif j==1 or j==23:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset12.append(barElement1.label); 
								# self.lset12.append(barElement2.label);		
						
						# elif j==0 or j==24:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset13.append(barElement1.label); 
								# self.lset13.append(barElement2.label);		
						
						# elif j==63 or j==25:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset14.append(barElement1.label); 
								# self.lset14.append(barElement2.label);		

						# elif j==62 or j==26:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset15.append(barElement1.label); 
								# self.lset15.append(barElement2.label);										
						
						# elif j==61 or j==27:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset16.append(barElement1.label); 
								# self.lset16.append(barElement2.label);	

						
						# elif 59<=j<=60 or 28<=j<=29:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset17.append(barElement1.label); 
								# self.lset17.append(barElement2.label);								
						
						# elif 54<=j<=58 or 30<=j<=34:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset18.append(barElement1.label); 
								# self.lset18.append(barElement2.label);	
						
						# elif 48<=j<=53 or 35<=j<=40:
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset19.append(barElement1.label); 
								# self.lset19.append(barElement2.label);			
						
						# else: 
							# self.pl.append(barElement1.label); self.pl.append(barElement2.label);
							# if k == 8:
								# self.lset20.append(barElement1.label); 
								# self.lset20.append(barElement2.label);	



								
		self.lastlayer=self.lset1+self.lset2+self.lset3+ self.lset4+self.lset5;


	def gen_Sets(self):
	# element set
		self.p.SetFromElementLabels(name='nuclues',elementLabels=tuple(self.nucleus))
		self.p.SetFromElementLabels(name='annulus',elementLabels=tuple(self.annulus))
		self.p.SetFromElementLabels(name='afLat',elementLabels=tuple(self.afLat))
		self.p.SetFromElementLabels(name='afAnt',elementLabels=tuple(self.afAnt))
		self.p.SetFromElementLabels(name='afPost',elementLabels=tuple(self.afPost))
		self.p.SetFromElementLabels(name='fiber',elementLabels=tuple(self.barElement))
		self.p.SetFromElementLabels(name='ant',elementLabels=tuple(self.ant))
		self.p.SetFromElementLabels(name='al',elementLabels=tuple(self.al))
		self.p.SetFromElementLabels(name='lat',elementLabels=tuple(self.lat))
		self.p.SetFromElementLabels(name='pl',elementLabels=tuple(self.pl))
		self.p.SetFromElementLabels(name='post',elementLabels=tuple(self.post))
		
		self.p.SetFromElementLabels(name='lant',elementLabels=tuple(self.lant))
		self.p.SetFromElementLabels(name='lal',elementLabels=tuple(self.lal))
		self.p.SetFromElementLabels(name='llat',elementLabels=tuple(self.llat))
		self.p.SetFromElementLabels(name='lpl',elementLabels=tuple(self.lpl))
		self.p.SetFromElementLabels(name='lpost',elementLabels=tuple(self.lpost))
		self.p.SetFromElementLabels(name='set1',elementLabels=tuple(self.set1))	
		
		self.p.SetFromElementLabels(name='fiberPly1',elementLabels=tuple(self.fiberPly1))
		self.p.SetFromElementLabels(name='fiberPly2',elementLabels=tuple(self.fiberPly2))
		self.p.SetFromElementLabels(name='fiberPly3',elementLabels=tuple(self.fiberPly3))
		self.p.SetFromElementLabels(name='fiberPly4',elementLabels=tuple(self.fiberPly4))
		self.p.SetFromElementLabels(name='fiberPly5',elementLabels=tuple(self.fiberPly5))
		self.p.SetFromElementLabels(name='fiberPly6',elementLabels=tuple(self.fiberPly6))
		
		self.p.SetFromElementLabels(name='all_beam_elements',elementLabels=tuple(self.barElement))
		
		# self.p.SetFromElementLabels(name='lset1',elementLabels=tuple(self.lset1))
		# self.p.SetFromElementLabels(name='lset2',elementLabels=tuple(self.lset2))
		# self.p.SetFromElementLabels(name='lset3',elementLabels=tuple(self.lset3))
		# self.p.SetFromElementLabels(name='lset4',elementLabels=tuple(self.lset4))
		# self.p.SetFromElementLabels(name='lset5',elementLabels=tuple(self.lset5))
		# self.p.SetFromElementLabels(name='lset6',elementLabels=tuple(self.lset6))
		# self.p.SetFromElementLabels(name='lset7',elementLabels=tuple(self.lset7))
		# self.p.SetFromElementLabels(name='lset8',elementLabels=tuple(self.lset8))
		# self.p.SetFromElementLabels(name='lset9',elementLabels=tuple(self.lset9))
		# self.p.SetFromElementLabels(name='lset10',elementLabels=tuple(self.lset10))
		# self.p.SetFromElementLabels(name='lset11',elementLabels=tuple(self.lset11))
		# self.p.SetFromElementLabels(name='lset12',elementLabels=tuple(self.lset12))
		# self.p.SetFromElementLabels(name='lset13',elementLabels=tuple(self.lset13))
		# self.p.SetFromElementLabels(name='lset14',elementLabels=tuple(self.lset14))
		# self.p.SetFromElementLabels(name='lset15',elementLabels=tuple(self.lset15))
		# self.p.SetFromElementLabels(name='lset16',elementLabels=tuple(self.lset16))
		# self.p.SetFromElementLabels(name='lset17',elementLabels=tuple(self.lset17))
		# self.p.SetFromElementLabels(name='lset18',elementLabels=tuple(self.lset18))
		# self.p.SetFromElementLabels(name='lset19',elementLabels=tuple(self.lset19))
		# self.p.SetFromElementLabels(name='lset20',elementLabels=tuple(self.lset20))
		
		# self.p.SetFromElementLabels(name='fiberPly7',elementLabels=tuple(self.fiberPly7))
		# self.p.SetFromElementLabels(name='fiberPly8',elementLabels=tuple(self.fiberPly8))
		# self.p.SetFromElementLabels(name='fiberPly9',elementLabels=tuple(self.fiberPly9))
		# self.p.SetFromElementLabels(name='fiberPly10',elementLabels=tuple(self.fiberPly10))

	# node set
		self.p.SetFromNodeLabels(name='BC', nodeLabels=tuple(self.setBC));
		self.p.SetFromNodeLabels(name='LC', nodeLabels=tuple(self.setLC));

	def gen_Section(self,num_fiber_layer,fiber_radius, stiffness_array, fiber_fe_type):
		
		self.m= mdb.models[self.nameModel]
		self.p =self.m.parts[self.partName]
		
		# generate materials 
		model =mdb.models[self.nameModel]
		mat_1 = model.Material(name='nuclues')
		mat_1.Elastic(table=((0.5, 0.48), ))
		
		mat_2 = model.Material(name='annulus')
		mat_2.Elastic(table=((4.2, 0.3), ))
		
		
		for i in range(len(stiffness_array)): 
			mat_name='fiber_'+str(i+1)
			mat=model.Material(name=mat_name)
			mat.Elastic(noCompression=OFF,table=((stiffness_array[i], 0.3), ))

		# mat_2 = model.Material(name='afLat')
		# mat_2.Elastic(table=((0.8, 0.4), ))
		
		# mat_3 = model.Material(name='afAnt')
		# mat_3.Elastic(table=((0.4, 0.4), ))
	
		# mat_3_1 = model.Material(name='afPost')
		# mat_3_1.Elastic(table=((1.0, 0.4), ))
		
		# mat_4=model.Material(name='nuclueshyper')
		# mat_4.Hyperelastic(materialType=ISOTROPIC, testData=OFF, type=MOONEY_RIVLIN,
		# volumetricResponse=VOLUMETRIC_DATA, table=((0.09, 0.12, 0.1905), ))

		# mat_5=model.Material(name='annulushyper')
		# mat_5.Hyperelastic(materialType=ISOTROPIC, testData=OFF, type=MOONEY_RIVLIN,
		# volumetricResponse=VOLUMETRIC_DATA, table=((0.045, 0.56, 0.1653), ))



		# stiffness_array =np.linspace(E[0],E[1],5)

		
		
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# Generate Sections 
		
		# solid 
		model.HomogeneousSolidSection(name='nuclues', material='nuclues', thickness=None)
		model.HomogeneousSolidSection(name='annulus', material='annulus', thickness=None)
		
		# fiber : truss or beam 
		self.m.CircularProfile(name='profile-1', r=fiber_radius)
		
		if fiber_fe_type=='beam':
			for i in range(len(stiffness_array)): 
				mat_fiber='fiber_'+str(i+1)
				self.m.BeamSection(name='beam_section'+str(i+1), integration=DURING_ANALYSIS, poissonRatio=0.0, profile='profile-1', material=mat_fiber, temperatureVar=LINEAR, consistentMassMatrix=False)

		elif fiber_fe_type=='truss':
			for i in range(len(stiffness_array)): 
				mat_fiber='fiber_'+str(i+1)
				self.m.TrussSection(name='truss_section'+str(i+1), material=mat_fiber, area=pi*fiber_radius*fiber_radius)

		# model.HomogeneousSolidSection(name='nucluesHyper', material='nucluesHyper', thickness=None)

		# model.HomogeneousSolidSection(name='afLat', material='afLat', thickness=None)
		# model.HomogeneousSolidSection(name='afAnt', material='afAnt', thickness=None)
		# model.HomogeneousSolidSection(name='afPost', material='afPost', thickness=None)
		# model.TrussSection(name='trussSection', material='annulus fiber', area=3.14e-06)

		
		
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# Assign Sections 
		
		# sectionNameList=['nuclues','afLat','afAnt','afPost']
		sectionNameList=['nuclues','annulus']
		
		for name in sectionNameList: 
			region = self.p.sets[name]
			self.p.SectionAssignment(region=region, sectionName=name, offset=0.0,
									offsetType=MIDDLE_SURFACE, offsetField='',
									thicknessAssignment=FROM_SECTION)
		# assign beam/truss section
		setList =[]
		for i in range(num_fiber_layer): setList.append('fiberPly'+str(i+1))
		
		for i in range(num_fiber_layer):
			setName = setList[i];
			region = self.p.sets[setName]
			
			# section_number = num_fiber_layer/2-(i/2);
			if fiber_fe_type=='beam': 
				temp= (i+2)//2 
				section_name='beam_section'+str(temp)
				self.p.SectionAssignment(region=region, sectionName=section_name, offset=0.0,offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)
				self.p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.25, 0.75, 0.5))
				elemTrussType = ElemType(elemCode=B31, elemLibrary=STANDARD)
				self.p.setElementType(regions=region, elemTypes=(elemTrussType, ))
				self.p.regenerate()
			
			elif fiber_fe_type=='truss':
				temp= (i+2)//2 
				section_name='truss_section'+str(temp)
				self.p.SectionAssignment(region=region, sectionName=section_name, offset=0.0,offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)
				elemTrussType = ElemType(elemCode=T3D2, elemLibrary=STANDARD)
				self.p.setElementType(regions=region, elemTypes=(elemTrussType, ))
				self.p.regenerate()
				

	def gen_BC(self):

		# create assembly instance from part
		a = mdb.models[self.nameModel].rootAssembly
		a.Instance(name=self.nameAssembly, part=self.p, dependent=ON)
		instance_sets = a.instances[self.nameAssembly].sets
		# instance_sets['LC'], instance_sets['BC']

		# define fixed BC
		a = mdb.models['IVD'].rootAssembly
		BC_region = a.instances['assemblyLattice'].sets['BC']
		mdb.models['IVD'].EncastreBC(name='BC-1', createStepName='Initial', region=BC_region, localCsys=None)

		# create RP and couple to Loading surface
		a = mdb.models['IVD'].rootAssembly
		a.ReferencePoint(point=(0.0, 0.0, 9.0))
		a = mdb.models['IVD'].rootAssembly
		r1 = a.referencePoints
		refPoints1=(r1[3], )
		a.Set(referencePoints=refPoints1, name='rp')
		a = mdb.models['IVD'].rootAssembly
		region1=a.sets['rp']
		a = mdb.models['IVD'].rootAssembly
		region2=a.instances['assemblyLattice'].sets['LC']
		mdb.models['IVD'].Coupling(name='Constraint-1', controlPoint=region1,
		surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
		localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

	def create_compress_step(self):
		mdb.models['IVD'].StaticStep(name='compress', previous='Initial',
		stabilizationMethod=NONE, continueDampingFactors=False,
		adaptiveDampingRatio=None, matrixSolver=ITERATIVE,
		matrixStorage=SOLVER_DEFAULT, extrapolation=LINEAR, nlgeom=ON,
		solutionTechnique=FULL_NEWTON)

		regionDef=mdb.models['IVD'].rootAssembly.sets['rp']
		mdb.models['IVD'].FieldOutputRequest(name='compress_output',
		createStepName='compress', variables=('RF', ), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		del mdb.models['IVD'].historyOutputRequests['H-Output-1']

	def addDisp(self,disp):
	   #  add displacement for 2 mm ->> read out RF
		a = mdb.models['IVD'].rootAssembly
		region = a.sets['rp']
		mdb.models['IVD'].DisplacementBC(name='compress', createStepName='compress',
		region=region, u1=0.0, u2=0.0, u3=-disp, ur1=0.0, ur2=0.0,
		ur3=0.0, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
		fieldName='', localCsys=None)

	def create_flexion_step(self):
		del mdb.models['IVD'].steps['compress']
		mdb.models['IVD'].StaticStep(name='flexion', previous='Initial',
		stabilizationMethod=NONE, continueDampingFactors=False,
		adaptiveDampingRatio=None, matrixSolver=ITERATIVE,
		matrixStorage=SOLVER_DEFAULT, extrapolation=LINEAR, nlgeom=ON,
		solutionTechnique=FULL_NEWTON)
		mdb.models['IVD'].steps['flexion'].setValues(maxNumInc=300, initialInc=0.001, maxInc=0.05)

		regionDef=mdb.models['IVD'].rootAssembly.sets['rp']
		mdb.models['IVD'].FieldOutputRequest(name='flexion_output',
		createStepName='flexion', variables=('RM', ), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)
		mdb.models['IVD'].HistoryOutputRequest(name='H-Output-2',
		createStepName='flexion', variables=('UR', 'RM'), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		del mdb.models['IVD'].historyOutputRequests['H-Output-1']

	def create_extension_step(self):
		del mdb.models['IVD'].steps['flexion']
		mdb.models['IVD'].StaticStep(name='extension', previous='Initial', nlgeom=ON)
		mdb.models['IVD'].steps['extension'].setValues(maxNumInc=300, initialInc=0.001, maxInc=0.05)

		regionDef=mdb.models['IVD'].rootAssembly.sets['rp']
		mdb.models['IVD'].FieldOutputRequest(name='extension_output',
		createStepName='extension', variables=('RM', ), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		mdb.models['IVD'].HistoryOutputRequest(name='H-Output-2',
		createStepName='extension', variables=('UR', 'RM'), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		del mdb.models['IVD'].historyOutputRequests['H-Output-1']

	def create_lbend_step(self):
		del mdb.models['IVD'].steps['extension']
		mdb.models['IVD'].StaticStep(name='lbend', previous='Initial', nlgeom=ON)
		mdb.models['IVD'].steps['lbend'].setValues(maxNumInc=300, initialInc=0.001, maxInc=0.05)

		regionDef=mdb.models['IVD'].rootAssembly.sets['rp']
		mdb.models['IVD'].FieldOutputRequest(name='lbend_output',
		createStepName='lbend', variables=('RM', ), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		mdb.models['IVD'].HistoryOutputRequest(name='H-Output-2',
		createStepName='lbend', variables=('UR', 'RM'), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		del mdb.models['IVD'].historyOutputRequests['H-Output-1']

	def create_arotation_step(self):
		del mdb.models['IVD'].steps['lbend']
		mdb.models['IVD'].StaticStep(name='arotation', previous='Initial', nlgeom=ON)
		mdb.models['IVD'].steps['arotation'].setValues(maxNumInc=300, initialInc=0.001, maxInc=0.05)

		regionDef=mdb.models['IVD'].rootAssembly.sets['rp']
		mdb.models['IVD'].FieldOutputRequest(name='arotation_output',
		createStepName='arotation', variables=('RM', ), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		mdb.models['IVD'].HistoryOutputRequest(name='H-Output-2',
		createStepName='arotation', variables=('UR', 'RM'), region=regionDef,
		sectionPoints=DEFAULT, rebar=EXCLUDE)

		del mdb.models['IVD'].historyOutputRequests['H-Output-1']

	def addAngle(self,stepName,angle):
		a = mdb.models['IVD'].rootAssembly
		region = a.sets['rp']

		if stepName=='flexion':
			angle=-angle;
			mdb.models['IVD'].DisplacementBC(name=stepName, createStepName=stepName,
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=angle, ur2=0.0,
			ur3=0.0, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
			fieldName='', localCsys=None)

		elif stepName=='extension':
			mdb.models['IVD'].DisplacementBC(name=stepName, createStepName=stepName,
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=angle, ur2=0.0,
			ur3=0.0, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
			fieldName='', localCsys=None)

		elif stepName=='lbend':
			mdb.models['IVD'].DisplacementBC(name=stepName, createStepName=stepName,
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=angle,
			ur3=0.0, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
			fieldName='', localCsys=None)

		elif stepName=='arotation':
			mdb.models['IVD'].DisplacementBC(name=stepName, createStepName=stepName,
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0,
			ur3=angle, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
			fieldName='', localCsys=None)

	def inputWrite(self,job_submit,loadcase,ii):
		import section
		import regionToolset
		import displayGroupMdbToolset as dgm
		import part
		import material
		import assembly
		import step
		import interaction
		import load
		import mesh
		import optimization
		import job
		import sketch
		import visualization
		import xyPlot
		import displayGroupOdbToolset as dgo
		import connectorBehavior
		import os
		# create initial input file
		job_name='IVD_'+loadcase+'_'+str(ii)
		mdb.Job(name=job_name, model='IVD', description='', type=ANALYSIS, atTime=None,
		waitMinutes=0, waitHours=0, queue=None, memory=90,
		memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
		scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
		numGPUs=0)
		mdb.jobs[job_name].writeInput(consistencyChecking=OFF)


		# revise the input file:
		# print os.getcwd()
		# file_name=job_name+'.inp'
		# line_num=search(file_name);
		# print 'The returned line number is: ', line_num

		# text='*Element, type=T3D2'
		# file = open(file_name,'r')
		# lines = file.readlines()
		# file.close();

		# lines[line_num-1] = text+'\n'
		# file1 = open(file_name,'w');
		# lines = file1.writelines(lines);
		# file1.close();
		# print "inp file has been revised"
		# time.sleep(5)

		# create new job
		# mdb.JobFromInputFile(name='IVDnew',
		# inputFileName='C:\\Users\\yuz\\Desktop\\workfolder\\01\\IVD.inp',
		# type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
		# memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
		# explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE,
		# userSubroutine='', scratch='', resultsFormat=ODB,
		# parallelizationMethodExplicit=DOMAIN, numDomains=1,
		# activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)

		# mdb.jobs['IVDnew'].submit(consistencyChecking=OFF)
		# mdb.jobs['IVDnew'].waitForCompletion();

		# submit the job
		# if job_submit==True:
			# print 'job sumitting'
			# scrip_name = 'submitjob'
			# strCommandLine = 'abaqus noGUI job='+newJob_name+' interactive'
			# os.system(strCommandLine)
			# mdb.jobs['IVDnew'].submit(consistencyChecking=OFF);

	def read_Output(self,stepName,readValue):
		odbname ='IVDnew'
		myOdb = openOdb(path=odbname+'.odb')
		SetName ='RP'
		myassembly=myOdb.rootAssembly
		RP = myassembly.nodeSets[SetName]
		# get reaction force at z direction
		if stepName =='compress': result=myOdb.steps[stepName].frames[-1].fieldOutputs[readValue].getSubset(region=RP).values[0].data[2]
		elif (stepName=='flexion' or stepName=='extension'):
			result=myOdb.steps[stepName].frames[-1].fieldOutputs[readValue].getSubset(region=RP).values[0].data[0]
		elif stepName=='lbend': result=myOdb.steps[stepName].frames[-1].fieldOutputs[readValue].getSubset(region=RP).values[0].data[1]
		elif stepName=='arotation': result=myOdb.steps[stepName].frames[-1].fieldOutputs[readValue].getSubset(region=RP).values[0].data[2]
		myOdb.close()
		return result

class FiberObject(object):
# each fiber lies in certain ith layer, with certain number 
# with certain element labels making one fiber 
	def __init__(self,layerNumber,cont):
		N4 = 9
		self.numLayer= N4-1           #it goes accross 8 layers of fibers
		# self.name= fibername
		self.layerNumber=layerNumber  # at certain layer
		self.fibernumber= cont             # the cont th fiber at certain layer
		self.elements=[]              # elements of certain fiber

def point_along_line(points,num,height,num_layer):

# points is the points on outer contour
# num is the number of division = the total number of points on line including the end point
	cout=1 # the order of mesh
	endpoint_set =points
	basenode=[]
	mesh=[]
	print "%d number of points have been generated on outer contour generating %d lines" %(len(endpoint_set),len(endpoint_set))
	print "%d number of points along each line" %num
	# *******************************************************
	# generat base mesh

	# append the center
	basenode.append([cout,0,0,0])
	mesh.append([cout,0,0,0])
	cout =cout+1
	for point in endpoint_set:
		x_end = point[0]
		y_end = point[1]
		xx_range = np.linspace(0,x_end,num+1)[1:]
		yy_range = np.linspace(0,y_end,num+1)[1:]

		for i in range(num):
			basenode.append([cout,xx_range[i],yy_range[i],0])
			mesh.append([cout,xx_range[i],yy_range[i],0])
			cout=cout+1
  
	print "So,nodes at each layer"
	print len(mesh)
	for j in range(num_layer)[1:]:
		new_z= j * (height*1.0/(num_layer-1))
		# print new_z
		for node in basenode:
			mesh.append([cout,node[1],node[2],new_z])
			cout=cout+1
	print "total number of nodes are"
	print len(mesh)
	return mesh



if __name__=="__main__":
	main()    