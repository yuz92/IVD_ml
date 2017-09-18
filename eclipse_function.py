def point_along_line(points,num,height,num_layer):  
# points is the points on outer contour
# num is the number of division = the total number of points on line including the end point
    cout=1 # the order of mesh 
    endpoint_set =points 
    basenode=[]
    mesh=[]
    print ("%d number of points have been generated on outer contour generating %d lines" %(len(endpoint_set),len(endpoint_set)) )
    print ("%d number of points along each line" %num) 
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
  
    print ("So,number of nodes at each layer = ", len(mesh))
    for j in range(num_layer)[1:]:
        new_z= j * (height*1.0/(num_layer-1))
        # print new_z
        for node in basenode: 
            mesh.append([cout,node[1],node[2],new_z])
            cout=cout+1     
    print ("total number of nodes =", len(mesh))
    return mesh          
 
class supereclipse2d(object):

    def __init__(self,rx,ry,n):
        self.rx=rx 
        self.ry=ry
        self.n=n  # controls the superformula shape 
        self.x=[]
        self.y=[]
        self.cord=[]
        
    def generate(self):

        
        with open('node_final.txt','r') as f: 
            content=f.readlines()
            new_content = [x.strip() for x in content] 
            each_line =[yy.split() for yy in new_content]
        for i in each_line:
            x=float(i[0][1:-1]); 
            y=float(i[1][:-1]); 
            self.x.append(x)
            self.y.append(y)
            self.cord.append([x,y])

        return len(self.x)

    def check(self):
        plt.figure()
        plt.plot(self.x,self.y,'ro')
        font_title = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}    
        font_axis = {'family' : 'normal',
                'weight' : 'bold',
                'size'   : 18}    
        plt.title('Inhomogeneous Mesh',**font_title)
        plt.xlabel('x-axis[mm]',**font_axis)
        plt.ylabel('y_axis [mm]',**font_axis)
        plt.show()
 


 
def plotmesh_onelayer(meshpoint):
# The mesh is organized: [number of nodes, x,y,z]
    x_cord=[]
    y_cord=[] 
    for i in meshpoint: 
        x_cord.append(i[1])
        y_cord.append(i[2]) 
     
    plt.figure()
    plt.plot(x_cord,y_cord,'ro')
    font_title = {'family' : 'normal',
    'weight' : 'bold',
    'size'   : 22}    
    font_axis = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 18}    
    plt.title('Mesh Points on the bottom Layer',**font_title)
    plt.xlabel('x-axis[mm]',**font_axis)
    plt.ylabel('y_axis [mm]',**font_axis)
    plt.show()
     
    
# import numpy as np    
# from math import * 
# import matplotlib.pyplot as plt
# eclipse1 =supereclipse2d(25,17.5,1)
# eclipse1.generate()
# eclipse1.check()
# mesh=point_along_line(eclipse1.cord,5,9,4)
# plotmesh_onelayer(mesh)

