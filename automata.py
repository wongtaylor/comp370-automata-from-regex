import sys


# Abstract Syntax Tree
class AST: 
    def __init__(self, value, l_child, r_child, node_type):
        self.val = value
        self.l_child = l_child
        self.r_child = r_child
        self.parent = self
        self.node_type = node_type
    
    def get_left(self):
        return self.l_child
        
    def get_right(self):
        return self.r_child
        
    def get_parent(self):
        return self.parent
    
    
class NFA:
    
    def __init__(self, n_states, alphabet, start_state, accept_states):
        self.start_state = start_state
        self.n_states = n_states
        self.alphabet = alphabet
        self.accept_states = accept_states
        self.trans_set = []
        self.closure_trans = []
	self.states = []

    def get_start_state(self):
        return self.start_state
        
    def get_n_states(self):
        return self.n_states

    def get_alphabet(self):
        return self.alphabet

    def get_accept_states(self):
        return self.accept_states

    def get_trans_set(self):
        return self.trans_set

    def add_transition(self, trans):
        self.trans_set.append(trans)

    def add_closure_trans(self, transition):
        self.closure_trans.append(transition)

    def get_closure_trans(self):
        return self.closure_trans


def renumber(transitions, factor):
    '''''
    renumber: renumbers transitions so that concat, union, and star NFA's can be made 
    	@param: transitions is a set of transitions in the form of tuples
	@param factor is the amount you are shifting the state numbers by
	@returns the new set of transitions'
    '''
    ret_trans = []
    for trans in transitions:
        qa = trans[0]
        qb = trans[2]
        new_trans = (qa+factor, trans[1], qb+factor)
	ret_trans.append(new_trans)
    return ret_trans


def concat(n1, n2):
    '''
    concat: performs the operatoins associated with the concat function 
    	@param n1, n2 are nfa machines
	@returns new updated nfa with appropriate state numbers
    '''
    # create final alphabet with symbols from both nfa alphabets
    alpha = []
    alpha.append(n1.get_alphabet())
    for a in n2.get_alphabet():
	if a not in alpha:
	    alpha.append(a)
    num_states = n1.n_states + n2.n_states 

    # create accept states set
    final_accept_states = []
    for accept in n2.get_accept_states():
	final_accept_states.append(accept+n1.n_states)

    # create new nfa with combined attributes
    new_nfa = NFA(num_states, alpha, n1.get_start_state(), final_accept_states)
    
    # create transition set with both n1 and n2 trans_set
    final_trans_set = []	       
    trans2 = []
    trans2 = renumber(n2.get_trans_set(), n1.n_states)
    for trans in n1.get_trans_set():
	final_trans_set.append(trans)
    for trans in trans2:
        final_trans_set.append(trans)
       
    # add epsilon transition from accept state of n1 to start state of n2
    for a in n1.get_accept_states():
        trans_tuple = (a, 'e', n2.get_start_state()+n1.n_states)
        final_trans_set.append(trans_tuple)
        
    new_nfa.trans_set = final_trans_set
    
    return new_nfa
    
    
def union(n1, n2):
    '''
    union: performs the operatoins associated with the union function 
    	@param n1, n2 are nfa machines
	@returns new updated nfa with appropriate state numbers
    '''
    # create final alphabet with symbols from both nfa alphabets
    alpha = []
    alpha.append(n1.get_alphabet())
    for a in n2.get_alphabet():
        if a not in alpha:
	    alpha.append(a)
    num_states = n1.n_states + n2.n_states + 1
   
    # create final accept states set from nfa n1 and n2
    final_accept_states = []
    for fin in n1.get_accept_states():
    	final_accept_states.append(fin+1)
    for fin in n2.get_accept_states():
	final_accept_states.append(fin+n1.n_states+1)
    
    # create new nfa 
    new_nfa = NFA(num_states, alpha, 1, final_accept_states)
    
    # create transition set with both n1 and n2 trans_set
    final_trans_set = []
    trans1 = []
    trans1 = renumber(n1.get_trans_set(), 1)
    trans2 = []
    trans2 = renumber(n2.get_trans_set(), n1.n_states+1)
    for trans in trans1:
	final_trans_set.append(trans)
    for trans in trans2:
        final_trans_set.append(trans)
    
    # add elpsilon transition from new start state to start states of n1 and n2
    final_trans_set.append((1, 'e', n1.get_start_state()+1))
    final_trans_set.append((1, 'e', n2.get_start_state()+n1.n_states+1))
        
    new_nfa.trans_set = final_trans_set
    
    return new_nfa


