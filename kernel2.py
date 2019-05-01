import matplotlib.pyplot as plt
from classes2 import *
import pdb
import math


XLIM = [0, 100]
YLIM = [0, 100]

fig = plt.figure()
ax = fig.add_subplot(111)

#triangle
#P = StructuredPoly([(0,0), (10,10), (0,20), (20,10), (0,0)])

#chomper
#P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 4), (2, 6), (10, 8), (10, 10), (0, 10)])

#star
P = StructuredPoly([(0, 50), (30, 70), (50, 100), (70, 70), (100, 50), (70, 30), (50, 0), (30, 30), (0, 50)])

# P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 2), (2, 8), (10, 8), (10, 10), (0, 10)])



def getInputPoly():
    ax.set_title('click done to create your polygon')
    plt.subplots_adjust(bottom=0.2)

    axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
    bdone = Button(axdone, 'Done')

    line, = ax.plot([], [], marker = 'o')
    linebuilder = LineBuilder(line)
    bdone.on_clicked(linebuilder._finish)
    plt.show()

    lst = []
    for x,y in zip(linebuilder.xs, linebuilder.ys):
        lst.append((x, y))
    return StructuredPoly(lst)




def getKernel(P):
    poly = [tuple(x) for x in P.polygon.get_xy()]
    angle = P.flex_dictionary
    pdb.set_trace()

    list_of_vertices = poly
    if angle[list_of_vertices[0]] == -1:
        # If so, make a K_0
        initial_node = Node(list_of_vertices[0])
        head_lambda = Lambda((list_of_vertices[1][0] - list_of_vertices[0][0], list_of_vertices[1][1] - list_of_vertices[0][1]))
        tail_lambda = Lambda((list_of_vertices[0][0] - list_of_vertices[-2][0], list_of_vertices[0][1] - list_of_vertices[-2][1]))

        '''
        head_lambda.next = initial_node
        head_lambda.prev = None

        initial_node.next = tail_lambda
        initial_node.prev = head_lambda

        tail_lambda.next = None
        tail_lambda.prev = initial_node
        '''

        P.k.addHead(head_lambda)
        P.k.addTail(tail_lambda)
        P.k.addNode(head_lambda, initial_node, tail_lambda)
        P.F = head_lambda
        P.L = tail_lambda
        #return P.k

    else:
        return poly

    for i in range(1, len(poly) - 2):
        if angle[poly[i]] == -1:
            result = _reflex(i, poly, P.k, P.F, P.L)
        elif angle[poly[i]] == 1:
            result = _convex(i, poly, P.k, P.F, P.L)

        if result == -1:
            return Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)])

    return P.k #JeffsAlgorithm(ker[len(poly) - 2])




def _reflex(i, P, K, F, L):
    edge = (P[i+1][0] - P[i][0], P[i+1][1] - P[i][1])
    new_vertex = Node(P[i+1])
    new_lambda = Lambda(edge)
    new_lambda.next, new_vertex.prev = new_vertex, new_lambda

    if ccw(new_vertex, F, new_lambda) == 1:
        pointer1, K_edge_int = F, None
        while pointer1 != L and K_edge_int == None:
            K_edge_int = findIntersection(pointer1, pointer1.next, new_lambda, new_vertex)
            pointer1 = pointer1.next

        if K_edge_int == None:
            return -1

        wprime = Node(K_edge_int)

        pointer2, K_edge_int = F, None
        while pointer != K.getTail() and K_edge_int == None:
            K_edge_int = findIntersection(pointer2.prev, pointer2, new_lambda, new_vertex)
            pointer2 = pointer2.prev

        pdb.set_trace()
        H_slope, T_slope = slope(K.head, K.head.next), slope(K.tail.prev, K.tail)
        edge_slope = slope(new_lambda, new_vertex)
        if K_edge_int != None:
            wdprime = Node(K_edge_int)
            K.addNode(pointer2, wdprime, pointer1)
            K.addNode(wdprime, wprime, pointer1)

        elif dot((-K.tail[0], -K.tail[1]), new_lambda) >= 0 and dot(new_lambda, K.head) >= 0:
            K.addNode(pointer2, wprime, pointer1)
            K.addNode(None, new_lambda, wprime)
            wdprime = None

        else:
            pointer3, K_edge_int = K.tail, None
            while K_edge_int != None:
                K_edge_int = findIntersection(pointer3.prev, pointer3, new_lambda, new_vertex)
                pointer3 = pointer3.prev

            wdprime = Node(K_edge_int)
            K.addNode(pointer3, wdprime, pointer1)
            K.addNode(wdprime, wprime, pointer1)
            K.setHead(wprime)
            K.setTail(wdprime)
            K.makeCircular()

        if wdprime == None:
            F = new_lambda
        else:
            F = wdprime

    else:
        pointer4 = F
        F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
        while F_pt_order == 1:
            F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
            pointer4 = pointer4.next
        F = pointer4

    pointer5, L_pt_order = L, 0
    while pointer5 != K.head and L_pt_order == -1:
        L_pt_order = ccw(new_vertex, pointer5.prev, pointer5)
        pointer5 = pointer5.next

    L = pointer5

    return 1




def _convex(i, P, K, F, L):
    return 1




def main():
    Q = getInputPoly()
    '''
    print(Q._pts)
    print(Q.polygon.get_xy())
    print(Q.flex_dictionary)
    '''
    print(getKernel(Q))


if __name__ == '__main__':
    main()
