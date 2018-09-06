#include "sys/types.h" // struct sysinfo
#include "sys/sysinfo.h" // sysinfo
#include <iostream> // cout, cin, 
#include <stdlib.h>	//system
#include "exec.hpp" //std::string exec(const char* cmd);
#include "BlackGPIO.h"
/**
Caculate de memory percentage that is been in use by the system 
@return percentage in a range of 0 to 1.
**/ 

struct sysinfo memInfo;
double memoryPercentage(){
	sysinfo (&memInfo);
	unsigned long physMemUsed = memInfo.totalram - memInfo.freeram;
	double percentage = physMemUsed/(memInfo.totalram * (1.0));
	return percentage;
}

using namespace BlackLib;
int main(){
	BlackGPIO green(GPIO_67, output, FastMode);
	BlackGPIO yellow(GPIO_68, output, FastMode);
	BlackGPIO red(GPIO_44, output, FastMode);
	BlackGPIO   button(GPIO_60, input, SecureMode);       
	while(true){
		double percentage = memoryPercentage();
		std::cout<<"Memory Usage: "<< percentage * 100 << "%" << std::endl;
		green.setValue(low);
		yellow.setValue(low);
		red.setValue(low);
		if(percentage < 0.25){
			green.setValue(high);
		}else if(percentage < 0.5){
			yellow.setValue(high);
		}else if(percentage < 0.75){
			red.setValue(high);
		}else{
			green.setValue(high);
			yellow.setValue(high);
			red.setValue(high);
			if(stoi(button.getValue())){
				std::string s_pid;
				s_pid = exec("ps aux --sort=-%mem | sed -n \'2p\'| cut -d\' \' -f8");
				std::string kill = "kill -9 " + s_pid;
				system(kill.c_str());
			}
		}
		sleep(1);
	}
}