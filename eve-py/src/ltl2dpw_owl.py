# -*- coding: utf-8 -*-
import re
import subprocess as sp  # Used to call external processes
from igraph import *  # igraph library for graph processing
from utils import alpha2wordset



def preprocess_ltl_formula(ltl_fml):
    """
    Preprocess the LTL formula, converting '[]' to 'G' and '<>' to 'F'.
    """
    # Convert [] to G, <> to F
    ltl_fml = ltl_fml.replace('[]', 'G').replace('<>', 'F')
    
    return ltl_fml

def replace_number_with_bool(condition, num, bool_value):

    return re.sub(rf'\b{num}\b', str(bool_value), condition)

def ltl2dpw(ltl_fml):

    # Preprocess LTL formula to replace [] and <> operators
    ltl_fml = preprocess_ltl_formula(ltl_fml)
    
    # Call external tool ltl2 for conversion
    work_dir = "../owl-linux-musl-amd64-21.0/bin"
    try:
        lines = sp.Popen(['./owl', 'ltl2dpa', '-f', ltl_fml, '--state-acceptance'], cwd=work_dir, stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8')
        out, err = lines.communicate()  # Get outputS
        if err:
            print("Transfer ERROR:", err)
            return None
    except Exception as e:
        print("Running ERROR:", e)
        return None
    
    out = out.splitlines()  # Split output by lines
    DPW = Graph(directed=True)  # Create a directed graph

    in_body = False
    current_state = None
    next_state = None
    state_colour = 0
    alphabets = []
    count = 0

    # Parse output and add state nodes
    for line in out:
        if not line:
            continue

        line = line.split(" ")  # Split by spaces  
       

        if line[0] == "AP:":
            alphabets = line[2:]
            alphabets = [symbol.strip('"').strip(",") for symbol in alphabets] 
            wordset = alpha2wordset(alphabets)
            wordset = {('',) if item == () else item for item in wordset}
        
        elif line[0] == "--BODY--":
            in_body = True

        elif in_body and line[0] == "State:":
            current_state = line[1].strip()  # Ensure spaces are removed

            if len(line) > 2:
                state_colour = int(line[len(line)-1].strip("{}") )
                  
            try:
                    vertex = DPW.vs.find(name=current_state)
                    DPW.vs[vertex.index]['state'] = current_state
                    DPW.vs[vertex.index]['colour'] = int(state_colour)


            except (KeyError,ValueError):
                    DPW.add_vertex(name=current_state,state=current_state,colour=state_colour) 
    
        
        elif in_body and line[0] == "--END--":
            break

        elif in_body and line[0] != "State:":
            bool_value = False
            count = 0
            condition_parts = []
            inside_brackets = False

            for item in line:
                count += 1
                if "[" in item and "]" in item:
                    inside_brackets = False
                    condition_parts.append(item.strip("[]"))  # Remove brackets
                    continue
                elif "[" in item:  # Start recording condition
                    inside_brackets = True
                    condition_parts.append(item.strip("["))  # Remove left bracket
                    continue
                elif "]" in item:  # Stop recording condition
                    inside_brackets = False
                    condition_parts.append(item.strip("]"))  # Remove right bracket
                    continue
                elif inside_brackets:
                    condition_parts.append(item)
                elif not inside_brackets:
                    break

            condition = " ".join(filter(None, condition_parts))  # Remove empty strings
            next_state = line[count - 1]
            if next_state not in DPW.vs["name"]:
                DPW.add_vertex(name=next_state)
            condition = condition.replace("t","True").replace("f","False")
            condition = condition.replace("&", "and").replace("|", "or").replace("!", "not ")
            nums = list(map(int, re.findall(r'\d+', condition)))

            
    
            for w in wordset:
                    
                    con = condition
                    for num in nums:
                        
                        if alphabets[num] in w:
                            bool_value = 'True'
                        else: 
                            bool_value = 'False'

                        con = replace_number_with_bool(con, num, bool_value)

                    if eval(con):

                        DPW.add_edge(DPW.vs.find(name=current_state).index,DPW.vs.find(name=next_state).index,start=current_state,end=next_state,word=set(list(w)))
    return DPW  # Return the constructed DPW automaton

def drawdpw(DPW):
    """
    Draw the DPW automaton.
    """
    layout = DPW.layout('kamada_kawai')
    DPW.es['label'] = [word for word in DPW.es["word"]]
    DPW.vs['label'] = [f'q{v.index} ({v["colour"]})' for v in DPW.vs]
    visual_style = {}
    visual_style['layout'] = layout
    visual_style['bbox'] = (600, 600)
    visual_style['margin'] = 80
    visual_style['vertex_label_dist'] = 2
    visual_style['autocurve'] = True
    plot(DPW, **visual_style)
