#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
#include <list>
#include <sstream>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
            result += buffer.data();
    }
    return result;
}

void getChildsIDS(std::list<pid_t>& result, pid_t pid = 1){
	std::string cmd = "pgrep -P " + std::to_string(pid);
	std::string r = exec(cmd.c_str());
	std::istringstream iss(r);
	std::string line;
	while (std::getline(iss, line))
	{
    	result.push_back(std::stoi(line));
	}
}
void tree(pid_t pid, int depth = 0){
	using std::cout;
	using std::endl;
	std::string cmd = "ps -p " +  std::to_string(pid) + " -o comm=";
	std::string out = exec(cmd.c_str());
	if(out.size() > 0)
		out.erase(out.end() - 1);
	std::list<pid_t> pids;
	getChildsIDS(pids, pid);
	for (int i = 0; i < depth; ++i)
	{
		cout<<"\t";
	}
	if(pids.size() == 0){
		cout<< pid << " " << out <<endl;
	}else{
		cout<< pid << " " << out <<endl;
		for (int i = 0; i < depth; ++i)
		{
			cout<<"\t";
		}
		cout<<"<childs>"<<endl;
		for(pid_t p: pids){
			tree(p, depth + 1);
		}
		for (int i = 0; i < depth; ++i)
		{
			cout<<"\t";
		}
		cout<<"</childs>"<<endl;
	}
}

int main(int argc, char const *argv[])
{
	if(argc == 2){	
		tree(atoi(argv[1]));
	}
	return 0;
}