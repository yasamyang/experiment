import testr
import testg
import time

def run():
    parser = testg.OptionParser(description='Autonomous grasp and manipulation planning example.')
    parser.add_option('--scene',
                      action="store",type='string',dest='scene',default='/home/user/experiment/data/lab1.env.xml',
                      help='Scene file to load (default=%default)')
    parser.add_option('--nodestinations', action='store_true',dest='nodestinations',default=False,
                      help='If set, will plan without destinations.')
    parser.add_option('--norandomize', action='store_false',dest='randomize',default=True,
                      help='If set, will not randomize the bodies and robot position in the scene.')
    (options, args) = parser.parse_args()
    env = testg.Environment()
    try:
        env.SetViewer('qtcoin')
        env.Load(options.scene)
        robot = env.GetRobots()[0]
        env.UpdatePublishedBodies()
        time.sleep(0.1) # give time for environment to update
        SNP = testr.SimpleNavigationPlanning(robot)
        SNP.performNavigationPlanning()
        GP= testg.GraspPlanning(robot,randomize=options.randomize,nodestinations=options.nodestinations)
        GP.performGraspPlanning()
        SNP = testr.SimpleNavigationPlanning(robot)
        SNP.performNavigationPlanning()
        
    finally:
        env.Destroy()

if __name__ == "__main__":
    run()
