# coding=utf-8
from collections import deque, namedtuple

automaton = []
# state_id: int, value: char, goto: dict, failure: int, output: set
Node = namedtuple("Node", "state value goto failure output")


def init_trie(words):
    """
    creates an AC automaton, firstly create an empty trie, then add words to the trie
    and sets fail transitions
    """
    create_empty_trie()
    map(add_word, words)
    set_fail_transitions()


def create_empty_trie():
    """ initialize the root of the trie """
    automaton.append(Node(0, '', {}, 0, set()))


def add_word(word):
    """add word into trie"""
    node = automaton[0]
    for char in word:
        # char is not in trie
        if goto_state(node, char) is None:
            next_state = len(automaton)
            node.goto[char] = next_state  # modify goto(state, char)
            automaton.append(Node(next_state, char, {}, 0, set()))
            node = automaton[next_state]
        else:
            node = automaton[goto_state(node, char)]
    node.output.add(word)


def goto_state(node, char):
    """goto function"""
    if char in node.goto:
        return node.goto[char]
    else:
        return None


def set_fail_transitions():
    """construction of failure function, and update the output function"""
    queue = deque()
    # initialization
    for char in automaton[0].goto:
        s = automaton[0].goto[char]
        queue.append(s)
        automaton[s] = automaton[s]._replace(failure=0)
    while queue:
        r = queue.popleft()
        node = automaton[r]
        for a in node.goto:
            s = node.goto[a]
            queue.append(s)
            state = node.failure
            # failure transition recursively
            while goto_state(automaton[state], a) is None and state != 0:
                state = automaton[state].failure
            # except the chars in goto function, all chars transition will goto root node self
            if state == 0 and goto_state(automaton[state], a) is None:
                goto_a = 0
            else:
                goto_a = automaton[state].goto[a]
            automaton[s] = automaton[s]._replace(failure=goto_a)
            fs = automaton[s].failure
            automaton[s].output.update(automaton[fs].output)


def search_result(strings):
    """AC pattern matching machine"""
    result_set = set()
    node = automaton[0]
    for char in strings:
        while goto_state(node, char) is None and node.state != 0:
            node = automaton[node.failure]
        if node.state == 0 and goto_state(node, char) is None:
            node = automaton[0]
        else:
            node = automaton[goto_state(node, char)]
        if len(node.output) >= 1:
            result_set.update(node.output)
    return result_set


init_trie(['1', '2', '3', '456', '37'])

x = search_result("32137456")
for xx in x:
    print xx.decode('utf-8')
