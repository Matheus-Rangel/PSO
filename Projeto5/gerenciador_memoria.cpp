#include <string>	//string
#include <stdlib.h>	//system
#include <iostream>	//cout
#include <memory>	//shared_ptr
#include <sstream>	//stringstream

using namespace std;

//Função que recupera a saída de um comando do terminal como string
string exec(const char* cmd) {
    array<char, 128> buffer;
    string result;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
            result += buffer.data();
    }
    result.erase(result.end()-1);
    return result;
}


int main(){

	string memoriaTotal = exec("cat /proc/meminfo | grep -n ^ | grep ^1: | awk '{print $2 FS $3}'");
	string memoriaLivre = exec("cat /proc/meminfo | grep -n ^ | grep ^2: | awk '{print $2 FS $3}'");
	cout << endl << "Memória Total: "<< memoriaTotal << endl;
	cout << "Memória Livre: "<< memoriaLivre << endl;

	string cache = exec("cat /proc/meminfo | grep -n ^ | grep ^5: | awk '{print $2 FS $3}'");
	cout << endl << "Memória Cache: "<< cache << endl;

	string swapTotal = exec("cat /proc/meminfo | grep -n ^ | grep ^15: | awk '{print $2 FS $3}'");
	string swapLivre = exec("cat /proc/meminfo | grep -n ^ | grep ^16: | awk '{print $2 FS $3}'");
	cout << endl << "Swap Total: "<< swapTotal << endl;
	cout << "Swap Livre: "<< swapLivre << endl;

	string usuario = exec("users");
	string comando = "ps -f -u " + usuario + " | awk '{print $2}'";
	string saida = exec(comando.c_str());

	stringstream ss;
	ss.str (saida);
	string pid;
	ss >> pid; //Descartando a linha de título PID

	/*cout << endl << "Falta de página por processo:" << endl;
	cout << "PID\tMINFL\tMAJFL" << endl;
	while(!ss.eof()){
		ss >> pid;
		//comando = "ps -o pid,min_flt,maj_flt " + pid + " | grep -n ^ | grep ^2: | awk '{print $2 FS $3 FS $4}'";
		comando = "ps -o pid,min_flt,maj_flt " + pid + " | grep -n ^ | grep ^2:";
		//comando = "ps -o pid,min_flt,maj_flt " + pid;
		saida = exec(comando.c_str());
		cout << saida << endl;
		//cout << comando << endl;
	}*/
	//sleep
}