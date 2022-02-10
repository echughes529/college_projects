import numpy as np
import matplotlib.pyplot as plt


KB = 1
J = 1
n_list = []
Mn_list =[]
T_list = []
M_list = []
stdM_list = []

print("Emma Hughes 19335855")

def initRandom(N):
    #initialize a square NxN lattice with a random state w
    return np.random.choice([-1,1], size=(N,N))
w = initRandom(10)    
    
def neighbors(w):
    #finds the neighbors of each lattice site
    nrows=w.shape[0]
    ncols=w.shape[1]
    
    nb=[]
    for j in range(nrows):
        for i in range(ncols):
            nb.append([[j, (i-1)%ncols], [j, (i+1)%ncols], [(j+1)%nrows, i], [(j-1)%nrows, i]])
    return np.array(nb)


def totalEnergy(w, neighbor, J):
    #computes the total energy of the state w
    en=0.
    for i in range(w.size):
        for n in neighbor[i]:
            en+=-J*w.ravel()[i]*w[n[0],n[1]]
    return en


def magnetization(w):
    #computes magnetization per spin for the state w
    return w.sum()/w.size



def step(en, w, neighbor, T, J):
    #metropolis step
    for i in range(w.size):
        deltaE=2*J*np.sum(w.ravel()[i]*w[neighbor[i].T[0], neighbor[i].T[1]])
        
        if deltaE<=0:
            w.ravel()[i]=-w.ravel()[i]
            en+=deltaE
        else:
            p=np.exp(-deltaE/(KB*T))
            if np.random.rand()<p:
                w.ravel()[i]=-w.ravel()[i]
                en+=deltaE
                
    return en


def plotState(w, figsize=(8,8)):
        #show state w in a matplotlib figure
        xdim=w.shape[0]
        ydim=w.shape[1]
        x, y = np.linspace(0, xdim-1, xdim), np.linspace(0, ydim-1, ydim)
        Y, X = np.meshgrid(y, x)
        
        fig, ax=plt.subplots(figsize=figsize)
        ax.set_aspect('equal')
        ax.scatter(X, Y, c=w, marker='o', s=2000*(figsize[0]/xdim)*(figsize[1]/ydim))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(Y.min(), Y.max())
        ax.set_xlim(X.min(), X.max())
        return fig


def ising(w, T, J, equilibrationSteps, averageSteps, showPlot):
    
    neighbor=neighbors(w)
    en=totalEnergy(w, neighbor, J)
    
    
    #equilibration
    print("Doing equilibration")
    
    for i in range(equilibrationSteps):
        en=step(en, w, neighbor, T, J)
        
        mstep=magnetization(w)
        n_list.append(i)
        Mn_list.append(mstep)
        print("Step %3i:\tM=%6.4f"%(i, mstep))


    print("")
        
    #averaging
    print("Doing averages")
    
    msum=0.
    msum2=0.
    for i in range(averageSteps):
        step(en, w, neighbor, T, J)
        
        mstep=magnetization(w)
        msum=msum+mstep
        msum2=msum2+mstep*mstep
        
        print("Step %3i:\tM=%6.4f\t<M>=%6.4f"%(i+equilibrationSteps, mstep, msum/(i+1)))
     
     
    #result
    M=msum/averageSteps
    stdM=np.sqrt((msum2/averageSteps)-(M)**2)
    print("")
    print("Temperature = %f\tMagnetization = %f +- %f"%(T,M,stdM))
    
    
    if showPlot:
        fig=plotState(w)
        plt.show()
        plt.close()
    
    return (w, T, M, stdM)




fig = plt.figure(2)
for i in range (0, 7):
    for n in range (0, 20):
        w, T, M, stdM = ising(w, T= (n/5.0), J=1, equilibrationSteps=400, averageSteps=400, showPlot=True)
        T_list.append(T)
        M_list.append(M)
        stdM_list.append(stdM)
        

    plt.plot(T_list, M_list, 'o', color = 'darkred')  
plt.title('Magnetisation Vs. Temperature for 10x10 Grid')   
plt.xlabel('Temperature (K)') 
plt.ylabel('Magnetisation')


fig = plt.figure(3)
w, T, M, stdM = ising(w, T= 2.0, J=1, equilibrationSteps = 500, averageSteps=50, showPlot=False)
plt.plot(n_list, Mn_list, '.', color = 'darkred')  
plt.title('Magnetisation Vs. Step Number for 100x100 Grid')   
plt.ylabel('Magnetisation') 
plt.xlabel('Steps')     
    
    
