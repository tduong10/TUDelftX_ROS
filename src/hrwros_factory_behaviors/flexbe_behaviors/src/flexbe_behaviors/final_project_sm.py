#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_manipulation_states.srdf_state_to_moveit import SrdfStateToMoveit as flexbe_manipulation_states__SrdfStateToMoveit
from hrwros_factory_states.compute_grasp_state import ComputeGraspState
from hrwros_factory_states.control_feeder_state import ControlFeederState
from hrwros_factory_states.vacuum_gripper_control_state import VacuumGripperControlState
from hrwros_factory_states.locate_factory_device_state import LocateFactoryDeviceState
from hrwros_factory_states.detect_part_camera_state import DetectPartCameraState
from flexbe_states.subscriber_state import SubscriberState
from hrwros_factory_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as hrwros_factory_states__MoveitToJointsDynState
from hrwros_factory_states.set_conveyor_power_state import SetConveyorPowerState
from hrwros_factory_states.move_base_state import MoveBaseState as hrwros_factory_states__MoveBaseState
from hrwros_factory_states.srdf_state_to_moveit import SrdfStateToMoveit as hrwros_factory_states__SrdfStateToMoveit
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
from geometry_msgs.msg import Pose2D

# [/MANUAL_IMPORT]


'''
Created on @author: Timmy
@author: Timmy
'''
class FinalProjectSM(Behavior):
	'''
	Final project for the MOOC Hello (Real) World with ROS
The three robots in the factory move to process the parts
	'''


	def __init__(self):
		super(FinalProjectSM, self).__init__()
		self.name = 'Final Project'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		names1 = ['robot1_shoulder_pan_joint', 'robot1_shoulder_lift_joint', 'robot1_elbow_joint', 'robot1_wrist_1_joint', 'robot1_wrist_2_joint', 'robot1_wrist_3_joint']
		pick1_group = 'robot1'
		robot1_loc = Pose2D(x=3.8, y=2.2, theta=-90.0)
		gripper1 = "vacuum_gripper1_suction_cup"
		robot2_loc = Pose2D(x=-4.3, y=-0.9, theta=0.0)
		pick2_group = 'robot2'
		gripper2 = "vacuum_gripper2_suction_cup"
		names2 = ['robot2_shoulder_pan_joint', 'robot2_shoulder_lift_joint', 'robot2_elbow_joint', 'robot2_wrist_1_joint', 'robot2_wrist_2_joint', 'robot2_wrist_3_joint']
		# x:31 y:297, x:742 y:423
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.robot1_loc = robot1_loc
		_state_machine.userdata.pose_turtlebot = []
		_state_machine.userdata.pick1_configuration = []
		_state_machine.userdata.place1_configuration = []
		_state_machine.userdata.conveyor_speed = 100
		_state_machine.userdata.robot2_loc = robot2_loc
		_state_machine.userdata.pick2_configuration = []
		_state_machine.userdata.place2_configuration = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:13 y:113
			OperatableStateMachine.add('Move R1 Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Navigate to robot1', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1347 y:308
			OperatableStateMachine.add('Compute pick',
										ComputeGraspState(group=pick1_group, offset=0.0, joint_names=names1, tool_link=gripper1, rotation=3.1415),
										transitions={'continue': 'Activate Gripper R1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick1_configuration', 'joint_names': 'joint_names'})

			# x:1169 y:9
			OperatableStateMachine.add('Start feeder',
										ControlFeederState(activation=True),
										transitions={'succeeded': 'Wait for part', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1342 y:99
			OperatableStateMachine.add('Stop feeder',
										ControlFeederState(activation=False),
										transitions={'succeeded': 'stop conveyor', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1336 y:382
			OperatableStateMachine.add('Activate Gripper R1',
										VacuumGripperControlState(enable=True, service_name='/gripper1/control'),
										transitions={'continue': 'Move R1 to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:561 y:24
			OperatableStateMachine.add('Compute place Turtlebot',
										ComputeGraspState(group=pick1_group, offset=0.8, joint_names=names1, tool_link=gripper1, rotation=3.1415),
										transitions={'continue': 'Move R1 to place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_turtlebot', 'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:379 y:32
			OperatableStateMachine.add('LocateTurtlebot',
										LocateFactoryDeviceState(model_name='mobile_base', output_frame_id='world'),
										transitions={'succeeded': 'Compute place Turtlebot', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_turtlebot'})

			# x:1323 y:841
			OperatableStateMachine.add('Move R1 back Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Move R2 Home', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1339 y:240
			OperatableStateMachine.add('Detect Part Camera',
										DetectPartCameraState(ref_frame='robot1_base', camera_topic='/hrwros/logical_camera_1', camera_frame='logical_camera_1_frame'),
										transitions={'continue': 'Compute pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:1369 y:26
			OperatableStateMachine.add('Wait for part',
										SubscriberState(topic='/break_beam_sensor_change', blocking=True, clear=True),
										transitions={'received': 'Stop feeder', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:742 y:11
			OperatableStateMachine.add('Move R1 to place',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick1_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'start conveyor', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:948 y:8
			OperatableStateMachine.add('start conveyor',
										SetConveyorPowerState(stop=False),
										transitions={'succeeded': 'Start feeder', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'speed': 'conveyor_speed'})

			# x:1338 y:171
			OperatableStateMachine.add('stop conveyor',
										SetConveyorPowerState(stop=True),
										transitions={'succeeded': 'Detect Part Camera', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'speed': 'conveyor_speed'})

			# x:205 y:59
			OperatableStateMachine.add('Navigate to robot1',
										hrwros_factory_states__MoveBaseState(),
										transitions={'arrived': 'LocateTurtlebot', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'robot1_loc'})

			# x:1313 y:762
			OperatableStateMachine.add('Deactivate gripper 1',
										VacuumGripperControlState(enable=False, service_name='/gripper1/control'),
										transitions={'continue': 'Move R1 back Home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1351 y:448
			OperatableStateMachine.add('Move R1 to pick',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick1_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'Move R1 PreGrasp', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick1_configuration', 'joint_names': 'joint_names'})

			# x:1007 y:842
			OperatableStateMachine.add('navigate to robot2',
										hrwros_factory_states__MoveBaseState(),
										transitions={'arrived': 'Detect Part Camera_R2', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'robot2_loc'})

			# x:839 y:839
			OperatableStateMachine.add('Detect Part Camera_R2',
										DetectPartCameraState(ref_frame='robot2_base', camera_topic='/hrwros/logical_camera_2', camera_frame='logical_camera_2_frame'),
										transitions={'continue': 'Compute pick_R2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:685 y:836
			OperatableStateMachine.add('Compute pick_R2',
										ComputeGraspState(group=pick2_group, offset=0.0, joint_names=names2, tool_link=gripper2, rotation=3.1415),
										transitions={'continue': 'Activate Gripper R2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick2_configuration', 'joint_names': 'joint_names'})

			# x:307 y:840
			OperatableStateMachine.add('Move R2 to pick',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick2_group, offset=0.0, tool_link=gripper2, action_topic='/move_group'),
										transitions={'reached': 'Move R2 Home_2', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick2_configuration', 'joint_names': 'joint_names'})

			# x:487 y:839
			OperatableStateMachine.add('Activate Gripper R2',
										VacuumGripperControlState(enable=True, service_name='/gripper2/control'),
										transitions={'continue': 'Move R2 to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1344 y:566
			OperatableStateMachine.add('Move R1 Home_2',
										hrwros_factory_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Compute place Turtlebot_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1323 y:696
			OperatableStateMachine.add('Move R1 to place_2',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick1_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'Deactivate gripper 1', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:1307 y:631
			OperatableStateMachine.add('Compute place Turtlebot_2',
										ComputeGraspState(group=pick1_group, offset=0.6, joint_names=names1, tool_link=gripper1, rotation=3.1415),
										transitions={'continue': 'Move R1 to place_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_turtlebot', 'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:1342 y:505
			OperatableStateMachine.add('Move R1 PreGrasp',
										hrwros_factory_states__SrdfStateToMoveit(config_name='R1PreGrasp', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Move R1 Home_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:95 y:817
			OperatableStateMachine.add('Move R2 Home_2',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R2Home', move_group=pick2_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Move R2Place', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:30 y:721
			OperatableStateMachine.add('Move R2Place',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R2Place', move_group=pick2_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Deactivate Gripper R2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1150 y:847
			OperatableStateMachine.add('Move R2 Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R2Home', move_group=pick2_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'navigate to robot2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:34 y:486
			OperatableStateMachine.add('Move R2 back Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R2Home', move_group=pick2_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:22 y:588
			OperatableStateMachine.add('Deactivate Gripper R2',
										VacuumGripperControlState(enable=False, service_name='/gripper2/control'),
										transitions={'continue': 'Move R2 back Home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
