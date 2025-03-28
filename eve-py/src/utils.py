# -*- coding: utf-8 -*-

import itertools
import copy
from igraph import *

def jointGoal(modules):
#    jointGoal=[]
    for m in modules:
#        jointGoal = jointGoal.append(list)
        print("player "+str(m[1])+" goal is "+str(m[5]))
        for l in list(m[5])[0].split(" "):
            print(l)

def evalNBWedge(AP,word):
    for a in AP:
        if a[0]=='~':
            if a.strip('~') in word:
                return False
        else:
            if a not in word:
                return False
    return True

'''constructs the powerset of a set of alphabets'''
def alpha2wordset(alphabets):
    wordset = set()
    for n in range(len(alphabets)+1):
        for subset in itertools.combinations(alphabets,n):
            wordset.add(subset)
    return wordset

def graph_product(GPar,DPW_prop,alphabets,cgsFlag):
    DPW_product = Graph(directed=True)
    S = set()
    colour_dict = dict()

    '''add init state for CGS'''
    if cgsFlag:
        L_t = set(alphabets).intersection(GPar.vs[0]['val'])
        # print GPar.vs[0]
        if L_t == set([]):
            L_t = set([''])
        # print 'L_t', L_t

        q = DPW_prop.es.find(_source=0,word=L_t).target

        colour_dict = GPar.vs[0]['colour']
        colour_dict['environment']=DPW_prop.vs[q]['colour']

        DPW_product.add_vertex(label=(0,q),colour=copy.copy(colour_dict),val=GPar.vs[0]['val'])

        S.add(frozenset(['s'+str(0),'q'+str(q)]))

        prevS = set()
        while prevS != S:
            prevS = copy.copy(S)
            for state in DPW_product.vs:
                for succ in GPar.vs[state['label'][0]].successors():
                    # print succ
                    L_t = set(alphabets).intersection(GPar.vs[succ.index]['val'])
                    if L_t == set([]):
                        L_t = set([''])
                    # print 'L_t', L_t
                    q = DPW_prop.es.find(_source=state['label'][1], word=L_t).target
                    # print q

                    colour_dict = GPar.vs[succ.index]['colour']
                    colour_dict['environment'] = DPW_prop.vs[q]['colour']

                    if not frozenset(['s'+str(succ.index), 'q'+str(q)]) in S:
                        DPW_product.add_vertex(label=(succ.index, q), colour=copy.copy(colour_dict), val=GPar.vs[succ.index]['val'])
                        S.add(frozenset(['s'+str(succ.index),'q'+str(q)]))
            # print S, prevS

        for v in DPW_product.vs:
            for e in GPar.es.select(_source=v['label'][0]):
                d = e['word']
                t = e.target
                # print GPar.vs[t]
                L_t = set(alphabets).intersection(GPar.vs[t]['val'])
                if L_t == set([]):
                    L_t = set([''])
                # print 'L_t', L_t
                r = DPW_prop.es.find(_source=v['label'][1], word=L_t).target
                # print v['label'][0], '--', d, '-->', t, '\t\tL(t)=', L_t
                # print v['label'][1], '--', L_t, '-->', r
                tr_idx = DPW_product.vs.find(label=(t, r)).index
                # print v.index, '====>', tr_idx
                '''check if there's already edge from sq_idx to tr_idx'''
                if tr_idx not in DPW_product.vs[v.index].successors():
                    DPW_product.add_edge(v.index, tr_idx, word=d)

    else:
        '''add init state for RMG'''
        colour_dict = GPar.vs[0]['colour']
        colour_dict['environment'] = DPW_prop.vs[0]['colour']

        DPW_product.add_vertex(label=(0, 0), colour=copy.copy(colour_dict), val=GPar.vs[0]['val'])
        S.add(frozenset(['s'+str(0), 'q'+str(0)]))

        # for v in DPW_product.vs:
        #     print v

        prevS = set()
        while prevS != S:
            prevS = copy.copy(S)
            for state in DPW_product.vs:
                # print state
                for succ in GPar.vs[state['label'][0]].successors():
                    # print succ
                    L_t = set(alphabets).intersection(GPar.vs[succ.index]['val'])
                    if L_t == set([]):
                        L_t = set([''])
                    # print 'L_t', L_t
                    #print('-------------')
                    #print('source',state['label'][1])
                   # print("L_t",L_t)
                    q = DPW_prop.es.find(_source=state['label'][1], word=L_t).target
                    #print('end',q)
                    # print '&&&&&&',q

                    colour_dict = GPar.vs[succ.index]['colour']
                    colour_dict['environment'] = DPW_prop.vs[q]['colour']

                    if not frozenset(['s'+str(succ.index),'q'+str(q)]) in S:
                        DPW_product.add_vertex(label=(succ.index,q),colour=copy.copy(colour_dict),val=GPar.vs[succ.index]['val'])
                        S.add(frozenset(['s'+str(succ.index),'q'+str(q)]))
            # print S, prevS

        for v in DPW_product.vs:
            for e in GPar.es.select(_source=v['label'][0]):
                d = e['word']
                t = e.target
                # print GPar.vs[t]
                L_t = set(alphabets).intersection(GPar.vs[t]['val'])
                if L_t == set([]):
                    L_t = set([''])
                # print 'L_t', L_t
                r = DPW_prop.es.find(_source=v['label'][1],word=L_t).target
                # print v['label'][0], '--', d, '-->', t, '\t\tL(t)=', L_t
                # print v['label'][1], '--', L_t, '-->', r
                tr_idx = DPW_product.vs.find(label=(t,r)).index
                # print v.index,'====>',tr_idx
                '''check if there's already edge from sq_idx to tr_idx'''
                if tr_idx not in DPW_product.vs[v.index].successors():
                    DPW_product.add_edge(v.index,tr_idx,word=d)

    for v in DPW_product.vs():
        v['name']=v.index

    # printGParDetails(DPW_product)

    return DPW_product

