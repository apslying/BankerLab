import operator
import pprint
import copy
import sys
# fix banker=[4]
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
    visited=False
    def __init__(self):
        self.initialClaims = []
        self.currentlyHelds = []
        self.arrayOfActivities=[]

    def __repr__(self):
        return "<%s %s %s %s %s %s %s %s>" % (self.initialClaims, self.currentlyHelds, self.currentIndex, self.runTime, self.waitTime, self.blocked, self.arrayOfActivities, self.visited)


def createActivities():
    taskArray=[]
    file = open('input-01.txt', mode='r')
    #file = open(sys.argv[1], mode='r')
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

def isEnd(blockedQueue):
    for task in blockedQueue:
        if task.currentIndex>=0:
            return False
    return True

def runFifo(taskArray):
    pp = pprint.PrettyPrinter()
    openQueue=[]
    nextBlockedQueue=[]
    blockedQueue=copy.deepcopy(taskArray)

    time=0
    banker=[4]
    middlebanker=[0] #purpose is to deal with Important Note in banker.pdf
    #print taskArray
    while isEnd(blockedQueue)==False:
    #for i in range(0,5):
        # print 'time', time, '-', time+1
        # deadlocked=True
        # for task in taskArray:
        #     if task.blocked==False:
        #         deadlocked=False
        #         break
        #
        # if deadlocked==True:
        #     print 'dead'
        #     print taskArray
        #     index=0
        #     while taskArray[index].currentIndex==-1:
        #         index+=1
        #     #reached task that should be aborted
        #     #print 'index', index
        #     print banker
        #     for i, resource in enumerate(taskArray[index].currentlyHelds):
        #         banker[i]+=resource
        #         print banker
        #         taskArray[index].currentlyHelds[0]=0
        #
        #     for task in taskArray:
        #         task.blocked=False #NOT CORRECT- WILL MESS UP RUN/WAIT TIMES
        #
        #     taskArray[index].currentIndex=-2
        #     print 'here', taskArray

        if False:
            print 'nothing'
        else:
            print 'alive'
            print 'blockedQueue'
            blockedQueue.extend(nextBlockedQueue)
            blockedQueue.extend(openQueue)
            nextBlockedQueue=[]
            openQueue=[]


            for index, task in enumerate(blockedQueue):
                # check if task has terminated
                if task.currentIndex!=-1 and task.currentIndex!=-2:
                    task.visited=True
                    print 'task', index+1
                    activity=task.arrayOfActivities[task.currentIndex]
                    #perform the specified action
                    if activity.action == 'initiate':
                        print 'initiate'
                        task.initialClaims[activity.resourceType-1]=activity.numberOfResources
                        task.runTime+=1
                        task.currentIndex += 1
                        # print banker
                        # print taskArray
                        openQueue.append(task)

                    elif activity.action == 'request':
                        print 'request'
                        if banker[activity.resourceType-1]>= activity.numberOfResources:
                            print'-success'
                            task.blocked=False
                            banker[activity.resourceType - 1] -= activity.numberOfResources
                            task.currentlyHelds[activity.resourceType - 1] += activity.numberOfResources
                            task.runTime += 1
                            task.currentIndex += 1
                            openQueue.append(task)

                        else:
                            print '-blocked'
                            task.blocked=True
                            task.runTime += 1
                            task.waitTime+=1
                            nextBlockedQueue.append(task)

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
                        openQueue.append(task)


                    elif activity.action == 'terminate':
                        print 'terminate'
                        task.currentIndex=-1
                        # print banker
                        # print taskArray
                        openQueue.append(task)
                    blockedQueue=[]
            banker=map(operator.add, banker, middlebanker)
            print banker
            middlebanker=[0]
            time+=1
    return blockedQueue