def star(n1):
    '''
    star: performs the operatoins associated with the star function 
    	@param n1 is an nfa machines
	@returns new updated nfa with appropriate state numbers
    '''
    alpha = []
    alpha.append(n1.get_alphabet())
    num_states = n1.n_states + 1
    
    # create final accept states for new nfa machine 
    final_accept_states = []
    for fin in n1.get_accept_states():
    	final_accept_states.append(fin+1)
    
    # create new nfa 
    new_nfa = NFA(num_states, alpha, 1, final_accept_states)
    
    # create final transition set
    final_trans_set = []
    trans1 = []
    trans1 = renumber(n1.get_trans_set(), 1)
    for trans in trans1:
        final_trans_set.append(trans)
    
    # add epsilon transition from new start state to n1 start state
    final_trans_set.append((1, 'e', n1.get_start_state()+1))
    
    # add epsilon transitions from n1 accept states to n1 start state
    for a in n1.get_accept_states():
        final_trans_set.append((a+1, 'e', n1.get_start_state()+1))
   
    # add epsilon transition from new start state to accept states
    for a in new_nfa.get_accept_states():
    	final_trans_set.append((1, 'e', a))

    new_nfa.trans_set = final_trans_set
    
    return new_nfa
    

def init_single_nfa(symbol):
    '''
    init_single_nfa: creates an nfa with one state on a single symbol
    NFA: state 1 --symbol--> state 2
    '''
    # initialize an nfa with two states
    new_nfa = NFA(2, symbol, 1, [2])
    new_nfa.states = [1,2]
    
    # add single transition to trans_set
    trans_set = []
    trans_tuple = (1, symbol, 2)
    trans_set.append(trans_tuple)
    
    # set trans_set to the trans_set of new_nfa
    new_nfa.trans_set = trans_set
    
    return new_nfa


class DFA:

    def __init__(self, alphabet, start_state, accept_states):
        self.states = None
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = []
        self.trans_set = []
	
    def set_n_states(self, num_states):
        self.states = num_states

    def get_n_states(self):
        return self.states

    def add_transition(self, trans):
        self.trans_set.append(trans)

    def get_trans_set(self):
        return self.trans_set

    def add_accept_states(self, new_accept_state):
        self.accept_states.append(new_accept_state)

    def get_accept_states(self):
        return self.accept_states

    def get_alphabet(self):
        return self.alphabet

    def get_start_state(self):
        return self.start_state

    def set_start_state(self, new_start_state):
        self.start_state = new_start_state


class operator():

    def __init__(self, operator):
        self.operator = operator
        if operator == '*': # star
            self.value = 3
        elif operator == '|': # union
            self.value = 1
        elif operator == '@': # concat
	    self.value = 2
	else: # parentheses
	    self.value = 0


def parse(reg_expr):
    '''
    Parse method goes through and adds operators to the operator stack,
    keeping in mind order of precedence, and adds operands to the operand
    stack. Once you have gone through the whole reg_expr array, pop from
    the operator stack and pop twice from the operand stack, creating a
    syntax tree as you go, until the operator stack is empty.
        @param: reg_expr is an array holding the regular expression read in
        @returns root which is the syntax tree
    '''
    # initialize empty stacks for operands and operators
    operand_stack = []
    operator_stack = []
    right_paren_scanned = False
    previous = -1

    # index through reg_expr held in an array
    for a in reg_expr:
	if previous != -1:
            if (a == '(' and identify(previous) == 0) or (a == '(' and previous == ')'):
	        operator_stack.append('@')
	if a == '(' and previous != '*':
	    operator_stack.append(a)
	    previous = a
	    continue
	if a == ' ': # ignore white spaces
	    continue
	identity = identify(a)
	
	if identity == 1: # operator scanned
            if a == ')':
	    	right_paren_scanned = True
	    if not operator_stack: # stack is empty
	    	operator_stack.append(a)
		previous = a
		continue
	    
	    # check if you need to push directly or pop then push
	    while operator_stack:
            	if a == '(' or a == '*':
		    check_type(a, previous, operator_stack, operand_stack) # adds implied concat to stack if necessary
                val = check_precedence(a, operator_stack)
		if val == 1: # push
                    operator_stack.append(a)
		    previous = a
		    break
	    	
		while operator_stack and val == 0: # pop
                    popped_operator = operator_stack.pop()
		    # if ')' is scanned, pop until you pop '(' and then break out of loop
		    if popped_operator == '(': 
		    	right_paren_scanned = False
			break     
                    update_nfa(popped_operator, operand_stack)
                    val = check_precedence(a, operator_stack)
		if val == 1: # push
                    operator_stack.append(a)
		    previous = a
		# end while - top of stack operator is less than current operator (a)
		break
	
	else: # operand scanned 
	    if operand_stack or operator_stack:
	    	check_type(a, previous, operator_stack, operand_stack) # adds implied concat to stack if necessary
            simple_nfa = init_single_nfa(a)
            operand_stack.append(simple_nfa)
	previous = a

    # go through regular expression, pop operators left on stack
    while operator_stack:
        popped_operator = operator_stack.pop()
        update_nfa(popped_operator, operand_stack)
    
    # pop root final NFA)
    root = operand_stack.pop()
    return root    
            
            