'''this function adds two MP players for E/A-Nash'''
'''for CGSs'''
def addMPPlayers_cgs(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())
                
                
'''for RMGs'''                
def addMPPlayers_rmg(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())

def printGParDetails(GPar):
    print ("\n######## Vertex List ########")
    for v in GPar.vs():
        print(v)
    print ("############################################################\n")

    print ("\n######## Edge List ########")
    print(GPar.get_edgelist())
    print ("############################################################\n")

    print ("\n######## Edge labels ########")
    for e in GPar.es():
        print(e)
    print ("############################################################\n")

    return True

def printSynthSigmaDetails(GPar):
    print ("\n\n######## Vertex List ########")
    for v in GPar.vs():
        # print v
        if v['val'] is None:
            v['val'] = []

        print("state:", v['label'], "| val:", list(v['val']))
        # try:
        #     print "state:", v['label'], "| val:", list(v['val'])
        # except TypeError:
        #     # print "state:", v['label'], "| val:", list([''])
        #     print "\n"

    print ("############################################################\n")

    print ("\n######## Edge List ########")
    print(GPar.get_edgelist())
    print ("############################################################\n")

    # for e in GPar.es:
    #     del e['label']
    # try:
    #     del GPar.es['label']
    # except KeyError:
    #     pass
    # GPar.es['Action Profile'] = GPar.es['word']

    print ("\n######## Transition Profile ########")
    for e in GPar.es():
        print(GPar.vs[e.source]['label'], " --(", list(e['word']), ")--> ", GPar.vs[e.target]['label'])
    print ("############################################################\n")

    return True

def num2name(w,modules):
    coal=[]
    for i in w:
        coal.append(list((modules[i])[1])[0])
    return coal

def check_draw_flag():
    with open("draw_flag","r") as f:
        data = f.read()
        if data == "1":
            return True
        else:
            return False

def check_verbose_flag():
    with open("verbose_flag","r") as f:
        data = f.read()
        if data == "1":
            return True
        else:
            return False

def generate_set_W(modules):
    W = []
    for n in range(len(modules)+1):
        for subset in itertools.combinations(list(range(0,len(modules))),n):
#            print subse t
            #W.add(subset)
            W.append(subset)
    return W
    
def generate_set_modules(modules):
    W = []
    for n in range(len(modules)+1):
        for subset in itertools.combinations((modules),n):
            print(subset)
            #W.add(subset)
            W.append(subset)
    return W
    
def get_l(w,modules):
    N = list(range(0,len(modules)))
    l = [item for item in N if item not in w]
    return l
    
def build_GPar_L(GPar,w,l,PUN_L):
    GPar_L=copy.copy(GPar)
    to_del=[]
    for v in GPar_L.vs:
            if v['name'] not in PUN_L:
#                print 'VINDEX', v.index
                to_del.append(v.index)
#                GPar_L[frozenset(l)].delete_vertices(v.index)
    GPar_L.delete_vertices(to_del)
    return GPar_L

