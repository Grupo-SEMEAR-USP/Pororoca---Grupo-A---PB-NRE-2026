from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path

def generate_launch_description():
    wallington_description_dir = get_package_share_directory("wallington_description")

    #Coloca o arquivo de descrição do robô como argumento, caso a gente for testar coisas novas e diferentes
    model_arg = DeclareLaunchArgument( 
        name="model",
        default_value=os.path.join(wallington_description_dir, "urdf", "wallington.urdf.xacro"),
        description="Caminho absoluto ate o arquivo de configuração do modelo do robo"
    )

    #Coloca o mundo em que o robô vai ser gerado como argumento
    world_arg= DeclareLaunchArgument( 
        name="world",
        default_value= os.path.join(wallington_description_dir, "worlds", "blank_world.sdf"),
        description="Caminho absoluto até o mundo em que o robo sera carregado"
    )

    #Roda um comando do OS para interpretar o xacro do modelo
    robot_description = ParameterValue(
        Command([
            "xacro ",
            LaunchConfiguration("model")
        ]),
        value_type=str
    )

    robot_state_publisher = Node(
        package= "robot_state_publisher",
        executable= "robot_state_publisher",
        parameters= [{"robot_description": robot_description}]
    )

    #Bom declarar onde o simulador está rodando, bem como todos os pacotes ao redor
    gazebo_resource_path = SetEnvironmentVariable( 
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(wallington_description_dir).parent.resolve())]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
        launch_arguments=[("gz_args", [" -v 4", " -r ", LaunchConfiguration("world")])]
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description",
                    "-name", "wallington"]
    )

    #IMPORTANTE: NÃO ESQUECER DE DECLARAR NOVOS NÓS DE INTERAÇÃO AQUI!!!!
    gz_bridge = Node( 
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/camera@sensor_msgs/msg/Image[gz.msgs.Image'
        ],
        remappings=[
            
        ],
        parameters=[{
            "qos_overrides./tf_static.publisher_durability": "transient_local"
        }],
        output="screen"
    )

    return LaunchDescription([
        model_arg,
        world_arg,
        robot_state_publisher,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity,
        gz_bridge
    ])