def update_nfa(a, stack):    
    '''
    update_dfa: takes in an operator and a stack (operand)
    adds the nfa resulting from the operator to the stack
    '''
    if not stack:
        print("Operand stack is empty", stack)
    	exit(1)
    if a == '*':
        new_nfa = star(stack.pop())
    elif a == '|':
        r_nfa = stack.pop()
        if not stack:
            print("Operand stack is empty", stack)
    	    exit(1)
	l_nfa = stack.pop()
        new_nfa = union(l_nfa, r_nfa)
    else: #concat
	r_nfa = stack.pop()
        if not stack:
            print("Operand stack is empty", stack)
    	    exit(1)
        l_nfa = stack.pop()
        new_nfa = concat(l_nfa, r_nfa)  
    
    stack.append(new_nfa)

        
def check_type(a, previous, operator_stack, operand_stack):
    '''
    check_type: adds implied concat when necessary
        checks the type of the operator that is to be put on the stack 
	handles concat operator and add in  '@' for char or ')' 
        followed by another char, '(', or star
    	@param a is the current symbol scanned
	@param previous is the last symbol scanned
	@param operator_stack is the operator stack
	@param operand_stack is the operand stack
    '''

    if identify(a) == 0 or a == '(': # operand/char
        if previous == ')' or identify(previous) == 0 or previous == '*':
    	    # check to see if the precedence of top of stack is greater than '@'
	    if operator_stack:
	    	# peek at the top of stack
		top = operator_stack.pop()
	    	operator_stack.append(top)
	    	if top != '(' and top != '@': 
	            while check_precedence('@', operator_stack) == 0:
	                update_nfa(operator_stack.pop(), operand_stack)
	    operator_stack.append('@')

        
def identify(a):
    '''
    Identify method determines if 'a' is an operator or operand
        @param 'a' is an element in the array (reg_expr)
        @returns '1' for an operator or '0' for an operand
    '''
    if a == '*' or a == '|' or a == '(' or a == ')':
        return 1 # operator
    else:
        return 0 # operand


def check_precedence(operator_to_be_pushed, stack):
    '''
    check_precedence method determines if the operator that was just scanned
    has greater precedence than the operator currently on top of the stack
        @param operator_to_be_pushed is the operator just scanned
        @param stack is the operator stack
        @returns '1' if the operator to be pushed has greater precedence than
        the operator on top of the stack, otherwise returns '0'
    '''
    if not stack:
    	return 1
    else:
    	top_of_stack = stack.pop()
	stack.append(top_of_stack)
    	top_operator = operator(top_of_stack)
    	curr_operator = operator(operator_to_be_pushed)
    
    	if operator_to_be_pushed == '(':
            return 1
    	else:
            if curr_operator.value > top_operator.value:
                return 1 # want to push
            else: # curr_operator <= top_operator
                return 0 # pop
        

def closure(NFA, start_state):
    '''
    Closure method: For given start_state, follow the epsilon transitions all the way through 
    and add the new qb states to the final_set 
        Params: NFA is the NFA machine and start_state is the beginning start state (qa state)
        Return final set which is the set where start_state can get to on epsilon transitions.
    '''
    
    final_set = []
    track = [start_state]
    
    # Run a DFS, if a state can be reached via epsilon, push onto stack and continue
    while track:
        state = track.pop()
        for move in NFA.get_trans_set():
            if (move[0] == state) and (move[1] == 'e') and ((move[2] not in final_set) and (move[2] != start_state)):
                track.append(move[2])
                final_set.append(move[2])
    return final_set


