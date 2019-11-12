from Read_UCS import Read_Natural_UCS_Solution
import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import os
import matplotlib.lines as mlines
import matplotlib as mpl
import copy

class Multi_Action_Attribute_Importance:
    def __init__(self,address,action_num):
        Read_UCS=Read_Natural_UCS_Solution(address)

        self.Raw_Population=Read_UCS.population

        self.infor_list=self.Record_Information(action_num)

    def Initial_result_list(self,action_num):
        result_list=[]
        attribute_list=[]
        for i in range(0,len(self.Raw_Population[0][0])):
            attribute_list.append(0)

        for i in range(0,action_num):
            temp=copy.deepcopy(attribute_list)
            result_list.append(temp)
        return result_list


    def Record_Information(self,action_num):
        information_list=self.Initial_result_list(action_num)
        count_list=[]
        for i in range(0,action_num):
            count_list.append(0)

        for rule in self.Raw_Population:
            count_list[rule[1]]+=1
            for i in range(0,len(rule[0])):
                if rule[0][i]!='#':
                    information_list[rule[1]][i]+=1

        for act in range(0,len(information_list)):
            for cod in range(0,len(information_list[act])):
                information_list[act][cod]=round(1.0*information_list[act][cod]/count_list[act],2)

        return information_list

#add='Natural_Solution\\ZOO_RICH_OPTIMAL.txt'
#Multi_Action_Attribute_Importance(add,7)

class Visualization_Mul_Action_Attribute_Importance:

     def __init__(self,address,path,action_num):
         M_I=Multi_Action_Attribute_Importance(address,action_num) 
         self.distribution_list=M_I.infor_list
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
        #z=z_first.T
        z=z_first
        #print z


        
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

            
                       



        for angle in range(1, 360,5):
            ax1.view_init(25, angle)
            plt.draw()
            png_complete_name = self.png_path + str(angle) + ".png"
            # fig.savefig(png_complete_name, dpi=(400))
            #fig.savefig(png_complete_name,bbox_inches='tight')
            fig.savefig(png_complete_name)
            plt.pause(.001)

#add='Natural_Solution\\ZOO_RICH_OPTIMAL.txt'
#add='Natural_Solution\\ZOO_100k_UCS.txt'
#PATH='UCS_V\\ZOO_G\\'
#Visualization_Mul_Action_Attribute_Importance(add,PATH,7)