'''
This function builds product of streett automata
'''    
def build_streett_prod(GPar_L,w,modules):
    '''build streett automata from GPar_L'''
    s_Alpha=[]
    max_colour = get_max_colour(GPar_L)
#    print 'MAX',max_colour
#     print('#####w######',w,modules)
    for pl in w:
        Alpha=[]
        for i in range(max_colour):
            j=2*i
            a={}
            if i==0:
                a['C'+str(i)]=[]
            else:
                a['C'+str(i)]=copy.copy(list(Alpha[i-1]['C'+str(i-1)]))
            a['E'+str(i)]=[]
        
            pl_name = list(modules[pl][1])[0]
            # print pl_name
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j):
                a['C'+str(i)].append(v['name'])
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j+1):
                a['E'+str(i)].append(v['name'])
            a['C'+str(i)]=set(a['C'+str(i)])
            a['E'+str(i)]=set(a['E'+str(i)])
            Alpha.append(a)
        s_Alpha.append(Alpha)
    # print('>>>> s_ALPHA',s_Alpha)
    return s_Alpha
    
    
'''
This function check Street automaton emptiness
'''            
def Streett_emptyness(GPar_L,s_Alpha,modules):    
    S = copy.copy(GPar_L)
#    for v in S.vs:
#        print v
#     print S.get_edgelist()
#     for e in S.es():
#         print e

    max_colour = get_max_colour(GPar_L)
    while True:
        '''to nontrivial SCC'''
        '''selfloop'''

        SCC=[]
        for v in S.vs():
#            print "XXX", v
            if v in v.successors():
#                print v
                SCC.append([v['name']])
        '''clusters'''
        for c in S.components():
            if len(c)>1:
                SCC.append([S.vs[v]['name'] for v in c])
#            print SCC
        changed=False
        for c in SCC:
#            print 'C',c
            del_flag=False
#            for Alpha in s_Alpha:1
            for i in range(max_colour):
                e_to_del=[]
                v_to_del=[]
#                for i,a in enumerate(Alpha):
                for x,Alpha in enumerate(s_Alpha):
#                    print 'ALP',x, Alpha
                    c_cap_E=Alpha[i]['E'+str(i)].intersection(set(c))
                    c_cap_C=Alpha[i]['C'+str(i)].intersection(set(c))
                    if c_cap_E and not c_cap_C:
#                        print '##',c_cap_E
                        
                        '''need to also check if the edge exists in DSW S'''
                        if len(c_cap_E)==1 and ((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])) in S.get_edgelist()):