def init_NFA(NFA, state, alphabet):
    '''
    init_NFA: takes state and goes through the alphabet, appending qb states 
    to final set of qb states if there exists a state and symbol already defined.
        @param NFA is the NFA machine, state is the qa state
        @param alphabet is the set of symbols
        @returns final set which is set a specified state on a specified symbol can get to
    ''' 
    # Append normal trans_set for each symbol in the alphabet
    final = [state, []]
    final[1].append(('e', closure(NFA, state)))
    
    # for each letter in the alphabet create the places that it can get to
    for symbol in alphabet:
        results = []
        for transition in NFA.get_trans_set():
            if (transition[0] == state) and (transition[1] == symbol):
                results.append(transition[2])
        # append current set to add new qb state
        final[1].append((symbol, results))
    return final


def move(NFA, new_state, symbol):
    '''
    Move: Finds all the states the new_state can get to on the specified symbol.
        Params: NFA is the NFA machine, new_state is the start state (which can be a set of states)
        and symbol is the input symbol in the alphabet
        Returns new_set which is the set of qb states new_state can get to on symbol
    '''

    # new set is the set that state_at can get to on symbol
    new_set = []
    state_at = [new_state]
    for transition in NFA.get_trans_set():
        for state in state_at:
            if (transition[0] == state) and (transition[1] == symbol):
                new_set.append(transition[2])
    
    new_set.sort() 
    return new_set
        
        
def init_DFA(NFA, NFA_start_state):
    '''
    init_DFA: uses information from NFA machine to build a new DFA machine. Keeps track of states 
    to be be handed in states_queue and assigns the "id's" of the set of states to be the state you 
    can transition to or from.
        Params: NFA is the NFA machine, NFA_start_state is the beginning state of the DFA machine
        Returns newDFA which is the initialized new DFA machine
    '''

    new_trans = []
    new_accept = []
    start = NFA.get_closure_trans()[NFA_start_state-1]
    start_state = [NFA_start_state]
    for transition in start[1]:
        if transition[0] == 'e':
            start_state.extend(transition[1])
    start_state.sort()
    new_states = [start_state]
    # state_stack adds states to be handled and pops states that are handled using FIFO strategy
    # tried queue but realized that a stack would work better for what we are trying to do
    states_stack = [start_state]
    
    newDFA = DFA(NFA.get_alphabet(), NFA_start_state, None)
    
    while states_stack: # while there are still states in stack
        state_to_be_handled = states_stack.pop()
        for letter in NFA.get_alphabet():
            results = []
            # go through each letter in the alphabet to see where the nfa can go 
            # save where the nfa can to a list to be set as a transtion state for the dfa
            for state in state_to_be_handled:
                closure_trans = NFA.get_closure_trans()[state-1]
                for trans in closure_trans[1]:
                    if trans[0] == letter:
                        for x in trans[1]:
                            if x not in results:
                                # append results
                                results.append(x)
                                x_closure = NFA.get_closure_trans()[x-1]
                                # check the closure of the new results
                                for y_closure in x_closure[1][0][1]:
                                    if y_closure not in results:
                                        # append results
                                        results.append(y_closure)
                
            # sort the results so that we can see if they are used in the dfa
            results.sort()
            dfa_trans = (state_to_be_handled, letter, results)
            new_trans.append(dfa_trans)
            # check to see if the results set is already defined as a state
            if (results not in new_states) and (results != state_to_be_handled):
                states_stack.append(results)
                new_states.append(results)

     
    # set id of dfa transitions
    for b in new_trans:
        temp = (new_states.index(b[0]) + 1, b[1], new_states.index(b[2]) + 1)
        newDFA.add_transition(temp)
    
    # define accepting states in dfa
    for a in new_states:
        for accept in NFA.get_accept_states():
            if accept in a:
                newDFA.add_accept_states(new_states.index(a) + 1)

    # set n states to length of new_states
    newDFA.set_n_states(len(new_states))
    # set the start state of dfa to correct id
    newDFA.set_start_state(new_states.index(start_state) + 1)
    return newDFA
    

