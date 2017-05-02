import operator
import pprint
class Activity:
    def __init__(self, action, taskNumber, delay, resourceType, numberOfResources):
        self.action=action
        self.taskNumber=taskNumber
        self.delay=delay
        self.resourceType=resourceType
        self.numberOfResources=numberOfResources

    def __repr__(self):
        return "<%s %s %s %s %s>" % (self.action, self.taskNumber, self.delay, self.resourceType, self.numberOfResources)

class Task:
    currentIndex=0
    runTime=0
    waitTime=0
    blocked=False
    def __init__(self):
        self.initialClaims = []
        self.currentlyHelds = []
        self.arrayOfActivities=[]

    def __repr__(self):
        return "<%s %s %s %s %s %s %s>" % (self.initialClaims, self.currentlyHelds, self.currentIndex, self.runTime, self.waitTime, self.blocked, self.arrayOfActivities)


def createActivities():

    taskArray=[]
    file = open('input-06.txt', mode='r')
    a = file.read()
    assert isinstance(a, str)
    a=a.replace('  ', ' ')
    arr=a.split('\n')
    assert isinstance(arr, list)
    for line in arr:
        data=line.split(' ')
        assert isinstance(data, list)
        #print data
        for char in data:
            if char=='':
                data.remove(char)
        #everything before this point is to read and reformat the data
        if line==arr[0]: #first line
            for i in range(0, int(data[0])):
                #create number of tasks specified in first line of file
                obj=Task()
                #set initial claims and resources currently held to 0
                for j in range(0, int(data[1])):
                    obj.initialClaims.append(0)
                    obj.currentlyHelds.append(0)
                taskArray.append(obj)

        elif line==arr[len(arr)-1]:
            print 'last line'
        else:
            obj=Activity(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]))
            taskArray[obj.taskNumber-1].arrayOfActivities.append(obj)

    #print taskArray
    return taskArray

def isEnd(taskArray):
    for task in taskArray:
        if task.currentIndex>=0:
            return False
    return True

def runFifo(taskArray):
    pp = pprint.PrettyPrinter()
    time=0
    banker=[4]
    middlebanker=[0] #purpose is to deal with Important Note in banker.pdf
    #print taskArray
    while isEnd(taskArray)==False:
        print 'time', time, '-', time+1
        deadlocked=True
        for task in taskArray:
            if task.blocked==False:
                deadlocked=False
                break

        if deadlocked==True:
            print 'dead'
            print taskArray
            index=0
            while taskArray[index].currentIndex==-1:
                index+=1
            #reached task that should be aborted
            #print 'index', index
            print banker
            for i, resource in enumerate(taskArray[index].currentlyHelds):
                banker[i]+=resource
                print banker
                taskArray[index].currentlyHelds[0]=0

            for task in taskArray:
                task.blocked=False #NOT CORRECT- WILL MESS UP RUN/WAIT TIMES
                task.waitTime+=1

            taskArray[index].currentIndex=-2
            print 'here', taskArray


        else:
            print 'alive'
            for index, task in enumerate(taskArray):
                # check if task has terminated
                if task.currentIndex!=-1 and task.currentIndex!=-2:
                    print 'task', index+1
                    task.blocked=False #reset blocked state
                    activity=task.arrayOfActivities[task.currentIndex]
                    #perform the specified action
                    if activity.action == 'initiate':
                        print 'initiate'
                        task.initialClaims[activity.resourceType-1]=activity.numberOfResources
                        task.runTime+=1
                        task.currentIndex += 1
                        # print banker
                        # print taskArray
                    elif activity.action == 'request':
                        print 'request'
                        if banker[activity.resourceType-1]>= activity.numberOfResources:
                            print'-success'
                            banker[activity.resourceType - 1] -= activity.numberOfResources
                            task.currentlyHelds[activity.resourceType - 1] += activity.numberOfResources
                            task.runTime += 1
                            task.currentIndex += 1
                        else:
                            print '-blocked'
                            task.blocked=True
                            task.runTime += 1
                            task.waitTime+=1

                        # print banker
                        # print taskArray
                    elif activity.action == 'release':
                        print 'release'
                        middlebanker[activity.resourceType - 1] += activity.numberOfResources
                        task.currentlyHelds[activity.resourceType - 1] -= activity.numberOfResources
                        task.runTime+=1
                        task.currentIndex += 1
                        # print banker
                        # print taskArray

                    elif activity.action == 'terminate':
                        print 'terminate'
                        task.currentIndex=-1
                        # print banker
                        # print taskArray
            pp.pprint(taskArray)
            banker=map(operator.add, banker, middlebanker)
            print banker
            middlebanker=[0]
            time+=1
    return taskArray


def printSummaryData(taskArray):
    print taskArray
    print 'FIFO'
    totalRunTime=0
    totalWaitTime=0
    for index, task in enumerate(taskArray):
        if task.currentIndex==-2:
            print 'Task' + str(index + 1), '\t', 'aborted'
        else:
            print 'Task'+str(index+1) , '\t', task.runTime, task.waitTime, str(100*task.waitTime/float(task.runTime))+'%'
            totalRunTime+=task.runTime
            totalWaitTime+=task.waitTime

    print 'total', '\t', totalRunTime, totalWaitTime, str(float(100*totalWaitTime/float(totalRunTime)))+'%'



printSummaryData(runFifo(createActivities()))
# runFifo(createActivities())
# createActivities()