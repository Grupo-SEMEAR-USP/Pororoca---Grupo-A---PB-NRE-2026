#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "pluginlib/class_list_macros.hpp"

class CustomMotorBridge : public hardware_interface::SystemInterface{
    public:
        hardware_interface::CallbackReturn on_init(const hardware_interface::HardwareComponentInterfaceParams & params) override{
            if(hardware_interface::SystemInterface::on_init(params) != CallbackReturn::SUCCESS) return CallbackReturn::ERROR;

            node_ = rclcpp::Node::make_shared("custom_motor_bridge");
            pub_ = node_->create_publisher<std_msgs::msg::Float64MultiArray>("motor_commands", 10);

            hw_commands_.resize(4, 0.0);
            hw_states_.resize(4, 0.0);

            return CallbackReturn::SUCCESS;
        }

        std::vector<hardware_interface::StateInterface> export_state_interfaces() override{
            std::vector<hardware_interface::StateInterface> state_interfaces;
            state_interfaces.emplace_back("front_left_wheel_joint", "velocity", &hw_states_[0]);
            state_interfaces.emplace_back("back_left_wheel_joint", "velocity", &hw_states_[1]);
            state_interfaces.emplace_back("front_right_wheel_joint", "velocity", &hw_states_[2]);
            state_interfaces.emplace_back("back_right_wheel_joint", "velocity", &hw_states_[3]);
            return state_interfaces;
        }

        std::vector<hardware_interface::CommandInterface> export_command_interfaces() override{
            std::vector<hardware_interface::CommandInterface> command_interfaces;
            command_interfaces.emplace_back("front_left_wheel_joint", "velocity", &hw_commands_[0]);
            command_interfaces.emplace_back("back_left_wheel_joint", "velocity", &hw_commands_[1]);
            command_interfaces.emplace_back("front_right_wheel_joint", "velocity", &hw_commands_[2]);
            command_interfaces .emplace_back("back_right_wheel_joint", "velocity", &hw_commands_[3]);
            return command_interfaces;
        }

        hardware_interface::return_type read(const rclcpp::Time &, const rclcpp::Duration &) override{
            hw_states_[0] = hw_commands_[0];
            hw_states_[1] = hw_commands_[1];
            hw_states_[2] = hw_commands_[2];
            hw_states_[3] = hw_commands_[3];
            return hardware_interface::return_type::OK;
        }

        hardware_interface::return_type write(const rclcpp::Time &, const rclcpp::Duration &) override{
            std_msgs::msg::Float64MultiArray msg;
            msg.data = {hw_commands_[0], hw_commands_[1], hw_commands_[2], hw_commands_[3]};
            pub_->publish(msg);
            rclcpp::spin_some(node_);
            return hardware_interface::return_type::OK;
        }

    private:
        rclcpp::Node::SharedPtr node_;
        rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr pub_;
        std::vector<double> hw_commands_;
        std::vector<double> hw_states_;
};

PLUGINLIB_EXPORT_CLASS(
  CustomMotorBridge,
  hardware_interface::SystemInterface
)