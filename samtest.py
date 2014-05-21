from __future__ import with_statement # for python 2.5
__author__ = 'Rosen Diankov'

import time
from itertools import izip
import openravepy
if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

try:
    from multiprocessing import cpu_count
except:
    def cpu_count(): return 1

def check_object(obj):
    curr_target = []
    next_target = []
    
    for item in obj.graspables:
    	if 'mug' in str(item[0].target):
            #print item[0].target
            curr_target.append(item)
        else:
            next_target.append(item)
      
    return curr_target, next_target

def main(env,options):
    "Main example code."
    env.Load(options.scene)
    robot = env.GetRobots()[0]
    env.UpdatePublishedBodies()
    time.sleep(0.1) # give time for environment to update
    import grasp as gp
    robot_gp = gp.GraspPlanning(robot,randomize=options.randomize,nodestinations=options.nodestinations,plannername=options.planner)
    c_target,n_target = check_object(robot_gp)
    #sam: first grasp mug and place it
    #for t in c_target:
    #    success = robot_gp.graspAndPlaceObject(t[0], t[1])
    #sam: second grasp target, move to ashcan, place it
    for t in n_target:
        success, goals, graspindex = robot_gp.graspObject(t[0], t[1])
        import navig as ng
        robot_ng = ng.SimpleNavigationPlanning(robot)
        print 'Navigation planning '
        robot_ng.performNavigationPlanning()
        print 'goals', goals
        success = robot_gp.putObject(t[0], goals, graspindex)
    #robot_gp.performGraspPlanning(withreplacement=options.testmode)
    #robot_gp.performGraspPlanning(withreplacement=not options.testmode)   #sam repeat run
    time.sleep(5)
from optparse import OptionParser
from openravepy.misc import OpenRAVEGlobalArguments

@openravepy.with_destroy
def run(args=None):
    """Command-line execution of the example.

    :param args: arguments for script to parse, if not specified will use sys.argv
    """
    parser = OptionParser(description='Autonomous grasp and manipulation planning example.')
    OpenRAVEGlobalArguments.addOptions(parser)
    parser.add_option('--scene',
                      action="store",type='string',dest='scene',default='data/samtest2.env.xml',
                      help='Scene file to load (default=%default)')
    parser.add_option('--nodestinations', action='store_true',dest='nodestinations',default=False,
                      help='If set, will plan without destinations.')
    parser.add_option('--norandomize', action='store_false',dest='randomize',default=True,
                      help='If set, will not randomize the bodies and robot position in the scene.')
    parser.add_option('--planner',action="store",type='string',dest='planner',default=None,
                      help='the planner to use')
    (options, leftargs) = parser.parse_args(args=args)
    OpenRAVEGlobalArguments.parseAndCreateThreadedUser(options,main,defaultviewer=True)

if __name__ == "__main__":
    run()