def validate_expr(str, alphabet):
    '''
    validate_expr: takes in a string and the alphabet to make sure that
    the string is formatted properly
    	@param str is the regular expression
	@param alphabet is the valid symbols in the language
	@returns check which is 1 if invalid and 0 if valid
    '''

    reg_expr = str
    expr_stack = []
    check = 0
    first_letter_check = 0
    left_paren_scanned = False
    previous_thing =[' ',' ']
    
    for expr in reg_expr:
        if expr == ' ':
            continue
	thing = previous_thing.pop()
        if expr == '(':
	    first_letter_check += 1
	    left_paren_scanned = True
            expr_stack.append('(')
        elif expr == ')':
	    first_letter_check += 1
	    if left_paren_scanned == False and not expr_stack:
                print("invalid expression - ) with no matching (.")
                check = 1
            else:
                expr_stack.pop()
	        left_paren_scanned = False
        elif expr == 'e' or expr == ' ':
	    first_letter_check += 1
        elif expr == '*' or expr == 'N' or expr == '|': 
	    if first_letter_check == 0 or thing == expr:
                print("invalid expression: double special character")
		check = 1
	elif expr in alphabet:
	    first_letter_check += 1
        else:
            print("invalid expression character is not in the alphabet.")
            check = 1
        previous_thing.append(expr)
    if expr_stack:
        print("invalid expression - ( found with no matchin ).")
        exit(1)
        
    return check


def run_DFA(DFA, inputs, output_file):
    '''
    run_DFA: takes in a DFA, the inputs from the input file, and the output file 
    for the results to be written to
    return: closes the file upon success of writing to the file, exits if a string
    contains letters not in the alphabet
    '''
    
    # print results to specified output file
    ofp = open(output_file, 'w')
    # go through each input in the inputs array
    for input in inputs:
        state = DFA.get_start_state()
        # go through each letter in the input string

        for letter in input:
            # make sure letter is in alphabet
            if letter not in DFA.get_alphabet():
                print("Character " + repr(letter) + " not in alphabet")
                exit(1)
            state = find_next(state, letter, DFA)
	    if state == -1:
	    	break

	# write whether the string is in the language or not to the file
        if state in DFA.get_accept_states():
	    ofp.write("True\n")
        else:
            ofp.write("False\n")
    
    ofp.close()


def find_next(state, letter, DFA):
    '''
    find_next: takes in a state, letter (symbol) in the alphabet, and DFA 
    return: returns the state that the DFA can get to on that letter
    '''
    for move in DFA.get_trans_set():
    # find the state that the letter gets you to, and then continue in the loop
        if(move[0] == state) and (move[1] == letter):
            return move[2]
    # got through without returning 
    return -1
            
            
def main(argv=sys.argv):

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # try to open file
    try:
        ifp = open(input_file, 'r')
    except IOError:
        print("File not found. Please check to make sure that the file exists/path is correct")
        exit(1)

    # read in alphabet 
    alphabet = []
    lines = ifp.read().splitlines()
    al = str(lines[0])
    for character in range(len(al)):
        alphabet.append(al[character])
    
    # reads the regular expression and parses the string into an array
    reg_expr_str = lines[1]
    reg_expr = []
    for expr in reg_expr_str:
        reg_expr.append(expr)
    
    inputs = []
    for thing in range(2, len(lines)):
        inputs.append(lines[thing])

    # check to see if the regualr expression is in the proper format, if not - exit
    check = validate_expr(reg_expr, alphabet)
    if check == 1:
        ofp = open(output_file, 'w')
        ofp.write("Invlaid expression\n")
        ofp.close()
        exit(1)
    
    # 1) scan reg expr and parse - creating nfa by using two stacks
    nfa = parse(reg_expr)    
     
    # calls closure on NFA transitions and adds them to the closure set of transitions
    for state in range(1, nfa.get_n_states() + 1):
        nfa.add_closure_trans(init_NFA(nfa, state, alphabet))
    nfa.alphabet = alphabet
    
    # 2) convert nfa to dfa --> build the dfa from the nfa
    dfa = init_DFA(nfa, nfa.get_start_state())
    
    # 3) Simulate DFA and determine if each string is in the language, printing accept or reject
    run_DFA(dfa, inputs, output_file)
 

if __name__ == "__main__":
    sys.exit(main())
        
