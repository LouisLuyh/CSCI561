# Assignment 1, CSCI561, Yiheng Lu
import math, copy, time
import random as rd


def createInitPop(size):    # randomly create initial population with size of total # of cities
    tmp, population = [], []
    for i in range(size):
        tmp.append(i)

    for i in range(size):
        rd.shuffle(tmp)
        population.append(copy.copy(tmp))

    return population


def dist(p1, p2):   # calculate distance between 2 cities
    x1, y1, z1 = p1[0], p1[1], p1[2]
    x2, y2, z2 = p2[0], p2[1], p2[2]
    dist = math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

    return dist


def parentSelection(population, cityList):  # always choose the best two routes to be the parents
    fit1, fit2 = fitness(population[0], cityList), math.inf
    parent1, parent2 = population[0], []

    for i in range(len(population)):
        tmp = fitness(population[i], cityList)
        if tmp < fit2:
            fit2 = tmp
            parent2 = population[i]
        elif fit2 <= tmp < fit1:
            fit1 = tmp
            parent1 = population[i]

    return parent2, parent1


def nearestFirst(cityList):     # apply a heuristic onto the initial population (use Nearest First City approach)
    heu = [0]
    unVisited = list(range(1, len(cityList)))

    while len(unVisited) != 0:
        dis, pos = math.inf, None
        for i in unVisited:
            tmp = dist(cityList[heu[-1]], cityList[i])
            if tmp < dis:
                dis = tmp
                pos = i

        heu.append(pos)
        unVisited.remove(pos)

    return heu


def crossOver(parent1, parent2):    # crossing over the parents
    start = len(parent1) // 2 - len(parent1) // 4
    end = len(parent1) - start

    dic = dict.fromkeys(range(len(parent1)))
    for i in range(start, end):
        dic.update({i: parent1[i]})

    for i in range(len(parent2)):
        if not(start <= i < end):
            if parent2[i] not in dic.values():
                dic.update({i: parent2[i]})
            else:
                for j in parent2:
                    if j not in dic.values():
                        dic.update({i: j})

    return list(dic.values())


def mutate(child):  # randomly swap two sub-parts of a child
    if len(child) == 3:
        start = rd.randrange(0, len(child) - 1)
        end = len(child) - 1 - start
    else:
        start = rd.randrange(0, int(len(child)/2)-1)
        end = int(len(child)/2) - 1 - start
    if start > end:
        start, end = end, start

    for i in range(start, end):
        child[i], child[int(len(child)/2)+i] = child[int(len(child)/2)+i], child[i]

    return child


def fitness(path, cityList):  # fitness value = the total distance travelled
    fit = 0
    for i in range(len(path)):
        if i != len(path)-1:
            fit += dist(cityList[path[i]], cityList[path[i+1]])
        else:
            fit += dist(cityList[path[-1]], cityList[path[0]])

    return fit


def writeResult(path, cities):  # write the result to output file
    outp = open("output.txt", 'w')
    distance = fitness(path, cities)
    path.append(path[0])
    outp.write(str(distance)+'\n')
    for i in path:
        for j in cities[i]:
            outp.write(str(j)+" ")
        outp.write('\n')
    outp.close()


def timeoutT(init, numCity):    # make sure the program will not run out of time
    if numCity <= 50:
        return init + 58
    elif numCity <= 100:
        return init + 73
    elif numCity <= 200:
        return init + 118
    return init + 197


def findBest(population, cities):   # extract route with the best fitness among a population
    fit, best = math.inf, None
    for i in range(len(population)):
        tmp = fitness(population[i], cities)
        if tmp < fit:
            fit = tmp
            best = population[i]

    return best


def findRoute(numCity, cities, c):  # iterations of the genetic algorithm
    timeout = timeoutT(c, numCity)

    inip = createInitPop(numCity)
    best, tmp, counter = inip[0], None, 0
    heu = nearestFirst(cities)
    inip.append(heu)

    for i in range(10000):
        if time.time() > timeout:
            break
        if tmp == best:
            counter += 1
        if counter != 0 and tmp != best:
            counter = 0
        if counter == 300:   # same answer appears 300 times, the algorithm halts
            break

        children = []
        p1, p2 = parentSelection(inip, cities)
        c = crossOver(p1, p2)
        mc = mutate(c)

        children.append(p1)
        children.append(p2)
        children.append(c)
        children.append(mc)

        while len(children) < 75:
            if time.time() > timeout:
                break

            p1, p2 = rd.choices(inip, k=2)
            c = crossOver(p1, p2)
            children.append(c)

        inip = children
        tmp = findBest(inip, cities)
        if fitness(tmp, cities) < fitness(best, cities):
            best = tmp

    return best


def main():
    c = time.time()
    inp = open("input2.txt", "r")
    inList = []
    for i in inp:
        inList.append(i.strip('\n'))
    inp.close()

    numCity = int(inList[0])
    cities = []  # a list of cities' 3D-coordinates
    for city in inList[1:]:
        coord = city.split()
        cities.append((int(coord[0]), int(coord[1]), int(coord[2])))

    result = findRoute(numCity, cities, c)
    print(fitness(result, cities))
    writeResult(result, cities)


main()
