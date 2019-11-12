from Read_UCS import Read_Natural_UCS_Solution
import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import os
import matplotlib.lines as mlines
import matplotlib as mpl
import copy

class Attribute_knowledge:
    def __init__(self,address):
        Read_UCS=Read_Natural_UCS_Solution(address)

        self.Raw_Population=Read_UCS.population

        self.clustered=self.Conver_to_Cluster()

        self.attribute_List=self.Calculate_Attribute_importance_distribution()
        
    def Conver_to_Cluster(self):
        length=len(self.Raw_Population[0][0])
        cluster=[]
        for i in range(0,length+1):
            temp=[]
            cluster.append(temp)

        for rule in self.Raw_Population:
            level=self.General_Level(rule[0])
            cluster[level].append(rule)

        return cluster


    def General_Level(self,condition):
        count=0
        for cod in condition:
            if cod=='#':
                count+=1
        return count

    def Calculate_Attribute_importance_distribution(self):
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)
        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            distribution_list[i][cond_l]+=1
                for d_l in range(0,length):
                    distribution_list[i][d_l]=1.0*distribution_list[i][d_l]/len(self.clustered[i])
        #print (distribution_list)
        #print len(distribution_list)
        return distribution_list






class Visualization_Attribute_Importance:

     def __init__(self,address,path):
         A_K=Attribute_knowledge(address) 
         self.distribution_list=A_K.attribute_List
         self.png_path=path
         self.Drew()


     def Rainbown_color(self,length):
        R=0xff
        G_begin=0x66
        B_begin=0x66
        step=G_begin//length
        color='#'
        colors=[]
        for i in range(0,length):
            #color=color+str(hex(R))+str(hex(B_begin+step*i))+str(hex(G_begin-step*i))
            color=color+self.translate_sixteen_string(R)+self.translate_sixteen_string(B_begin+step*i)+self.translate_sixteen_string(B_begin-step*i)
            colors.append(color)
            color='#'
        #for co in colors:
        #    print co
        return colors


     def translate_sixteen_string(self,value):
        if abs(value)<0x10:
            #print value, '           ', 0x10
            result='0'
            result=result+str(hex(value)).split('x')[-1]
        else:
         result=str(hex(value)).split('x')[-1]
        return result   


     def Detect_Inforative_levels(self,list):
         result=[]
         for i in range(0,len(list)):
             for j in list[i]:
                 if j!=0:
                    result.append(i)
                    break
         print result
         return result


     def Drew(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        #self.distribution_list= self.distribution_list[0:16]
        z_first=np.asarray( self.distribution_list)
        z=z_first.T
        print z


        
        xlabels_t=[]       
        for i in range(0,len(z)):
            xlabels_t.append(str(i))
        xlabels=np.array(xlabels_t)
        xpos=np.arange(xlabels.shape[0])

        ylabels_t=[]       
        for i in range(0,len(z[0])):
            ylabels_t.append(str(i))
        ylabels=np.array(ylabels_t)
        ypos=np.arange(ylabels.shape[0])



        xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

        dx=0.3
        dy=0.1

        ax1.w_xaxis.set_ticks(xpos + dx/2.)
        ax1.w_xaxis.set_ticklabels(xlabels)

        ax1.w_yaxis.set_ticks(ypos + dy/3.)
        ax1.w_yaxis.set_ticklabels(ylabels)
        #use_color=["blue","green","purple","red","brown","orange"]
        y=[]

        for i in range(0,len(z[0])):
            y.append(i)


        use_color='black'
        for i in range(0,len(z)):
            x=[i]*len(z[i])
            if len(z)>=20:

                ax1.plot(x, y, z[i], color='black',lw=3,alpha=3)

                ax1.legend()
                for j in range(0,len(z[i])):
                    #if z[i][j] !=0:
                        #ax1.scatter(i, j, z[i][j],color=str(use_color[i]))
                    #    ax1.scatter(i, j, z[i][j],color='black')
                    if z[i][j] !=0 and i%4==0:
                        #ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=str(use_color[i]))
                        ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color='black')  
            else:
                ax1.plot(x, y, z[i], color='black',lw=2)
                #ax1.plot(x, y, z[i], color=str(use_color[i]))
                #ax1.scatter(x, y, z[i],color=str(use_color[i]))
                ax1.legend()
                for j in range(0,len(z[i])):
                    
                    #ax1.scatter(i, j, z[i][j],color=str(use_color[i]))
                    #ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=str(use_color[i]))
                    #ax1.scatter(i, j, z[i][j],color='black')
                    if  z[i][j]!=0:
                        ax1.scatter(i, j, z[i][j],color='black')
                        ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color='black')
       
        #for i in range(0,len(z)):
        #    for j in range(0,len(z[i])):
        #        ax1.text(i, j, z[i][j]+0.01, str(z[i][j]), color=use_color[1])  
        
        #ax1.set_xlabel('\n\n Attribute')
   
        ax1.set_xlabel('X ', fontsize=20)
        #ax1.set_title('10-BIT MAJORITY-ON', fontsize=30)
        #ax1.set_title('12-BIT CARRY', fontsize=30)
        #ax1.set_title('6-BIT MUX', fontsize=30)
        #ax1.set_ylabel('Number of Attributes kept in one classifier rule')
        #ax1.set_ylabel('kept attributes')
        ax1.set_ylabel('Y', fontsize=20)
        #ax1.set_zlabel("\n \n attribute percentage \n (Number of attribute / Number of attribute + Number of '#')")
        #ax1.set_zlabel("attribute percentage")
        ax1.set_zlabel("Z", fontsize=20)


        important_list=self.Detect_Inforative_levels(self.distribution_list)

        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
        y=[]
        count=0
        for i in range(0,len(z_first[0])):
            y.append(i)
         
        for level in important_list:
            x=[level]*len(z_first[level])
            n_z=z_first[level]
            #print y
            #print x
            #print n_z
            
            #ax1.plot( y, x,n_z, '--', color=color_list[count],lw=1,alpha=3)

                    
            #ax1.scatter(y, x,n_z,color=color_list[count]) 
            count+=1
            if count>len(color_list):
                count=0

            
                       



        for angle in range(1, 360,10):
            ax1.view_init(25, angle)
            plt.draw()
            png_complete_name = self.png_path + str(angle) + ".png"
            # fig.savefig(png_complete_name, dpi=(400))
            #fig.savefig(png_complete_name,bbox_inches='tight')
            fig.savefig(png_complete_name)
            plt.pause(.001)



#add='Natural_Solution\\6_MUX.txt'
#PATH='UCS_V\\MUX6\\'


#add='Natural_Solution\\6_Carry.txt'
#PATH='UCS_V\\Carry_6\\'


#add='Natural_Solution\\6_MajorityOn.txt'
#PATH='UCS_V\\Majority6\\'


#add='Natural_Solution\\8_MajorityOn.txt'
#PATH='UCS_V\\Majority8\\'

#add='Natural_Solution\\ZOO.txt'
#PATH='UCS_V\\ZOO\\'

#add='Natural_Solution\\Poly_ZOO.txt'
#add='Natural_Solution\\ZOO_RICH_OPTIMAL.txt'
#PATH='UCS_V\\ZOO_P\\'
#Visualization_Attribute_Importance(add,PATH)