#                        if len(c_cap_E):
#                            S.delete_edges((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
                            e_to_del.append((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
#                            break
                        else:
#                            S.delete_vertices(namelist2idxlist(S,list(c_cap_E)))
#                            print 'namelist2idxlist', namelist2idxlist(S,list(c_cap_E))
#                            v_to_del.append(namelist2idxlist(S,list(c_cap_E))[0])
                            v_to_del = v_to_del + namelist2idxlist(S,list(c_cap_E))
                        del_flag=True
                        changed=True
#                        break
                if del_flag:
#                    print 'e_to_del',e_to_del
#                    print 'v_to_del',idxlist2namelist(S,v_to_del)
                    S.delete_edges(list(set(e_to_del)))
#                    try:
#                        S.delete_edges(list(set(e_to_del)))
#                    except ValueError:
#                        print 'e_to_del',e_to_del
#                        for v in S.vs():
#                            print v
#                        print S.get_edgelist()
                    S.delete_vertices(list(set(v_to_del)))
                    break
            if del_flag:
                break
            
            
        if not changed:
            break
        
    '''delete trivial SCC and non-SCC'''
    to_del=[]
    to_del_sigma=[]
    self_loop=[]
    '''trivial'''
    for v in S.vs:
        if len(v.successors())==0:
            to_del.append(v.index)
            to_del_sigma.append(v.index)
        else:
            '''self-loop'''
            if v in v.successors():
                self_loop.append(v.index)
            
    '''non-SCC'''
#    print 'SSSSSSLLLLLLL', self_loop
    for c in S.components():
#        print c
        if len(c)==1 and c[0] not in self_loop:
            to_del.append(c[0])
            
    '''return strategy profile \vec{sigma}'''
    S_cpy = copy.copy(S)
    S_cpy.delete_vertices(to_del_sigma)
    
    '''emptiness check'''
    S.delete_vertices(to_del)
                
#    return S.simplify(multiple=True,loops=False)
    return S,S_cpy
    
def get_max_colour(GPar):
    vcolour_max=0
    for v in GPar.vs:
        if max(v['colour'].values())>vcolour_max:
#            print 'asdas',max(v['colour'].values())
            vcolour_max = max(v['colour'].values())
    return vcolour_max
    
def idxlist2namelist(G,idxlist):
    namelist=[]
    for v in idxlist:
        namelist.append(G.vs[v]['name'])
    return namelist

def name2idx(G,name):
    for v in G.vs.select(name=name):
        return v.index

def label2idx(G,label):
    return G.vs.find(label=label).index
        
def namelist2idxlist(G,namelist):
    idxlist=[]
    for name in namelist:
        idxlist.append(name2idx(G,name))
    return idxlist

def drawTTPG_kk(TTPG):
    layout = TTPG.layout('kk')
#    mc = get_max_prior(TTPG)+1
#    r = 3*(float(TTPG.vcount())/mc)
    for v in TTPG.vs:
        v['color']=hsv_to_rgb(float(v.index)/TTPG.vcount(),1,1)
        v['size']=20
        if v['itd']:
            v['shape']='circle'
        else:
            v['shape']='square'
    for e in TTPG.es:
        e['color']=TTPG.vs[e.source]['color']
    TTPG.vs['label']=[None for v in TTPG.vs]
    TTPG.vs[0]['label']='S0'
    visual_style = {}
    visual_style['layout']=layout
    visual_style['bbox']=(1000,1000)
    visual_style['margin']=40
#    visual_style['vertex_label_dist']=2
    visual_style['autocurve']=True
    visual_style['vertex_frame_width']=0
    plot(TTPG, **visual_style)


def replace_symbols(string):
    old = ['&&', '||', '[]', '<>']
    new = ['and', 'or', 'G', 'F']
    for i, j in enumerate(old):  ## replace symbols into 'normal' ones
        string = string.replace(j, new[i])
    return string


'''This method synthesises a lasso witness. However, the lasso does not include punishment actions when applicable. 
Thus, in some lassos, there may seem to be a beneficial deviation by player i. 
However, such a deviation may be spurious because there exist punishment actions by the coalition -i 
that prevent the goal of i from being satisfied. Can we also extract these punishment actions? 
This is TODO...
'''
def synth_lasso(g, s_Alpha, graph_product_for_rgmFlag):

    '''rectifying vertex label'''
    if not graph_product_for_rgmFlag:
        for v in g.vs:
            v['label'] = v['name']


    '''check for each SCC in the witness graph/automaton'''
    for i in g.clusters():
        if subcyc(idxlist2namelist(g, i), s_Alpha, g, graph_product_for_rgmFlag):
            break
        # if not graph_product_for_rgmFlag:
        #     # print("EE", idxlist2namelist(g,i))
        #     if subcyc(idxlist2namelist(g,i), s_Alpha, g, graph_product_for_rgmFlag):
        #         break
        # else:
        #     # subcyc(i, s_Alpha, g, graph_product_for_rgmFlag)
        #     if subcyc(idxlist2namelist(g, i), s_Alpha, g, graph_product_for_rgmFlag):
        #         break

'''this method checks for a good subset of a given SCC'''
def subcyc(scc,s_Alpha,g,graphprodFlag):
    '''iterate through each subset, starting from the smallest, producing (probably) the smallest lasso'''
    for n in range(1,len(scc) + 1):
        for subset in itertools.combinations((scc), n):
            # print('SUBSET:', subset)
            # if not graphprodFlag:
            subset = g.vs.select(name_in=subset)

            subg = g.subgraph(subset)

            '''if the subset is strong connected, then check it whether it is good wrt the Streett condition'''
            if g.subgraph(subset).is_connected() and len(subg.get_edgelist())>0:
                if check_good(subset,s_Alpha,g,graphprodFlag):
                    return True

def check_good(component,s_Alpha,g,graphprodFlag):
    max_col = get_max_colour(g)

    # print("MAX COL", max_col)

    '''for each index of the Streett condition, check if it is good/satisfying'''
    for i in range(max_col):
        for a in s_Alpha:
            # print("COMP:", component)
            # print(a[i])
            c_cap_E = a[i]['E' + str(i)].intersection(set(component))
            c_cap_C = a[i]['C' + str(i)].intersection(set(component))

            '''if bad/unsatisfying then return false'''
            if c_cap_E and not c_cap_C:
                # print("BAD")
                return False

    '''if the subset/component is strongly connected, then build the subgraph from it'''
    if g.subgraph(component).is_connected() and len(g.subgraph(component).get_edgelist())>0:
        build_subgraph(component,g,graphprodFlag)
        return True
    else:
        return False

def build_subgraph(component,g,graphprodFlag):
    # print(component)
    vertex_set = set(component)
    # print(vertex_set)
    subg = g.subgraph(vertex_set)
    # plot(subg, target="subg.png")
    # build_cycle(subg,vertex_set)

    '''find a cycle within the subgraph'''
    cycle = subgraph_traversal(subg,vertex_set)
    # print("CYCLE:", cycle)

    '''build the path of the cycle in the subgraph'''
    cycle_path, cycle_edges = get_cycle_path(cycle,subg,g)

    print("CYCLE PATH:", cycle_path)

    # for v in cycle_path:
    #     print(g.vs.select(label_eq=v)[0])


    '''if the initial state is not part of the cycle, then we need to find the shortest prefix'''
    if 0 not in component:
        prefix, pref_edges = find_prefix(g,cycle)
        # print("LASSO:", prefix, cycle_path)
        lasso = prefix[:-1] + cycle_path
    else:
        pref_edges = []
        lasso = cycle_path

    print("LASSO:", lasso)

    '''the edges of the lasso path are composed from the cycle and the prefix edges'''
    included_edges = cycle_edges + pref_edges

    '''build a subgraph that includes only those edges inlcuded in the lasso'''
    lasso_graph_edges = g.subgraph_edges(included_edges, delete_vertices=False)
    plot(lasso_graph_edges, target="edges.png")

    # if not graphprodFlag:
    lasso = g.vs.select(name_in=lasso)

    '''delete vertices that are not in the lasso'''
    lasso_graph = lasso_graph_edges.subgraph(lasso)

    '''plot the lasso'''
    plot(lasso_graph, target="lasso.png")


def get_cycle_path(cycle,subg,g):
    path = [cycle[0]]
    edges = []

    '''iterate through each pair of connected vertices, and get the edges connecting them'''
    for i in range(len(cycle)):

        '''if the pair of vertices are adjacent/neighbours, then only need 1 edge'''
        if subg.are_connected(subg.vs.select(name_eq=cycle[i])[0],subg.vs.select(name_eq=cycle[(i+1)%len(cycle)])[0]):
            path.append(cycle[(i+1)%len(cycle)])
            edges.append(g.get_eid(g.vs.select(name_eq=cycle[i])[0],g.vs.select(name_eq=cycle[(i+1)%len(cycle)])[0], directed=True))
        else:
            '''else, they are not adjacent/neighbours, then get the set of edges connecting them'''
            spath = subg.get_shortest_paths(subg.vs.select(name_eq=cycle[i])[0],to=subg.vs.select(name_eq=cycle[(i+1)%len(cycle)])[0], mode=OUT, output='vpath')[0]

            # Convert indices to names
            path_names = [subg.vs[i]["name"] for i in spath]

            path.extend(path_names[1:])

            for i in range(len(path_names)-1):
                edges.append(g.get_eid(g.vs.select(name_eq=path_names[i])[0],g.vs.select(name_eq=path_names[(i+1)%len(path_names)])[0], directed=True))

    return path, edges


'''this method traverses the given vertex set using DFS to find the cycle path'''
def subgraph_traversal(subg,vertex_set):
    result = subg.dfs(0)
    cycle = []

    for v in result[0]:
        cycle.append(subg.vs[v]['name'])

    return cycle

'''this method find the shortest prefix connecting the initial state with the cycle in the lasso'''
def find_prefix(g,cycle):
    paths = {}
    edges = []

    for v in cycle:
        v = g.vs.select(name_eq=v)[0].index
        paths[v] = g.get_shortest_paths(0,to=v, mode=OUT, output='vpath')

    # get the shortest path
    shortest_prefix = min(paths, key=lambda x: len(paths[x]))

    prefix = paths[shortest_prefix][0]

    prefix = [g.vs[v]['label'] for v in prefix]

    print("PREFIX:", prefix)

    #get the edges
    for i in range(len(prefix)-1):
        edges.append(g.get_eid(g.vs.select(name_eq=prefix[i])[0],
                               g.vs.select(name_eq=prefix[(i + 1) % len(prefix)])[0], directed=True))


    return prefix, edges
