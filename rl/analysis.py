# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.01
    return answerDiscount, answerNoise

def question3a():
    # answerLivingReward cannot be positive, or pacman won't take risk and run forever. 
    # answerLivingReward cannot be a large negative number, or pacman will go for +10 exit. 
    # Set answerDiscount and answerLivingReward to a relatively small number, which prevents
    # pacman from going to +10 exit. 
    # and set answerNoise to 0.0, under which situation pacman can ignore the risk of -10 cliff and 
    # take the shortest path to +1 exit. 
    answerDiscount = 0.5
    answerNoise = 0
    answerLivingReward = -3.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    # 'not risking the cliff' means there exists risks, so the answerNoise here cannot be 0.0.
    # answerLivingReward cann ot be too large also, or pacman may want to exit the game 
    # as soon as possible, it will jump into cliff or take risking path. 
    # Under the situation described above, answerDiscount should be moderate, or pacman will
    # go straight towards +10 exit. 
    answerDiscount = 0.5
    answerNoise = 0.4
    answerLivingReward = -3.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    # Since pacman wants to go to +10 exit, the answerDiscount should be large enough to slow down
    # the decay of rewards. 
    # The same as 3a, set answerNoise to 0.0, which enables pacman to ignore uncertainty and takes
    # shortest path to +10 exit. 
    # Here I also set answerLivingReward to a small negative number, so in comparison with the +10 
    # exit reward, pacman can almostly ignore the negative answerLivingReward impact. 
    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    # Since pacman doesn't want to risk the cliff, it means there exists uncertainty. So a large answerNoise
    # can scare the pacman away from the risking path along cliff. 
    # The selection for answerDiscount and answerLivingReward is the same as 3c. 
    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    # Since it is a forever running pacman, answerLivingReward should be positive, the other two 
    # parameters seem useless here. So I set them all to 0.0.
    answerDiscount = 0.0
    answerNoise = 0.0
    answerLivingReward = 2
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    return 'NOT POSSIBLE'
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
