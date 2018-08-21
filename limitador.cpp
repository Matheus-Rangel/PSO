#include <array>
#include <stdio.h>
#include <string>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/resource.h>
#include <iostream>
#include <memory>
#include <sstream>

int NUM_PROC;
int getrlimit(int resource, struct rlimit *rlim);
int setrlimit(int resource, const struct rlimit *rlim);
int prlimit(pid_t pid, int resource, const struct rlimit *new_limit, 
			struct rlimit *old_limit);

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

int limit(std::string uid, rlimit *limiteProc){
	std::string cmd = "pgrep -u" + uid;
	std::string s = exec(cmd.c_str());
	std::istringstream iss(s);
	std::string line;
	while (std::getline(iss, line))
	{
    	prlimit((pid_t)stoi(line), RLIMIT_NPROC, limiteProc, nullptr);
	}
	std::cout<< "Uid: " << uid << " está limitado para " << limiteProc->rlim_max << " processos" << std::endl;

}
void limit_users(rlimit *limiteProc){
	std::string cmd = "awk -F: \'($3 >= 1000) {printf \"%s\\n\",$3}\' /etc/passwd";
	std::string uids = exec(cmd.c_str());
	std::istringstream iss(uids);
	std::string line;
	while (std::getline(iss, line))
	{
    	limit(line, limiteProc);
	}
}

int main(int argc, char **argv){
 	NUM_PROC = atoi(argv[1]);
 	rlimit limiteProc;
 	limiteProc.rlim_cur = NUM_PROC;
 	limiteProc.rlim_max = NUM_PROC;
 	limit_users(&limiteProc);
}