def runBankers(taskArray):
    pp = pprint.PrettyPrinter()
    pp.pprint(taskArray)
    blockedQueue = []
    time = 0
    banker = [4]
    middlebanker = [0]  # purpose is to deal with Important Note in banker.pdf
    # print taskArray
    # while isEnd(taskArray) == False:
    for i in range(0,9):
        print 'time', time, '-', time + 1
        for task in taskArray:
            if task.currentIndex != -1:

                if task.blocked==True:
                    blockedQueue.append(task)

        for index, task in enumerate(blockedQueue):
            # check if task has terminated
                print 'task/blocked', index + 1
                activity = task.arrayOfActivities[task.currentIndex]
                # perform the specified action
                if activity.action == 'initiate':
                    print 'initiate'
                    task.initialClaims[activity.resourceType - 1] = activity.numberOfResources
                    task.runTime += 1
                    task.currentIndex += 1
                    # print banker
                    # print taskArray
                elif activity.action == 'request':
                    print 'request'
                    isSafe(banker, taskArray, activity)
                    if isSafe(banker, taskArray, activity):
                        print'-success'
                        task.blocked = False
                        banker[activity.resourceType - 1] -= activity.numberOfResources
                        task.currentlyHelds[activity.resourceType - 1] += activity.numberOfResources
                        task.runTime += 1
                        task.currentIndex += 1
                    else:
                        print '-blocked'
                        task.blocked = True
                        task.runTime += 1
                        task.waitTime += 1

                        # print banker
                        # print taskArray
                elif activity.action == 'release':
                    print 'release'
                    middlebanker[activity.resourceType - 1] += activity.numberOfResources
                    task.currentlyHelds[activity.resourceType - 1] -= activity.numberOfResources
                    task.runTime += 1
                    task.currentIndex += 1
                    # print banker
                    # print taskArray

                elif activity.action == 'terminate':
                    print 'terminate'
                    task.currentIndex = -1
                    # print banker
                    # print taskArray

        for index, task in enumerate(taskArray):
            # check if task has terminated
            if task not in blockedQueue and task.currentIndex != -1:
                print 'task/open', index + 1
                print
                activity = task.arrayOfActivities[task.currentIndex]
                # perform the specified action
                if activity.action == 'initiate':
                    print 'initiate'
                    task.initialClaims[activity.resourceType - 1] = activity.numberOfResources
                    task.runTime += 1
                    task.currentIndex += 1
                    # print banker
                    # print taskArray
                elif activity.action == 'request':
                    print 'request'
                    if isSafe(banker, taskArray, activity):
                        print'-success'
                        task.blocked = False
                        banker[activity.resourceType - 1] -= activity.numberOfResources
                        task.currentlyHelds[activity.resourceType - 1] += activity.numberOfResources
                        task.runTime += 1
                        task.currentIndex += 1
                    else:
                        print '-blocked'
                        task.blocked = True
                        task.runTime += 1
                        task.waitTime += 1

                        # print banker
                        # print taskArray
                elif activity.action == 'release':
                    print 'release'
                    middlebanker[activity.resourceType - 1] += activity.numberOfResources
                    task.currentlyHelds[activity.resourceType - 1] -= activity.numberOfResources
                    task.runTime += 1
                    task.currentIndex += 1
                    # print banker
                    # print taskArray

                elif activity.action == 'terminate':
                    print 'terminate'
                    task.currentIndex = -1
                    # print banker
                    # print taskArray

        for task in taskArray:
            task.visited = False
        pp.pprint(taskArray)
        banker = map(operator.add, banker, middlebanker)
        print banker
        middlebanker = [0]
        time += 1
    return taskArray


def isSafe(banker, taskArray, activity):
    newTaskArray=[]
    for task in taskArray:
        newTask=copy.deepcopy(task)
        newTaskArray.append(newTask)

    newBanker=copy.deepcopy(banker)
    pp = pprint.PrettyPrinter()
    # print 'new'
    # pp.pprint(newTaskArray)
    # print 'is it safe?'
    # print newBanker
    # pp.pprint(newTaskArray)
    # print activity
    # print '-------------------'
    bankerAfter=newBanker[activity.resourceType - 1] - activity.numberOfResources
    # pp.pprint(taskArray)
    newTaskArray[activity.taskNumber-1].currentlyHelds[activity.resourceType - 1] += activity.numberOfResources
    # print 'end'
    # pp.pprint(taskArray)
    print 'banker', bankerAfter
    #try to terminate a task to gain more resources
    flag=0
    # print 'here'
    pp.pprint(newTaskArray)
    while flag==0:
        flag=1
        for task in newTaskArray:
            if bankerAfter >= task.initialClaims[activity.resourceType-1]-task.currentlyHelds[activity.resourceType-1]:
                bankerAfter+=task.currentlyHelds[activity.resourceType-1]
                flag=0
                newTaskArray.remove(task)
                break

    print 'there'
    pp.pprint(newTaskArray)


    if newTaskArray:

        print 'false'
        return False
    else:
        print 'true'
        return True

def printSummaryData(blockedQueue):
    print blockedQueue
    print 'FIFO'
    totalRunTime=0
    totalWaitTime=0
    for index, task in enumerate(blockedQueue):
        if task.currentIndex==-2:
            print 'Task' + str(index + 1), '\t', 'aborted'
        else:
            print 'Task'+str(index+1) , '\t', task.runTime, task.waitTime, str(100*task.waitTime/float(task.runTime))+'%'
            totalRunTime+=task.runTime
            totalWaitTime+=task.waitTime

    print 'total', '\t', totalRunTime, totalWaitTime, str(float(100*totalWaitTime/float(totalRunTime)))+'%'

def printSummaryDataBankers(taskArray):
    print 'Bankers'
    totalRunTime = 0
    totalWaitTime = 0
    for index, task in enumerate(taskArray):
        print 'Task' + str(index + 1), '\t', task.runTime, task.waitTime, str(
            100 * task.waitTime / float(task.runTime)) + '%'
        totalRunTime += task.runTime
        totalWaitTime += task.waitTime

    print 'total', '\t', totalRunTime, totalWaitTime, str(float(100 * totalWaitTime / float(totalRunTime))) + '%'

printSummaryData(runFifo(createActivities()))
#printSummaryDataBankers(runBankers(createActivities()))
#runFifo(createActivities())
# createActivities()